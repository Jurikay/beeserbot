#!/usr/bin/env python3

# by Jurek Baumann

# API IMPLEMENTATION FROM https://github.com/sammchardy/python-binance
# DOCS: http://python-binance.readthedocs.io/en/latest/index.html
"""MAIN entrypoint of the bot."""

# IMPORTS
import splashScreen
import time
import threading
import logging

from colorSyntax import *
import ui
import TA
from botFunctions import *
from botLogic import *

# binance API
# from binance.client import Client
# from binance.websockets import BinanceSocketManager


# used to supress linter error...
logging.debug("Juris beeser Bot version " + str(splashScreen.version) + " started")

# API related variables


# main loop function

#  BOT LOGIC GOES HERE
def mainLoop():
    iterator = 0
    minuteIt = 0
    while val["exitThread"] is False:

        val["s"] += 1
        val["cs"] += 1

        try:
            ui.app.periodicUpdate()
        except KeyError:
            pass
        time.sleep(1)
        # Hard refresh Display every 15 seconds TODO: find a better way to fix display errors

        if iterator > 9:
            try:
                ui.app.hardRefresh()
                logging.debug("DISPLAY hardrefresh              ")
                iterator = 0
            except KeyError:
                pass
        else:
            iterator += 1

        if minuteIt > 10:
            val["openOrders"] = getOrders(val["symbol"])
            logging.debug("open orders: " + str(val["openOrders"]))



            # TA.createCSV()
            val["indicators"] = TA.createCSV()
            ui.app.getForm("MAIN").setBandInfo()
            minuteIt = 0
        else:
            minuteIt += 1
        # Test: running for:

        # val["timeRunning"] = str(datetime.timedelta(seconds=int(val["s"])))

        # if val["exitThread"] == True:
        #     print("exit thread")

        #
        # if val["running"] == True:
        #     try:
        #         algoLogic(depthMsg["bids"][0][0], depthMsg["asks"][0][0], val["buyTarget"], val["sellTarget"])
        #         # algoLogic2(depthMsg["bids"][0][0], depthMsg["asks"][0][0], val["buyTarget"], val["sellTarget"])
        #     except KeyError:
        #         pass
            val["initiateBuy"] = True


def secondLoop():
    logging.debug("second loop")
    while val["exitSecondThread"] is False:
        logging.debug("second loop iteration")
        if val["initiateBuy"]:
            logging.debug("ONCE PLS")
            val["initiateBuy"] = False
        if val["running"] is True:
            try:
                neueAlgoLogic(val["buyTarget"], val["sellTarget"])
                logging.debug("calle neueAlgoLogic")
            except KeyError:
                logging.debug("neue algo logic: KeyError!")

        time.sleep(0.5)

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


# def buyLoop():
#     while val["buyLoop"] is True:
#         # while val["tryToBuy"] == 1:
#         #     time.sleep(0.2)
#         #     logging.debug("trying to buy")
#
#         time.sleep(0.5)
#




if __name__ == '__main__':
    # Starting main loop in separate Thread as a deamon
    mainThread = threading.Thread(target=mainLoop, args=(), daemon=True)

    mainThread.start()

    secondThread = threading.Thread(target=secondLoop, args=(), daemon=True)

    secondThread.start()

    # buyThread = threading.Thread(target=buyLoop, args=(), daemon=True)
    #
    # buyThread.start()


    # calcThread = threading.Thread(target=calcLoop,args=(), daemon=True)

    # calcThread.start()

    val["indicators"] = TA.createCSV()

    # print(indicators["1h"]["lowerBoll"])


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
