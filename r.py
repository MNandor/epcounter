#!/bin/python3

from db import log, addShow, getShowByName, listShows, logs, finishShow, editShow, showFinishes, changeState, executeCommand, logSearch, addTag, removeTag, changeReference
from printing import promptShowDetails, stringToShow
import sys
import re

args = sys.argv[1:]

# Command, function to execute
cmdArgless=[
	(['list'], lambda: listShows(True)),
	(['shows', 'all'], lambda: listShows(False)),
	(['logs'], lambda: logs()),
	(['finishes', 'history'], lambda: showFinishes()),
]

# Handle commands with no arguments
if len(args) == 1:
	arg = args[0]
	for cmd, lamb in cmdArgless:
		if arg in cmd:
			lamb()
			exit()


ns = lambda x: exit('not supported')
nn = lambda: None

# Command, function to execute, function if there is no argument, function if there are
cmdArg=[
	(['dog'], lambda x: print('hi'), lambda: input(), lambda x: print(stringToShow(x))),
	(['add'], lambda x: addShow(x), lambda: promptShowDetails(), ns),
	(['finish'], lambda x: finishShow(), nn,  ns),
	(['edit', 'modify'], lambda x: editShow(), nn, ns),
	(['change', 'changestate'], lambda x: changeState(), nn, ns),
	(['logsearch', 'searchlogs'], lambda x: logSearch(x), lambda: int(input('Show ID: ')), ns),
	(['tag'], lambda x: addTag(), nn,  ns),
	(['untag', 'removetag'], lambda x: removeTag(), nn,  ns),
	(['changereference', 'reference', 'refer', 'rewatch', 'season', 'newseason'], lambda x: changeReference(), nn,  ns),
	(['grep', 'search'], lambda x: listShows(False, x), lambda: input("Search term: "), lambda x: x),
]

# Handle commands with potentional arguments
for cmd, lamb, funIsnt, funIs in cmdArg:
	if args[0] in cmd:
		if len(args) == 1:
			x = funIsnt()
			print(x)
			lamb(x)
		else:
			args = ' '.join(args[1:])
			x = funIs(args)
			lamb(x)
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
