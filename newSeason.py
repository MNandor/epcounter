#!/bin/python3
import requests
from bs4 import BeautifulSoup
import os

source = requests.get('https://myanimelist.net/anime/season').text

soup = BeautifulSoup(source, features='html5lib')

HOME=os.path.expanduser('~')+'/.local/share/mnprograms/'


with open(HOME+'alttitles.txt') as ifs:
	searchterms = [x.strip() for x in ifs.readlines()]
	print(searchterms)


titles = soup.find_all(class_='link-title')

for n, tit in enumerate(titles):

	name = tit.contents[0]
	link = tit['href']

	findany = any([term.lower() in name.lower() for term in searchterms])
	
	if findany:
		print(f'[{n}] \033[92m{name}\033[0m')
	else:	
		print(f'[{n}] {name}')
		
