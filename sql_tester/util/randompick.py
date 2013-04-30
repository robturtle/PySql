#!/usr/bin/env python
# Filename: randompick.py
# Author:   LIU Yang
# Create Time: Sun Apr 28 11:40:09 CST 2013
# License:     LGPL v2.0+
# Contact Me:  JeremyRobturtle@gmail.com
"""Random pick sereral items from a sequence
"""
import random

class RandomGenerator(object): pass

class RandomChoicer(RandomGenerator):
	def __init__(self, seq):
		self.seq = seq
	@staticmethod
	def __call__(*nouse):
		return random.choice(self.seq)

class RandomRanger(RandomGenerator):
	def __init__(self, lo, hi):
		self.lo = lo
		self.hi = hi
	@staticmethod
	def randomRange(lo, hi):
		return random.random()*(hi-lo) + lo
	def __call__(self, *nouse):
		return self.randomRange(self.lo, self.hi)

class RandomPicker(RandomGenerator):
	def __init__(self, seq, n):
		self.seq = seq
		self.n   = n
	@staticmethod
	def randomPick(seq, n):
		"""Random pick n items from sequence seq.

		WARNING:
			This will change the seq in place. If
			that's not what you want, pass a copy
			of seq as parameter.

		Exception:
			IndexError if n > len(seq)
		"""
		random.shuffle(seq)
		return seq[:int(n)]
	def __call__(self):
		return self.randomPick(self.seq, self.n)

class RangePicker(RandomGenerator):
	"""Pickup a subset of a sequence with a range of count
	"""
	def __init__(self, lo, hi):
		"""Members:
		size:
			Size of the output.
		lo:
			minimum size of generated seq.
		hi:
			maximum size of generated sq.
		"""
		self.lo   = lo
		self.hi   = hi
	def __call__(self, seq):
		size = RandomRanger.randomRange(self.lo, self.hi)
		return RandomPicker.randomPick(seq, size)

if __name__ == '__main__':
	r = RandomRanger(1, 10)
	for i in range(10):
		print round(r(), 2)

	rp = RandomPicker([1, 2, 3, 4, 5, 6], 4)
	for i in range(10):
		print rp()

	print; print 'Range Picker'
	rgp = RangePicker(0, 5)
	for i in range(10):
		print rgp([1,2,3,4,5,6])
