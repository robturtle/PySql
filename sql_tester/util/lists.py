#!/usr/bin/env python
# Filename: lists.py
# Author:   LIU Yang
# Create Time: Mon Apr 29 23:54:45 CST 2013
# License:     LGPL v2.0+
# Contact Me:  JeremyRobturtle@gmail.com
"""Deduce functions and arguments in a list
"""
from mytypes import Function

class ListDeducer:
	def __init__(self, deduce_map, *args):
		self.dmap = deduce_map
		self.opts = list(args)
	def __call__(self, *args):
		opt = self.opts.pop(0)
		if opt in self.dmap:
			args = list(args)
			func, ex_arg_count = self.dmap[opt]
			args.extend(self._fetchArgs(ex_arg_count))
			ret = func(*args) if args else func()
		else:
			raise KeyError, "handler of %r not registered!" % opt
		return ret
	def _fetchArgs(self, count):
		if type(count) == type(''):
			try:
				idx = self.opts.index(count)
			except ValueError:
				"""string count is treated as delimiter. So we assume
				there ain't one at end of the list
				"""
				idx = len(self.opts)
		else:
			idx = int(count)
		ex_args = self.opts[:idx]
		self.opts = self.opts[idx:]
		return ex_args
	def __nonzero__(self):
		return len(self.opts) != 0
	"""Some useful functions as dmap's value"""
	@staticmethod
	def passOpts(*args):
		return args




if __name__ == '__main__':
	def rev(seq):
		return seq[::-1]

	deduce_map = {'-U':[str.upper, 0],
	              '-a':[str.__add__, 1],
	              '-r':[rev, 0],
				  }

	x = ListDeducer(deduce_map)
	x.opts = [1, 2, 3]
	x.opts = ['-U', '-r', '-a', ' Python!', '@', 'department', 'dept_name']
	s = x('hello, world!'); print s
	s = x(s); print s
	s = x(s); print s
	try:
		s = x(s)
	except KeyError:
		pass
	else:
		raise SystemError, "I need an exception here"

	print
	print 'Test _fetchArgs'
	x.opts = [1, 2, 3, 4, 5, 6, '@', 7, 8, 9]
	print x._fetchArgs(2)   == [1,2]
	print x._fetchArgs('@') == [3,4,5,6]
	print x._fetchArgs(1)   == ['@']
	print x._fetchArgs('@') == [7,8,9]

	x.dmap['pass'] = [ListDeducer.passOpts, '@']
	x.opts = ['pass', 1, 2, 3, 4, 5, 6, '@', 7, 8, 9]
	print x() == (1,2,3,4,5,6);
