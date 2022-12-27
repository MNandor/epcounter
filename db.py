#!/bin/python3

import sqlite3
import time
import os
from printing import displayShow, displayLog, error, selectShow, displayFinishes
from opener import seekOpenings, startWatching, writeTitles

# Todo use $HOME instead for file location
HOME=os.path.expanduser('~')+'/.local/share/mnprograms/'
os.makedirs(HOME, exist_ok=True)
con = sqlite3.connect(HOME+'Epcounter.db')
cur = con.cursor()


def create_db():

	# The main data is stored here

	# ID: unique ID number
	# Name: display name of the show
	# URL: the link to the show
	# - can be local file or web address
	# - character @ will be replaced by current episode number
	# - character * will invoke a regex search (todo)
	# State:
	# - 0 neutral (can be watched)
	# - 1 episode started (requires "did you watch" confirmation)
	# - 2 finished (show is hidden)
	# - 3 to watch list (hidden by default)
	# - 4 maybe watch list (same as to watch except different name)
	# - 5 abandoned
	# Next: the upcoming episode number
	# Padding: minimum length of url, padded with zeroes e.g. 4 -> 004 
	# Tags: a comma-separated list of user-defined tags
	# Reference:
	# - positive: references a previous season
	# - negative: absolute value references previous show that's being rewatched

	cur.execute("""CREATE TABLE IF NOT EXISTS shows(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		name TEXT NOT NULL,
		url TEXT,
		state INTEGER DEFAULT 0,
		next INTEGER DEFAULT 1,
		padding INTEGER DEFAULT 0,
		tags TEXT DEFAULT '',
		reference INTEGER DEFAULT 0
	);""")

	# Logs are for keeping history, in case the user wants this information later

	# ID: unique ID number
	# Timestamp: when the event occurred, Unix time 
	# Show: reference to the table above
	# Action: text description of the event

	cur.execute("""CREATE TABLE IF NOT EXISTS logs(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		timestamp INTEGER NOT NULL,
		show INTEGER NOT NULL,
		action TEXT NOT NULL
	);""")


	con.commit()

create_db()

def log(showID, action):
	now = int(time.time())

	cur.execute('INSERT INTO logs(timestamp, show, action) values (?,?,?)', (now, showID, action))
	con.commit()


def addShow(item):

	name, url, padding, state = item

	cur.execute('INSERT into shows(name, url, padding, state) values (?,?,?,?)', (name, url, padding, state))
	id1 = int(cur.lastrowid)

	cur.execute('SELECT MAX(id) from shows')

	id2 = cur.fetchone()[0]

	print(f'Inserted at ID {id1} {id2}')

	log(id1, "ADDED")


def getShowByName(name):

	#if empty string, select latest from log
	if name.strip() == '':
		cur.execute('SELECT * from logs')
		# yeah this crashes if the log is empty, *pretends to care*
		last = cur.fetchall()[-1][2]

		cur.execute('SELECT * FROM shows WHERE id = ?', (last,))
		return cur.fetchone()


	name = name.lower()
	# only select from shows not hidden by their state
	# this is anything currently beign watched regardless of whether
	# last episode was confirmed
	cur.execute("SELECT * FROM shows WHERE state < 2")
	res = cur.fetchall()

	sel = None
	for item in res:
		if name in item[1].lower():
			if sel == None:
				sel = item
			else:
				error(f'Multiple shows found! {sel} and {item}')

	if sel == None:
		error('No show found!')

	return sel




# Show a list of shows
def listShows(visibleOnly = False, grep=''):
	# Generally, visible only and grep are not used together. It's safe to ignore
	if visibleOnly:
		cur.execute("select * from shows where (state = 0 or state = 1)")
	else:
		cur.execute('select * from shows where name LIKE ?', (f'%{grep}%', ))

	res = cur.fetchall()
	for item in res:
		displayShow(item)

# used to map ids to names
logsMap = None

def updateLogsMap():
	global logsMap
	if logsMap == None:
		cur.execute('select id, name from shows')
		res = cur.fetchall()
		logsMap = {x[0]:x[1] for x in res}

def logs():
	global logsMap
	updateLogsMap()

	cur.execute('select * from logs')

	res = cur.fetchall()
	for item in res:
		displayLog(item, logsMap)



def finishShow():
	cur.execute("SELECT * FROM shows WHERE state < 2")
	res = cur.fetchall()

	print('Which show did you finish?')

	show = selectShow(res, True)[0]

	cur.execute('UPDATE shows SET state = 2 WHERE id = ?', (show[0], ))
	log(show[0], f"FINISHED SHOW")

	seekOpenings(show[1].replace(' ', '+'))

	writeTitles()




def editShow():
	cur.execute("SELECT * FROM shows WHERE state < 2")
	res = cur.fetchall()

	show = selectShow(res, True)[0]

	print('Make changes. Empty answer means unchanged except for URL')
	# todo give an easy option to leave url unchanged

	newname = input(f'Name: {show[1]} > ')
	if newname == '': newname = show[1]

	newURL = input(f'URL: {show[2]} > ')


	newpadding = input(f'Padding: {show[5]} > ')
	if newpadding == '':
		newpadding = show[5]
	else:
		newpadding = int(newpadding)

	cur.execute('UPDATE shows SET name = ?, url = ?, padding = ?  WHERE id = ?', (newname, newURL, newpadding, show[0]))
	log(show[0], f"EDITED FROM NAME: {show[1]} URL: {show[2]} PADDING: {show[5]}")


def showFinishes():
	cur.execute('SELECT shows.name, (logs.timestamp) FROM shows LEFT JOIN logs ON logs.show = shows.id WHERE shows.state == 2 GROUP BY shows.id ORDER BY logs.timestamp')
	res = cur.fetchall()

	displayFinishes(res)


def changeState():
	# != 2 hides finished shows for convenience
	# but they're still editable if you get the ID from "all"
	cur.execute('select * from shows where state != 2')

	res = cur.fetchall()
	shows = selectShow(res, False)
	ids = [x[0] for x in shows]

	print('Selected:')
	for item in res:
		if item[0] in ids:
			print(item[1])

	print('Desired state?')

	print('''STATES
	0 neutral
	1 requires "did you watch" confirmation
	2 finished
	3 watch list
	4 maybe watch list
	''')

	state = int(input())

	for id in ids:
		cur.execute('SELECT state FROM shows WHERE id = ?', (id,))
		oldstate = int(cur.fetchall()[0][0])
		cur.execute('UPDATE shows SET state = ? WHERE id = ?', (state, id))
		log(id, f'STATE CHANGE FROM {oldstate} to {state}')


def executeCommand(command, show):
	alsoOpen = False

	# do this at the end
	if 'o' in command:
		command = command.replace('o', '')
		alsoOpen = True

	"""MODES
		n: set next episode to n
		+n: set next episode to current next +n
		+++: like above but count plus signs
		++n: error
	"""


	#User started watching this episode but never confirmed finishing it, handle this
	if show[3] == 1 or command == '0': #or part necessary in case user forgets if it's been opened or not

		# Presuming having finished
		if command == '':

			cur.execute('SELECT * FROM logs WHERE show = ? and action = ?', (show[0], f'BEGAN EPISODE {show[4]}'))
			mylog = cur.fetchall()[-1]

			diff = int(time.time()) - mylog[1]
			diff = diff/60/60

			days = int(diff // 24)
			diff = diff % 24
			hours, minutes = int(diff), int(60*(diff-int(diff)))

			timespan = []
			if days > 0:
				timespan += [f'{days} days']

			if hours > 0:
				timespan += [f'{hours} hours']

			timespan += [f'{minutes} minutes']

			timespan = ', '.join(timespan)

			ans = input(f'Did you finish watching episode {show[4]}, {timespan} ago?')

			if ans.lower() in ['yes', 'y']:
				cur.execute('UPDATE shows SET state = 0, next = ? WHERE id = ?', (show[4]+1, show[0]))
				log(show[0], f'MARKED FINISHED EPISODE {show[4]}')
				print(f'Episode {show[4]} marked finished.')
				show = list(show)
				show[4]+=1
			else:
				command = '0'


		# This is the command for "I did not finish this episode"
		if command == '0':
			cur.execute('UPDATE shows SET state = 0 WHERE id = ?', (show[0],))
			log(show[0], f'DID NOT FINISH EPISODE {show[4]}')
			print(f'Episode {show[4]} marked unfinished.')
			command = ''

		# If neither, then we have a set command. In this case, the user tells us what episode is next, so this check is irrelevant.
		# Note: '+' is a set command and is equivalent to "yes, I finished it"


	runUpdate = True

	pc = command.count('+')
	command = command.replace('+', '')

	nextEp = show[4]

	if pc == 0:
		if command == '': runUpdate = False
		else: nextEp = int(command)
	elif pc == 1:
		if command == '': nextEp+=1
		else: nextEp += int(command)
	else:
		if command == '': nextEp+=pc
		else: error('Incorrect command!')

	if runUpdate:
		print(f'set to {nextEp}')
		cur.execute('UPDATE shows SET state = 0, next = ? WHERE id = ?', (nextEp, show[0]))
		log(show[0], f'JUMPED TO {nextEp}')


	if alsoOpen:
		id, name, url, state, next, padding, _, _ = show
		print(f'Opening episode {next}')
		next = str(nextEp).zfill(padding) #important: use nextEp, not next
		url = url.replace('@', str(next))

		if url.strip() != '':
			startWatching(url)
		else:
			print(f'Please open {name} episode {next}')


		cur.execute('UPDATE shows SET state = 1 WHERE id = ?', (id,))
		log(id, f"BEGAN EPISODE {next.lstrip('0')}")

def logSearch(id):
	global logsMap
	updateLogsMap()

	cur.execute('select * from logs where show = ?', (id,))
	for item in cur.fetchall():
		if item[2] == id:
			displayLog(item, logsMap)
	exit()

def addTag():
	cur.execute("SELECT * FROM shows")
	res = cur.fetchall()

	print('Which show(s) to tag?')

	shows = selectShow(res, False)

	# todo print existing tags in all shows
	# todo ask for what tags to add only once

	for show in shows:
		print(show)
		existingTags = show[6].split(',')

		newTags = input('What tags to add? ').split(',')

		tags = set(existingTags)|set(newTags)
		tags = sorted(list(tags))
		if '' in tags:
			tags.remove('')
		tags = ','.join(tags)

		print(tags)

		id = show[0]
		
		cur.execute('UPDATE shows SET tags = ? WHERE id = ?', (tags, id))
		log(id, f"SET TAGS {tags}")



def removeTag():
	cur.execute("SELECT * FROM shows")
	res = cur.fetchall()

	print('Which show(s) to untag?')

	shows = selectShow(res, False)

	for show in shows:
		print(show)
		existingTags = show[6].split(',')

		newTags = input('What tags to remove? ').split(',')

		tags = set(existingTags)-set(newTags)
		tags = sorted(list(tags))
		if '' in tags:
			tags.remove('')
		tags = ','.join(tags)

		print(tags)

		id = show[0]
		
		cur.execute('UPDATE shows SET tags = ? WHERE id = ?', (tags, id))
		log(id, f"SET TAGS {tags}")

def listTags():
	cur.execute("SELECT distinct tags FROM shows")
	res = cur.fetchall()
	res = [x[0].split(',') for x in res]

	res = [item for sublist in res for item in sublist]

	if '' in res:
		res.remove('')

	print(','.join(res))


def searchByTag():
	print('Available tags:')
	listTags()

	tag = input('Tag to search for: ')

	cur.execute("SELECT * FROM shows WHERE tags LIKE ?", (f'%{tag}%',))
	res = cur.fetchall()

	for item in res:
		displayShow(item)




def changeReference():
	cur.execute("SELECT * FROM shows")
	res = cur.fetchall()

	print('Which show to change?')

	showC = selectShow(res, True)[0]

	print('Which show to reference?')

	showR = selectShow(res, True)[0]

	isRewatch = input('Is this a new season (0) or rewatch (1)? ').strip() == '1'

	c = showC[0]
	r = showR[0]

	if isRewatch:
		r = -r

	print(f'{c} -> {r}')
	cur.execute('UPDATE shows SET reference = ? WHERE id = ?', (r, c))
	log(c, f"SET REFERENCE {r}")

