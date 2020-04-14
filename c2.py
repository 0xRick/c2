#!/usr/bin/python3 

import sys
import logging

sys.path.append("./core")

from menu import *

def main():

    log = logging.getLogger('werkzeug')
    log.disabled = True

    loadListeners()
    uagents()

    home()

if __name__ == "__main__":
    main()