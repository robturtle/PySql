#!/usr/bin/env python
# Filename: lang_parser.py
# Author:   LIU Yang
# Create Time: Mon Apr 29 16:52:10 CST 2013
# License:     LGPL v2.0+
# Contact Me:  JeremyRobturtle@gmail.com
"""Language Parser
"""
import re

class LangParser(object): pass
#TODO: make it inherit from Singleton

class FuncParser(LangParser):
	def __init__(self):
		self.pat = re.compile(r'(.*)\(([^()]*)\)')
	def __call__(self, string):
		from mytypes import Function
		match = self.pat.match(string)
		retlst = [match.group(0), match.group(1)]
		args = [arg.strip() for arg in match.group(2).split(',')]
		return Function(*(retlst + args))

funcParser = FuncParser()




if __name__ == '__main__':
	s = 'numeric(8,2)'
	print funcParser(s)
