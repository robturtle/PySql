#!/usr/bin/env python
# Filename: sqlize.py
# Author:   LIU Yang
# Create Time: Wed May  1 01:13:53 CST 2013
# License:     LGPL v2.0+
# Contact Me:  JeremyRobturtle@gmail.com
from sql_tester import SqlParser
import sys
import getopt

def usage():
	print 'Usage:', sys.argv[0], 'inputfile [-o output.sql]'
	sys.exit(1)

try:
	opts, args = getopt.getopt(sys.argv[1:], "ho:", ["help", "output="])
	inputfile = args[0]
except (getopt.GetoptError, IndexError) as e:
	print e
	usage()

writer = sys.stdout
for o, a in opts:
	if o in ("-h", "--help"):
		usage()

parser = SqlParser(open(inputfile), writer)
parser.process()
