#!/bin/python3

from db import log

def error(msg):
	print(msg)
	input()
	exit()


log(1, "hi")
