#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# by Jurek Baumann

# API IMPLEMENTATION FROM https://github.com/sammchardy/python-binance
# DOCS: http://python-binance.readthedocs.io/en/latest/index.html
'''
MAIN entrypoint of the bot
'''

print("starting engines 🛥")

# IMPORTS

# various stuff
import npyscreen
import datetime
import time
import threading
from math import fabs,ceil,floor

# my stuff
from config import *
from colorSyntax import *
from ui import *
from botFunctions import *

# currently not needed
import curses
# import sys
# import os

# binance API
from binance.client import Client
from binance.websockets import BinanceSocketManager
from binance.enums import *


exitThread = False

# main loop function

#  BOT LOGIC GOES HERE
def mainLoop():

    while exitThread == False:

        val["s"] += 1
        val["cs"] += 1
        time.sleep(1)
        logging.debug("###EINE SEC")

        # Test: running for:

        # val["timeRunning"] = str(datetime.timedelta(seconds=int(val["s"])))

        # if exitThread == True:
        #     print("exit thread")



def calcLoop():
    # while True:
    #     logging.debug("calc bot action")
    #     time.sleep(.1)
    pass


# Start npyscreen. Everything after this will be triggered on exit (ESC)
if __name__ == '__main__':
    # Starting main loop in separate Thread as a deamon
    mainThread = threading.Thread(target=mainLoop,args=(), daemon=True)

    mainThread.start()

    calcThread = threading.Thread(target=calcLoop,args=(), daemon=True)

    calcThread.start()

    # (re)start webSocket connections
    restartSocket(symbol)
    # start the websocket manager
    bm.start()

    # start npyscreen ui

    app.run()
