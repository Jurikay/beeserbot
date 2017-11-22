#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# by Jurek Baumann

"""Functions related to buy / sell decision logic."""

# import botFunctions
import threading
import logging
from binance.enums import *
from binance.client import Client
from binance.exceptions import BinanceAPIException
from customSocketManager import BinanceSocketManager

try:
    from config import api_key, api_secret, symbol
except ModuleNotFoundError:
    print("Paste Your API key and secret into config_sample.py and rename it to config.py!")

logging.basicConfig(filename="test.log", filemode='w', level=logging.DEBUG, format='%(asctime)s %(message)s')


# use val to store different values like websocket conn_keys
val = {"s": 0, "cs": 0, "socket1": 0, "socket2": 0, "socket3": 0, "symbol": symbol, "iter1": 0, "bm": 0, "tryToBuy": False, "tryToSell": False, "runTime": 0}


client = Client(api_key, api_secret)

val["bm"] = BinanceSocketManager(client)
val["exitThread"] = False
val["exitSecondThread"] = False
val["symbol"] = symbol
val["buyLoop"] = True
val["indicators"] = dict()

val["running"] = False
val["openOrders"] = dict()
# DEBUG hardcode symbol
# symbol = 'ETHBTC'
val["initiateBuy"] = False
# initilize "global" dictionaries
depthMsg = dict()
tradesMsg = dict()
tickerMsg = dict()
userMsg = dict()
globalList = list()
tradeHistDict = dict()
accHoldings = dict()
indicators = dict()

val["myOrders"] = dict()


val["angelBuyId"] = None
val["angelSellId"] = None
lock = threading.RLock()

#debug
val["buySize"] = 20
val["sellSize"] = 25

val["depthTracker"] = 0


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

val["priceList"] = getCurrentPrices()
