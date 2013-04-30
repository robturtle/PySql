#!/usr/bin/env python
# Filename: function.py
# Author:   LIU Yang
# Create Time: Sat Apr 27 23:53:56 CST 2013
# License:     LGPL v2.0+
# Contact Me:  JeremyRobturtle@gmail.com
"""Programming Language Parser
Function objects
"""
#TODO:
"""
1. batter way to handle '(' ')'
2. transitively construct Function instances
"""

class Function(object):
	def __init__(self, name, *args):
		self.name = name
		self.args = args
	@staticmethod
	def parse(string):
		if not string: return Function('')
		string = string.replace(')','')
		parts = string.split('(')
		name = parts[0]
		args = [p.strip() for p in parts[1].split(',') if p!=''] if len(parts)>1 else []
		return Function(name, *args)
	def __str__(self):
		return self.name+'('+','.join(self.args)+')'
	def __repr__(self):
		return 'Function("'+self.name+'","'+'","'.join(self.args)+'")'
	def __nonzero__(self):
		return bool(self.name) or bool(self.args)

if __name__ == '__main__':
	print Function.parse('').__repr__()
	print Function.parse('()').__repr__()
	print Function.parse('f(a,b)')
	print Function.parse('f(a,b)').__repr__()

	print bool(Function.parse(''))
	print bool(Function.parse('()'))
	print bool(Function.parse('(1)'))
	print bool(Function.parse('f(1)'))
