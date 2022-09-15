#!/bin/python3

from db import log, addShow, getShowByName, listShows, logs, finishShow, editShow, showFinishes, changeState, executeCommand
from printing import promptShowDetails
import sys
import re

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

	if args[0] == 'finishes':
		showFinishes()
		exit()

	if args[0] == 'change':
		changeState()
		exit()


if len(args) > 1:
	if args[0] == 'grep':
		listShows(False, ' '.join(args[1:]))
		exit()


commandre = re.compile('^([0-9o\+])+$')


if len(args) > 0 and commandre.match(args[0]) != None:
	command = args[0]
	args = args[1:]
else:
	command = 'o'



show = ' '.join(args).strip()

print((command, show))

show = getShowByName(show)
print(show[1])

executeCommand(command, show)
