#!/usr/bin/env python
# Filename: sql_formatter.py
# Author:   LIU Yang
# Create Time: Sun Apr 28 19:16:16 CST 2013
# License:     LGPL v2.0+
# Contact Me:  JeremyRobturtle@gmail.com
"""Basic Components of SQL Concepts
A Formatter indicates how to transfer a string data
into correct type, and provides a format string
"""
from util    import Display
from mytypes import Function

class Formatter(Display):
	"""Formatter indicates how to transfer
    an attribute into correct type.

    Members:

	dtype:
		Data's type.
    trans:
		A type transformer
    fmt:
		A string formatter

    """
	type_fmt_map = {'varchar':None, 'numeric':None, 'int':None}
	def __init__(self, dtype, trans, fmt, special=None):
		self.dtype = dtype
		self.trans = trans
		self.fmt   = fmt
		self.spec  = special
	@classmethod
	def parseString(cls, string):
		if not string: return None
		func = Function.parse(string)
		return cls.parseFunction(func)
	@classmethod
	def parseFunction(cls, func):
		typename = func.name
		"""In SQL, arguments of the types are numbers indicating its width"""
		args = [int(arg) for arg in func.args]
		return cls.type_fmt_map[typename](*args)
	def __call__(self, val):
		"""Returning a formatted string."""
		return self.fmt % self.trans(val)
	#TODO: implement special parse

class FormatVarchar(Formatter):
	"""SQL varchar type

	Members:

	width:
		data's minimum width (in char)
	"""
	def __init__(self, width):
		dtype = 'varchar'
		fmt = r'%-{0:d}r'.format(width)
		super(FormatVarchar, self).__init__(dtype, str, fmt)
		Formatter.type_fmt_map[dtype] = self.__class__

FormatVarchar(1) # Updata Formatter's type_fmt_map


class FormatNumeric(Formatter):
	"""SQL numeric type

	Members:

	a, b:
		%a.bf --- precision of number
	"""
	def __init__(self, a, b=0):
		dtype = 'numeric'
		if b == 0:
			fmt = r'%-{0:d}d'.format(a)
			super(FormatNumeric, self).__init__(dtype, int, fmt)
		else:
			fmt = r'%-{0:d}.{1:d}f'.format(a,b)
			super(FormatNumeric, self).__init__(dtype, float, fmt)
		Formatter.type_fmt_map[dtype] = self.__class__

FormatNumeric(1) # Updata Formatter's type_fmt_map


class FormatInt(Formatter):
	"""SQL int type
	"""
	def __init__(self):
		dtype = 'int'
		super(FormatInt, self).__init__(dtype, int, '%-6d')
		Formatter.type_fmt_map[dtype] = self.__class__

FormatInt() # Updata Formatter's type_fmt_map




if __name__ == '__main__':
	print Formatter.type_fmt_map
	fmter = Formatter.parseString('varchar(20)')
	print fmter
	fmter = Formatter.parseString('numeric(4,2)')
	print fmter
