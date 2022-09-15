#!/bin/python3

import webbrowser
import subprocess

# finished watching, but still want to listen to songs?
def seekOpenings(title):
	webbrowser.open('https://www.youtube.com/results?search_query='+title+'+opening')

def startWatching(link):
	if link.startswith('https://') or link.startswith('www.'):
		webbrowser.open(link)
	elif link.startswith('/') or link.startswith('~/'):
		# todo not hardcode vlc
		file = f'vlc "{link}"*'
		# todo remove arbitrary code execution vulnerability
		subprocess.Popen(['bash', '-c', file])
	else:
		# todo there's probably still a way to guess
		print('>>>'+link)
