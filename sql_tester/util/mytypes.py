#!/usr/bin/env python
# Filename: function.py
# Author:   LIU Yang
# Create Time: Sat Apr 27 23:53:56 CST 2013
# License:     LGPL v2.0+
# Contact Me:  JeremyRobturtle@gmail.com
"""Programming Language Parser
Function objects
"""
from display import Display

class Function(Display):
	def __init__(self, string, name, *args):
		self.string = string
		self.name = name
		self.args = args

if __name__ == '__main__':
	f = Function('f(a, b)', 'f', 'a', 'b')
	print f
