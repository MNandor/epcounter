#!/bin/python3

import sqlite3
import time
from printing import displayShow, displayLog, error

# Todo use $HOME instead for file location
con = sqlite3.connect('Epcounter.db')
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
		tags TEXT,
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




# Show all shows actively being watched
def listShows():
	cur.execute('select * from shows where state = 0 or state = 1')

	res = cur.fetchall()
	for item in res:
		displayShow(item)


# Same as list except doesn't hide inactive shows
def allShows():
	cur.execute('select * from shows')

	res = cur.fetchall()
	for item in res:
		displayShow(item)

	exit()

# used to map ids to names
logsMap = None
def logs():
	global logsMap
	if logsMap == None:
		cur.execute('select id, name from shows')
		res = cur.fetchall()
		logsMap = {x[0]:x[1] for x in res}


	cur.execute('select * from logs')

	res = cur.fetchall()
	for item in res:
		displayLog(item, logsMap)
