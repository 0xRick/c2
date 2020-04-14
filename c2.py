#!/usr/bin/python3 

import sys
import logging
import os

sys.path.append("./core")

from menu import *

def main():

	if os.path.exists("./data/") == False:
		os.mkdir("./data/")

	if os.path.exists("./data/listeners/") == False:
		os.mkdir("./data/listeners/")

	if os.path.exists("./data/databases/") == False:
		os.mkdir("./data/databases/")

	log = logging.getLogger('werkzeug')
	log.disabled = True

	loadListeners()
	uagents()
	
	home()

if __name__ == "__main__":
    main()