#!/usr/bin/env python
# Filename: display.py
# Author:   LIU Yang
# Create Time: Sun Apr 28 20:35:21 CST 2013
# License:     LGPL v2.0+
# Contact Me:  JeremyRobturtle@gmail.com
"""Friendly Display classes and instances
"""

class Display(object):
	def __str__(self):
		s = '<'+ self.__class__.__name__
		s = s + self.getattr() +'>\n'
		return s
	def getattr(self):
		s = ''
		for k in self.__dict__:
			s = s +'\n'+ '%-12s'%k +': '+ str(self.__dict__[k])
		return s




if __name__ == '__main__':
	class A(Display):
		a = 1
		b = 2
	a = A()
	a.c = 3
	print a
