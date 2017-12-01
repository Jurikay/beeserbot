#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# by Jurek Baumann

"""Functions related to buy / sell decision logic."""

# import botFunctions
import threading
import logging
import datetime
from binance.enums import *
from binance.client import Client
from binance.exceptions import BinanceAPIException
from customSocketManager import BinanceSocketManager

# from customSocketManager import BinanceSocketManager

try:
    from config import api_key, api_secret, symbol, buy_size, sell_size
except ModuleNotFoundError:
    print("Paste Your API key and secret into config_sample.py and rename it to config.py!")

logging.basicConfig(filename="test.log", filemode='w', level=logging.DEBUG, format='%(asctime)s %(message)s')


# class MySocketManager(BinanceSocketManager):
#
#     _user_timeout = 50 * 60  # 50 minutes
#
#     def __init__(self, client):
#         """Initialise the BinanceSocketManager
#
#         :param client: Binance API client
#         :type client: binance.Client
#
#         """
#         threading.Thread.__init__(self)
#         self._conns = {}
#         self._user_timer = None
#         self._user_listen_key = None
#         self._client = client
#         self.daemon = True
#

# use val to store different values like websocket conn_keys
val = {"s": 0, "cs": 0, "socket1": 0, "socket2": 0, "socket3": 0, "symbol": symbol, "iter1": 0, "bm": 0, "tryToBuy": False, "tryToSell": False, "runTime": 0, "newTrade": False, "restartTimer": -5}

recv_window = 6000000

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

val["accValue"] = "0000000"
# initialize "global" dictionaries
depthMsg = dict()
tradesMsg = dict()
tickerMsg = dict()
userMsg = dict()
klineMsg = dict()

globalList = list()
tradeHistDict = dict()
accHoldings = dict()
indicators = dict()

val["myOrders"] = dict()


val["angelBuyId"] = None
val["angelSellId"] = None
lock = threading.RLock()

val["amountBought"] = 0.0
val["totalCost"] = 0.0
val["avgBuyPrice"] = 0.0

# debug
val["buySize"] = buy_size
val["sellSize"] = sell_size

val["depthTracker"] = 0

filledTrades = []
reportFilename = "report-" + str(datetime.datetime.now().strftime("%m-%d-%H.%M"))


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
