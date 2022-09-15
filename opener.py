#!/bin/python3

import webbrowser

# finished watching, but still want to listen to songs?
def seekOpenings(title):
	webbrowser.open('https://www.youtube.com/results?search_query='+title+'+opening')
