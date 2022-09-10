#!/bin/python3

from db import log, addShow, getShowByName, listShows, allShows, logs
import sys

args = sys.argv[1:]

def error(msg):
	print(msg)
	input()
	exit()


if len(args) == 1 and args[0] == 'list':
	listShows()
	exit()


if len(args) == 1 and args[0] == 'add':
	addShow()
	exit()

if len(args) == 1 and (args[0] == 'shows' or args[0] == 'all'):
	allShows()
	exit()

if len(args) == 1 and args[0] == 'logs':
	logs()
	exit()
