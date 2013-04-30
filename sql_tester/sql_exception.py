#!/usr/bin/env python
# Filename: sql_exception.py
# Author:   LIU Yang
# Create Time: Sun Apr 28 21:52:49 CST 2013
# License:     LGPL v2.0+
# Contact Me:  JeremyRobturtle@gmail.com
"""SQL Exceptions:
	SqlException:
		base.

		ViolateOperation:
			invoking violate methods, or available methods
			at bad times.

		ForeignRefError:
			Raises if some resources reference to a
			foreign position which didn't has it.
"""

class SqlException(Exception):
	"""Base exception of SQL Test Package
	"""

class ViolateOperation(SqlException):
	"""If you do something you cannot do,
	you will see me.
	"""

class ForeignRefError(SqlException):
	"""If some resource you references do not exist,
	you will see me.
	"""

class SqlTypeError(SqlException):
	"""If you assign a variable with a mismatched type,
	you will see me.
	"""
