#!/usr/bin/env python
# Filename: sql_db.py
# Author:   LIU Yang
# Create Time: Mon Apr 29 20:09:55 CST 2013
# License:     LGPL v2.0+
# Contact Me:  JeremyRobturtle@gmail.com
"""Basic Components of SQL Concepts
Table represents an entity containing
a bunch of attributes.
"""
from util          import ListDeducer
from sql_exception import *
from sql_base      import Entity
from sql_table     import Table

class Database(Entity):
	def __init__(self, name, *options):
		"""Members:
		name:
			Database's name.
		options:
			A sequence containing options. There're:
			'extern':
				Indicating this database already existed in real Database.
				So there's no need to generate 'create database' query.
		"""
		super(Database, self).__init__(name, *options)
		self.tables = []
		self.extern = False
		self.optmap = {'extern'     :[self.setExtern,0],
				       'charset'    :[Database.setCharset,1]}
		self.optparser = ListDeducer(self.optmap, *self.options)
		self.tabmap = {'table'      :[self.addTable, '\n']}
		self.tabparser = ListDeducer(self.tabmap)
		self.fmtstr = self.parseOption()
	def parseOption(self):
		fmtstr = 'create database {0};\nuse {0};\n'
		while (self.optparser):
			fmtstr = self.optparser(fmtstr)
		return fmtstr
	def __str__(self):
		"""Return a SQL Queries string"""
		s = self.fmtstr.format(self.name) if not self.extern else ''
		for table in self.tables:
			s = s + str(table)
		return s
	def parse(self, reader):
		self.reader = reader
		while True:
			line = reader.readline()
			if not line: break
			self.tabparser.opts = line.split()
			table = self.tabparser()

	"""Option Handlers"""
	def setExtern(self, passthrow):
		self.extern = True
		return passthrow
	@staticmethod
	def setCharset(s, encode):
		idx = s.index(';')
		return s[:idx] +' character set '+ encode +s[idx:]
	"""Table Handlers"""
	def addTable(self, *args):
		table = Table(self, *args)
		self.tables.append(table)
		table.parse(self.reader)
		return table





if __name__ == '__main__':
	sql_optmap = {'database':[Database, '@']}
	input_s  = 'database scut extern charset utf8 @ tysihua @ BeiDa'
	db_reducer = ListDeducer(sql_optmap, *input_s.split())
	database = db_reducer()
	print database.name
	print database.options
	print database.fmtstr
	print database.extern
	database.extern = False
	print database
	database.parse(open('spam'))
	print database
