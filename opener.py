#!/bin/python3

import webbrowser

# finished watching, but still want to listen to songs?
def seekOpenings(title):
	webbrowser.open('https://www.youtube.com/results?search_query='+title+'+opening')

def startWatching(link):
	# todo open in webbrowser or local file, based on pattern
	print('>>>'+link)
