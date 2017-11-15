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
import logging
from math import fabs,ceil,floor

# my stuff
from config import *
from colorSyntax import *
import ui
from botFunctions import *

# currently not needed
import curses
# import sys
# import os

# binance API
from binance.client import Client
from binance.websockets import BinanceSocketManager
from binance.enums import *

val["bm"] = BinanceSocketManager(client)

exitThread = False

# main loop function

#  BOT LOGIC GOES HERE
def mainLoop():
    iterator = 0
    while exitThread == False:

        val["s"] += 1
        val["cs"] += 1

        logging.debug("###EINE SEC")
        try:
            ui.app.periodicUpdate()


        except:
            pass
        time.sleep(1)
        # Hard refresh Display every 15 seconds TODO: find a better way to fix display errors

        if iterator >= 15:
            try:
                ui.app.hardRefresh()
                logging.debug("DISPLAY hardrefresh              ")
                iterator = 0
            except:
                pass
        else:
            iterator += 1



        # Test: running for:

        # val["timeRunning"] = str(datetime.timedelta(seconds=int(val["s"])))

        # if exitThread == True:
        #     print("exit thread")


# def calcLoop():
#     loadingList = ["▁", "▂", "▃", "▄", "▅", "▆", "▇", "█", "▇", "▆", "▅", "▄", "▃"]
#     iterator = 0
#
#     while iterator <= len(loadingList):
#         try:
#             ui.app.setStatus("neuer statusLOL",loadingList[int(iterator)])
#             iterator +=1
#         except:
#             pass
#
#     time.sleep(0.2)
#
#     iterator = 0




# Start npyscreen. Everything after this will be triggered on exit (ESC)
if __name__ == '__main__':
    # Starting main loop in separate Thread as a deamon
    mainThread = threading.Thread(target=mainLoop,args=(), daemon=True)

    mainThread.start()

    # calcThread = threading.Thread(target=calcLoop,args=(), daemon=True)

    # calcThread.start()

    # (re)start webSocket connections
    restartSocket(symbol)
    logging.debug("ONCE")

    # start the websocket manager
    val["bm"].start()

    # start npyscreen ui

    ui.app.run()
