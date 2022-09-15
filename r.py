#!/bin/python3

from db import log, addShow, getShowByName, listShows, logs, finishShow, editShow
from printing import promptShowDetails
import sys

args = sys.argv[1:]



if len(args) == 1:
	if args[0] == 'list':
		listShows(True)
		exit()

	if args[0] == 'add':
		item = promptShowDetails()
		addShow(item)
		exit()

	if (args[0] == 'shows' or args[0] == 'all'):
		listShows(False)
		exit()

	if args[0] == 'logs':
		logs()
		exit()

	if args[0] == 'finish':
		finishShow()
		exit()

	if args[0] == 'edit':
		editShow()
		exit()


if len(args) > 1:
	if args[0] == 'grep':
		listShows(False, ' '.join(args[1:]))
		exit()
