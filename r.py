#!/bin/python3

from db import log, addShow, getShowByName, listShows, logs, finishShow, editShow, showFinishes, changeState, executeCommand, logSearch, addTag, removeTag, changeReference
from printing import promptShowDetails, stringToShow
import sys
import re
from newSeason import checkSeasonalAnime

args = sys.argv[1:]

# define missing lambdas
ns = lambda x: exit('not supported')
nn = lambda: None

def displayHelp():
	global cmdArg
	for cmd in cmdArg:
		print(','.join(cmd[0]))
		print('\t', cmd[4])

# Command, function to execute, function if there is no argument, function if there are
cmdArg=[
	(['list', 'ls'],
		lambda x: listShows(True),
		nn,
		ns,
		"Displays shows actively being watched.",
	),
	(['shows', 'all'],
		lambda x: listShows(False),
		nn,
		ns,
		"Display all shows in database.",
	),
	(['logs'],
		lambda x: logs(),
		nn,
		ns,
		"Display all logs in database.",
	),
	(['finishes', 'history'],
		lambda x: showFinishes(),
		nn,
		ns,
		"Display dates of all shows marked finished.",
	),
	(['help'],
		lambda x: displayHelp(),
		nn,
		ns,
		"Take a wild guess.",
	),

	(['add'],
		lambda x: addShow(x),
		lambda: promptShowDetails(),
		ns,
		"Add a new show to the database.",
	),
	(['finish'],
		lambda x: finishShow(),
		nn,
		ns,
		"Mark a show as finished.",
	),
	(['edit', 'modify'],
		lambda x: editShow(),
		nn,
		ns,
		"Change the details of a show (from active list).",
	),
	(['change', 'changestate'],
		lambda x: changeState(),
		nn,
		ns,
		"Change the state of the show, such as \"watching\" or \"to watch\".",
	),
	(['logsearch', 'searchlogs'],
		lambda x: logSearch(x),
		lambda: int(input('Show ID: ')),
		ns,
		"Search through logs by show ID.",
	),
	(['tag'],
		lambda x: addTag(),
		nn,
		ns,
		"Add a custom tag to a show.",
	),
	(['untag', 'removetag'],
		lambda x: removeTag(),
		nn,
		ns,
		"Remove a custom tag from a show.",
	),
	(['changereference', 'reference', 'refer', 'rewatch', 'season', 'newseason'],
		lambda x: changeReference(),
		nn,
		ns,
		"Reference a previous season or previous watch of a show.",
	),
	(['grep', 'search'],
		lambda x: listShows(False, x),
		lambda: input("Search term: "),
		lambda x: x,
		"Search through all shows.",
	),
	(['checkseasonal', 'seasonal'],
		lambda x: checkSeasonalAnime(),
		nn,
		ns,
		"Check MAL for seasonal anime.",
	),
]

# Handle commands with potentional arguments
for cmd, lamb, funIsnt, funIs, _ in cmdArg:
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
