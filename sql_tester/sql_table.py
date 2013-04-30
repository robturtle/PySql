#!/usr/bin/env python
# Filename: sql_table.py
# Author:   LIU Yang
# Create Time: Sun Apr 28 22:43:52 CST 2013
# License:     LGPL v2.0+
# Contact Me:  JeremyRobturtle@gmail.com
"""Basic Components of SQL Concepts
Table represents an entity containing
a bunch of attributes.
"""
from util          import ListDeducer
from sql_exception import *
from sql_base      import Entity
from sql_column    import Column

class LogicTable(Entity):
	"""A Logical Table is a combination of 2 physical table.
	While printed, it combine two tables's data to reach the count 'combiner.count'.

	It combine the whole set of left and a generated subset of right.
	So if the subset == right's complete set, a Cartesian product is to output.
	Otherwise the output would be regard as a relationship.

	It's useful to generate a random combined data if you pass a random combiner.
	"""
	def __init__(self, database, name, ltab, rtab, combiner=None):
		"""Members:
		name:
			LogicTable's name.
		ltab, rtab:
			left table, right table.
		combiner:
		A callable to generate right table's subset.
		If it's None, right table's complete set will be generated.
		"""
		super(LogicTable, self).__init__(name, None)
		self.ltab = ltab
		self.rtab = rtab
		self.combiner = combiner

class Table(Entity):
	"""Members:

	name:
		Table's name.
	extern:
		Is this table existed yet?
	cols:
		Table's columns


	Exceptions:

		ViolateOperation:
			if you're trying to:
				- Append a existed column
		ForeignRefError:
			If you're appending a value references from
			a foreign key and it doesn't has one
	"""
	inserthead = "insert into %-20s values ("
	inserttail = ");\n"
	def __init__(self, database, name, *options):
		super(Table, self).__init__(name, *options)
		self.colsetidx = 0
		self.cols     = []
		self.rows     = []
		self.refers   = []
		self.database = database
		self.extern   = False
		self.optmap   = {'extern'      :[self.setExtern,0],
				         '@'           :[self.setRefer,'@']}
		self.optparser = ListDeducer(self.optmap, *self.options)
		self.colmap   = {'*'           :[self.addCol, '*'],
				         '|'           :[self.setCol, '|']}
		self.colparser = ListDeducer(self.colmap)
		self.fmtstr    = self.parseOption()
	def parseOption(self):
		fmtstr = '\ncreate table %-20s (\n'
		while self.optparser:
			fmtstr = self.optparser(fmtstr)
		return fmtstr
	def parse(self, reader):
		"""Read from reader and parse into
		SQL Queries
		"""
		"""Parse Column info"""
		for i in range(2):
			colline = reader.readline()
			self.colparser.opts = colline.split()
			while self.colparser:
				self.colparser()
		"""Parse Row info"""
		while True:
			rowline = reader.readline()
			if rowline == '\n' or not rowline: break
			row = [val.strip() for val in rowline.split('|') if val]
			row += [None] * (len(self.cols)-len(row)) # There may be some random column have no data
			row = [col.fmter.trans(val) for col, val in zip(self.cols, row)]
			self.addRow(row)
	def addCol(self, *args): # Append Column
		if not args: return None
		col = Column(self, *args)
		if col in self.cols:
			raise ViolateOperation, "The column %r already existed!" % col.name
		self.cols.append(col)
		for row in self.rows:
			row.append(None) #TODO: check for constraint 'not null'
		return col
	def setCol(self, *args):
		if not args: return None
		col = self.cols[self.colsetidx]
		self.colsetidx += 1
		col.selfparser.opts = ['datatype']+ list(args)
		col.selfparser()
	def addRow(self, row): # Insert Row
		if len(row) > len(self.cols):
			raise SqlTypeError, "Inserting tuple %r's size mismatched with table %r(%d)" % (row, self.name, len(self.cols))
		[col.checkForeign(val) for col, val in zip(self.cols, row)]
		self.rows.append(row)
	def __str__(self):
		"""output in SQL codes"""
		s = self.fmtstr % self.name if not self.extern else ''
		for col in self.cols:
			s = s+ str(col)
		s = s[:-2] + ');\n\n' # get rid of ',\n'
		insertfmt = self.insertfmt()
		for row in self.rows:
			row = [col.fmter.trans(val) for col, val in zip(self.cols, row)]
			s = s+ insertfmt % tuple(row)
		return s
	def insertfmt(self):
		"""Return a string formatter for this table"""
		head = 'insert into %-15s values(' % self.name
		main = ', '.join([col.fmter.fmt for col in self.cols])
		return head + main + ');\n'
	"""Option Handlers"""
	def setExtern(self, passthrow):
		self.extern = True
		return passthrow
	def setRefer(self, passthrow, *args):
		for table in self.database.tables:
			if table.name == args[0]:
				self.refers.append(table)
				break
		else:
			raise LookupError, "Referencing table %r not existed in database %r" % (args[0], self.database.name)
		return passthrow
	def show(self):
		#TODO: Add Framework: I need create some utils
		title = [str(col.name)+' ' for col in self]
		values = '\n'.join([self.showfmt() % row for row in zip(*self)])
		print title +'\n'+ values




if __name__ == '__main__':
	t = Table(None, 'student')
	t.cols.append(Column(t, '#sid', 'datatype', 'varchar(12)'))
	t.cols.append(Column(t, 'name', 'datatype', 'varchar(20)'))
	try:
		t.addCol('sid', 'datatype', 'varchar(12)')
	except ViolateOperation as e:
		pass
	else:
		raise Exception, "expect exception here!"
	print t

	rec = ('001', 'Jeams Boy', '123')
	try:
		t.addRow(rec)
	except SqlTypeError as e:
		print e
	rec = rec[:2]
	t.addRow(rec)
	t.addRow(('002', 'Jeams Girl'))
	print t

	t = Table(None, 'student')
	t.addCol('#sid', 'datatype', 'varchar(12)')
	t.addCol('name', 'datatype', 'varchar(20)')
	t.addCol('nickname', 'datatype', 'varchar(20)',)
	print t
