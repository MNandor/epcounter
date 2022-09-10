#!/bin/python3

import sqlite3
import time

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
