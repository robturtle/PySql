#!/usr/bin/env python
# Filename: sql_column.py
# Author:   LIU Yang
# Create Time: Sun Apr 28 21:08:31 CST 2013
# License:     LGPL v2.0+
# Contact Me:  JeremyRobturtle@gmail.com
"""Basic Components of SQL Concepts
Column represents an attribute of an object,
a column of a table.
"""
from util          import ListDeducer, RandomRanger
from sql_base      import Entity
from sql_exception import *
from sql_formatter import Formatter
import random

class Column(Entity):
	"""Members:

	name:
		Column's name.
	primary:
		Whether it's a primary key.
	foreign:
		Foreign key's reference.
	fmter:
		Formatter of Column, indicates its datatype.

	Methods:

	setfmt(self, fmter) <-- fmter

	append(self, val) @override:
		Check validity of foreign key references.


	Exceptions:

		ViolateOperation:
			if you try to do sort or other a SQL Column
			can't do.
		ForeignRefError:
			If you're appending a value references from
			a foreign key and it doesn't has one
	"""
	def __init__(self, table, name, *options):
		self.table = table
		if name.startswith('#'):
			name = name[1:]
			self.primary = True
		else:
			self.primary = False
		super(Column, self).__init__(name, *options)
		self.data    = []
		self.foreign = None
		self.selfmap = {'@'       :[self.setForeign, 2],
				        'datatype':[self.setFmter,  '\n']}
		self.selfparser = ListDeducer(self.selfmap, *options)
		self.specialmap = {'random':[self.setRandom, 2],
				           'choice':[self.setChoice, 0],
						   'exchoice':[self.setExcludeChoice,0]}
		self.specparser = ListDeducer(self.specialmap)
		if options: self.selfparser()
	def setForeign(self, *args):
		tabidx, colidx = [int(arg) for arg in args]
		self.foreign = self.table.refers[tabidx].cols[colidx]
	def setFmter(self, fmtstr, *specials):
		self.fmtstr  = fmtstr
		self.fmter   = Formatter.parseString(fmtstr)
		if specials:
			self.specparser.opts = list(specials)
			self.specparser()
	def setRandom(self, a, b):
		self.fmter.trans = RandomRanger(float(a),float(b))
	def setChoice(self):
		self.fmter.trans = self.randomChoice
	def setExcludeChoice(self):
		self.exidx = 0
		self.fmter.trans = self.excludeChoice
	def excludeChoice(self, val):
		if val not in self.data: return val
		if self.exidx == 0:
			random.shuffle(self.data)
		val = self.data[self.exidx]
		self.exidx += 1
		if self.exidx >= len(self.data):
			self.exidx = 0
		return val
	def randomChoice(self, val):
		if val in self.data:
			return random.choice(self.data)
		else:
			return val
	def checkForeign(self, val): #TODO: change
		if self.foreign and val not in self.foreign:
			raise ForeignRefError, "Foreign column %r doesn't has this value: %r" % (self.foreign.name, val)
		self.data.append(val)
	def __nonzero__(self):
		return bool(self.name)
	def __str__(self):
		indent = '    '
		s = indent + '%-12s'%self.name +' '+ self.fmtstr +',\n'
		if self.primary:
			s = s+ indent +'primary key('+self.name+'),\n'
		if self.foreign:
			s = s+ indent +'foreign key('+self.foreign.name+')\n'
			s = s+'  ' + indent +'references '+ self.foreign.table.name +"("+ self.foreign.name +"),\n"
		return s




if __name__ == '__main__':
	col = Column('name', 'varchar(20)')
	col.append('a')
	col.append('b')
	col.append(3.14)
	print repr(col)
	print '3.14 in col?', 3.14 in col

	col2 = Column('nickname', 'varchar(20)', col)
	col2.append('a')
	col2.append('a')
	col2.append(3.14)
	try:
		col2.append('spam')
	except ForeignRefError as e:
		print e
	print col2

	try:
		col.sort()
	except ViolateOperation as e:
		print e

	col3 = Column('id', 'int')
	print col3.fmter
	col3.setfmt('varchar(20)')
	print col3.fmter

	col4 = Column('id', 'int')
	col3.append(1)
	col4.append(2)
	print col4 == col3
	print col4.__eq__(col3)

	col5 = Column('balance', 'numeric(4,2)')
	col5.append(34.34)
	col5.append('45.68')
	print col5
