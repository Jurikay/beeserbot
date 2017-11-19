#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# by Jurek Baumann

"""Functions related to buy / sell decision logic."""

# import botFunctions

import threading
from binance.enums import *
from binance.client import Client
from config import api_key, api_secret, symbol


from customSocketManager import BinanceSocketManager
# import ui

def getCurrentPrices():
    """Fetch bid and ask price and quantitiy of every coin. Access data this way: priceList["BNBBTC"]["askPrice"].

    Available values:
    'bidPrice', 'bidQty', 'askPrice', 'askQty'

    """
    priceList = dict()

    # API Call:
    currentPrices = client.get_orderbook_tickers()
    for index in enumerate(currentPrices):
        if "BTC" in currentPrices[index[0]]["symbol"] and "USDT" not in currentPrices[index[0]]["symbol"]:
            priceList[currentPrices[index[0]]["symbol"]] = currentPrices[index[0]]


    return priceList


# use val to store different values like websocket conn_keys
val = {"s": 0, "cs": 0, "socket1": 0, "socket2": 0, "socket3": 0, "symbol": symbol, "iter1": 0, "bm": 0, "tryToBuy": False, "tryToSell": False}


client = Client(api_key, api_secret)

val["bm"] = BinanceSocketManager(client)
val["exitThread"] = False
val["priceList"] = getCurrentPrices()
val["symbol"] = symbol
val["buyLoop"] = True

# DEBUG hardcode symbol
# symbol = 'ETHBTC'

# initilize "global" dictionaries
depthMsg = dict()
tradesMsg = dict()
tickerMsg = dict()
userMsg = dict()
globalList = list()
tradeHistDict = dict()
accHoldings = dict()

lock = threading.RLock()




def botCalc():
    """Fire this every time the orderbook is updated."""
    # logging.debug("bot calculations " + str(depthMsg["bids"][0]))


    pass
# app = ui.MainApp()
