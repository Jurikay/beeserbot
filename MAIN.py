#!/usr/bin/env python3

# by Jurek Baumann

# API IMPLEMENTATION FROM https://github.com/sammchardy/python-binance
# DOCS: http://python-binance.readthedocs.io/en/latest/index.html
'''
MAIN entrypoint of the bot
'''

version = "1.02"



print("""
                    \033[94m__         _       __\033[93m
                \033[94m__ / /_ ______(_)__   / /_ ___ ___ ___ ___ ___ ____\033[93m
/$$$$$$$  /$$  \033[94m/ // / // / __/ (_-<  / _  / -_) -_) -_|_-</ -_) __/\033[93m    /$$$$$$$              /$$
| $$__  $$|__/ \033[94m\___/\_,_/_/ /_/___/ /_.__/\__/\__/\__/___/\__/_/\033[93m      | $$__  $$            | $$
| $$  \ $$ /$$ /$$$$$$$   /$$$$$$  /$$$$$$$   /$$$$$$$  /$$$$$$       | $$  \ $$  /$$$$$$  /$$$$$$
| $$$$$$$ | $$| $$__  $$ |____  $$| $$__  $$ /$$_____/ /$$__  $$      | $$$$$$$  /$$__  $$|_  $$_/
| $$__  $$| $$| $$  \ $$  /$$$$$$$| $$  \ $$| $$      | $$$$$$$$      | $$__  $$| $$  \ $$  | $$
| $$  \ $$| $$| $$  | $$ /$$__  $$| $$  | $$| $$      | $$_____/      | $$  \ $$| $$  | $$  | $$ /$$
| $$$$$$$/| $$| $$  | $$|  $$$$$$$| $$  | $$|  $$$$$$$|  $$$$$$$      | $$$$$$$/|  $$$$$$/  |  $$$$/
|_______/ |__/|__/  |__/ \_______/|__/  |__/ \_______/ \_______/      |_______/  \______/    \___/""")

print(" Version\033[0m " + str(version) + "\033[93m – https://github.com/Jurikay/beeserbot\033[0m")
print("")
print("starting engines... Please stand by..")

# IMPORTS

import time
import threading
import logging

from colorSyntax import *
import ui
from botFunctions import *

# binance API
from binance.client import Client
# from binance.websockets import BinanceSocketManager
from binance.enums import *

from customSocketManager import BinanceSocketManager

# API related variables
val["bm"] = BinanceSocketManager(client)
val["exitThread"] = False
val["priceList"] = getCurrentPrices()


# main loop function

#  BOT LOGIC GOES HERE
def mainLoop():
    iterator = 0
    while val["exitThread"] is False:

        val["s"] += 1
        val["cs"] += 1

        logging.debug("###EINE SEC")
        try:
            ui.app.periodicUpdate()
        except KeyError:
            pass
        time.sleep(1)
        # Hard refresh Display every 15 seconds TODO: find a better way to fix display errors

        if iterator >= 10:
            try:
                ui.app.hardRefresh()
                logging.debug("DISPLAY hardrefresh              ")
                iterator = 0
            except KeyError:
                pass
        else:
            iterator += 1
        # Test: running for:

        # val["timeRunning"] = str(datetime.timedelta(seconds=int(val["s"])))

        # if val["exitThread"] == True:
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
    mainThread = threading.Thread(target=mainLoop, args=(), daemon=True)

    mainThread.start()

    # calcThread = threading.Thread(target=calcLoop,args=(), daemon=True)

    # calcThread.start()

    # (re)start webSocket connections
    restartSocket(symbol)
    logging.debug("ONCE")

    # start the websocket manager
    val["bm"].start()

    # start npyscreen ui
    fillList(val["symbol"])
    try:
        ui.app.run()
    except npyscreen.wgwidget.NotEnoughSpaceForWidget:
        print("\033[91mWindow too small")
