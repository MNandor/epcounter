#!/bin/python3

from db import log, addShow, getShowByName, listShows, logs, finishShow, editShow, showFinishes, changeState, executeCommand, logSearch, addTag, removeTag, changeReference
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

	if args[0] in ['edit', 'modify']:
		editShow()
		exit()

	if args[0] in ['finishes', 'history']:
		showFinishes()
		exit()

	if args[0] in ['change', 'changestate']:
		changeState()
		exit()

	if args[0] in ['logsearch', 'searchlogs']:
		print('Note: use "all" or "search" to find ID')
		id = int(input('ID: '))
		logSearch(id)
		exit()

	if args[0] in ['tag']:
		addTag()
		exit()

	if args[0] in ['untag', 'removetag']:
		removeTag()
		exit()

	if args[0] in ['changereference', 'reference', 'refer', 'rewatch', 'season', 'newseason']:
		changeReference()
		exit()


if len(args) > 1:
	if args[0] in ['grep', 'search']:
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
