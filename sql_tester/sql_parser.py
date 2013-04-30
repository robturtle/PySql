#!/usr/bin/env python
# Filename: sql_parser.py
# Author:   LIU Yang
# Create Time: Mon Apr 29 21:49:39 CST 2013
# License:     LGPL v2.0+
# Contact Me:  JeremyRobturtle@gmail.com
"""plain text --> instance tree
"""
from sql_exception import *
from util          import Display, ListDeducer
from sql_db        import Database
import sys

class SqlParser(Display):
	def __init__(self, reader, writer=sys.stdout):
		self.dmap = {'database':[Database, '\n']}
		self.parser = ListDeducer(self.dmap)
		self.reader = reader
		self.writer = writer
	def process(self):
		line = self.reader.readline()
		if not line: return
		self.parser.opts = line.split()
		database = self.parser()
		database.parse(self.reader)
		self.writer.write(str(database))




if __name__ == '__main__':
	parser = SqlParser(open('spam'))
	parser.process()
