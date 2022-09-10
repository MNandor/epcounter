#!/bin/python3


from datetime import datetime

def error(msg):
	print(msg)
	input()
	exit()

def displayShow(item):
	id, name, url, state, next, padding, tags, reference = item
	state = {0:'watching', 1:'ep began', 2:'finished', 3:'to watch', 4:'maybetry'}[state]
	#if len(name) > 30: name = name[:28]+'..'
	if len(url) > 15: url = url[:13]+'..'

	#name = name.ljust(30, ' ')
	url = url.ljust(15, ' ')

	id = str(id).rjust(3, ' ')

	print(f'{id}: [{state}] /{url}/{padding}/ N:{next} {name}')


def displayLog(item, logsMap):
	id, timeStamp, showID, command = item

	name = logsMap[showID]
	if len(name) > 24: name = name[:22]+'..'
	name = name.ljust(24, ' ')

	stamp = datetime.fromtimestamp(timeStamp).strftime('%b %d %H:%M')

	showID = str(showID).rjust(3, ' ')

	id = str(id).rjust(4, ' ')

	print(f'{id}: ({stamp}) {showID}/{name} {command}')

def promptShowDetails():

	name = input('Name: ')
	url = input('URL (\'@\' for the number): ')
	padding = input('Padding (default 0): ')
	state = input('State? (0=watch, 3=to watch, 4=maybe watch)')

	if state != '':
		state = int(state)
	else:
		# default value
		state = 4

	if padding.strip() == '': padding = '0'
	padding = int(padding)

	return (name, url, padding, state)
