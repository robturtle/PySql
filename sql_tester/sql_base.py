#!/usr/bin/env python
# Filename: sql_base.py
# Author:   LIU Yang
# Create Time: Tue Apr 30 19:54:18 CST 2013
# License:     LGPL v2.0+
# Contact Me:  JeremyRobturtle@gmail.com
from util import Display
class Entity(Display):
	def __init__(self, name, *options):
		self.name    = name
		self.options = options
	def __eq__(self, other):
		return self.name == other.name

