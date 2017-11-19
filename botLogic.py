#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# by Jurek Baumann

"""Functions related to buy / sell decision logic."""

# import botFunctions

import threading

# import ui


# DEBUG hardcode symbol
symbol = 'ETHBTC'

# initilize "global" dictionaries
depthMsg = dict()
tradesMsg = dict()
tickerMsg = dict()
userMsg = dict()
globalList = list()
tradeHistDict = dict()
accHoldings = dict()

lock = threading.RLock()

# use val to store different values like websocket conn_keys
val = {"s": 0, "cs": 0, "socket1": 0, "socket2": 0, "socket3": 0, "symbol": symbol, "iter1": 0, "bm": 0, "tryToBuy": False, "tryToSell": False}



def botCalc():
    """Fire this every time the orderbook is updated."""
    # logging.debug("bot calculations " + str(depthMsg["bids"][0]))


    pass
# app = ui.MainApp()
