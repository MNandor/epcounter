#!/bin/python3

def displayShow(item):
	id, name, url, state, next, padding, _, _ = item
	state = {0:'watching', 1:'ep began', 2:'finished', 3:'to watch', 4:'maybetry'}[state]
	#if len(name) > 30: name = name[:28]+'..'
	if len(url) > 15: url = url[:13]+'..'

	#name = name.ljust(30, ' ')
	url = url.ljust(15, ' ')

	id = str(id).rjust(3, ' ')

	print(f'{id}: [{state}] /{url}/{padding}/ N:{next} {name}')

