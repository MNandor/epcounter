#!/bin/python3

from db import log, addShow, getShowByName, listShows, allShows, logs
from printing import promptShowDetails
import sys

args = sys.argv[1:]



if len(args) == 1 and args[0] == 'list':
	listShows()
	exit()


if len(args) == 1 and args[0] == 'add':
	item = promptShowDetails()
	addShow(item)
	exit()

if len(args) == 1 and (args[0] == 'shows' or args[0] == 'all'):
	allShows()
	exit()

if len(args) == 1 and args[0] == 'logs':
	logs()
	exit()
