#!/usr/bin/env python3

# by Jurek Baumann

# API IMPLEMENTATION FROM https://github.com/sammchardy/python-binance
# DOCS: http://python-binance.readthedocs.io/en/latest/index.html
"""MAIN entrypoint of the bot."""

# IMPORTS
import time
import threading
import logging
import pandas as pd
import splashScreen

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
def clockLoop():
    while val["exitThread"] is False:
        try:

            ui.app.periodicUpdate()
        except KeyError:
            pass
        val["runTime"] += 1
        time.sleep(1)



def mainLoop():
    iterator = 0
    minuteIt = 0
    while val["exitThread"] is False:

        val["s"] += 1
        val["cs"] += 1

        # try:
        #     ui.app.periodicUpdate()
        # except KeyError:
        #     pass
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
            # val["openOrders"] = getOrders(val["symbol"])
            # logging.debug("open orders: " + str(val["openOrders"]))

            # debug: cancel all orders every 10 seconds to prevent multiple buy or sell orders... (WORKAROUND)
            cancelAllOrders()

            ui.app.getForm("MAIN").revalidate()




            if filledTrades and val["newTrade"]:
                quittung = (pd.DataFrame(filledTrades, columns=["date", "account value", "symbol", "price", "quantity", "side", "id"]))[::-1]

                quittung.to_csv(str(reportFilename)+".csv", index = False, encoding = 'utf-8')
                val["newTrade"] = False

            # TA.createCSV()
            val["indicators"] = TA.getTA()
            ui.app.getForm("MAIN").setIndicatorData()
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
    while val["exitSecondThread"] is False:

        if val["running"] is True:


            if isfloat(val["buyTarget"]) and isfloat(val["sellTarget"]):
                logging.debug(" BUY UND SELL TARGET VORHANDEN")
                if priceRefiner(float(val["buyTarget"]), float(val["sellTarget"])):
                    logging.debug("PRICE HAS BEEN REFINED")
                    neueAlgoLogic()
            else:
                logging.debug("buy target error: " + str(val["buyTarget"]))
        # except KeyError as err:
            #     logging.debug("neue algo logic: KeyError!")
            #     logging.debug(KeyError)
            #     logging.debug(err)
            #     logging.debug("buy target error: " + str(val["buyTarget"]) + " buy order: " + str(val["realBuyPrice"]))
            #     logging.debug("sell target error: " + str(val["sellTarget"]) + " sell order: " + str(val["realSellPrice"]))

        time.sleep(0.1)

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


    clockThread = threading.Thread(target=clockLoop, args=(), daemon=True)

    clockThread.start()

    # buyThread = threading.Thread(target=buyLoop, args=(), daemon=True)
    #
    # buyThread.start()


    # calcThread = threading.Thread(target=calcLoop,args=(), daemon=True)

    # calcThread.start()



    # print(indicators["1h"]["lowerBoll"])


    # (re)start webSocket connections
    restartSocket(symbol)
    logging.debug("ONCE")

    # start the websocket manager
    val["bm"].start()

    # get trade history
    fillList(val["symbol"])

    accHoldings = getHoldings()

    fetchDepth(val["symbol"])


    # get TA indicators
    val["indicators"] = TA.getTA()

    try:
        # start npyscreen
        ui.app.run()

    # Throw exception if window size is too small
    except npyscreen.wgwidget.NotEnoughSpaceForWidget:
        print("\033[91mWindow too small")
