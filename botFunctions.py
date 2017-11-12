# IMPORTS
import npyscreen
import datetime
import time
import threading
from math import fabs,ceil,floor
from config import *

# currently not needed
import curses
# import sys
# import os

from binance.client import Client
from binance.websockets import BinanceSocketManager
from binance.enums import *


# API related variables
client = Client(api_key, api_secret)
bm = BinanceSocketManager(client)


def availablePairs():

    ''' Create a dictonary containing all BTC tradepairs excluding USDT.
        Keys are:
        {'symbol': 'ETHBTC', 'tradedMoney': 3024.89552855, 'baseAssetUnit': 'Ξ', 'active': True, 'minTrade': '0.00100000', 'baseAsset': 'ETH', 'activeSell': 66254.102, 'withdrawFee': '0', 'tickSize': '0.000001', 'prevClose': 0.044214, 'activeBuy': 0, 'volume': '66254.102000', 'high': '0.047998', 'lastAggTradeId': 2809764, 'decimalPlaces': 8, 'low': '0.043997', 'quoteAssetUnit': '฿', 'matchingUnitType': 'STANDARD', 'close': '0.047656', 'quoteAsset': 'BTC', 'open': '0.044214', 'status': 'TRADING', 'minQty': '1E-8'}
    '''
    # create a local dictionary
    coins=dict()

    # API Call
    products = client.get_products()

    # For every entry in API answer:
    for i in range(len(products["data"])):

        # Check if pair contains BTC, does not contain USDT and if volume is > 0
        if "BTC" in products["data"][i]["symbol"] and not "USDT" in products["data"][i]["symbol"] and float(products["data"][i]["volume"]) > 0.0:
            # Create a temporary dictionary to store keys and values
            tempdict=dict()

            # Add every key-value pair to the temp dictionary
            for key, value in products["data"][i].items():
                tempdict[key] = value
            # Add every temp dictionary to the coin dictionary
            coins[tempdict["symbol"]]=tempdict
    # return the newly created coin dictionary
    return coins


def amountNumbers(bidAsk):
    '''
    Calculate the amount of numbers needed to properly display the order size
    '''
    bidAmount = list()
    try:
        for i in range(len(depthMsg[bidAsk])):
            bidAmount.append(int(float(depthMsg[bidAsk][i][1])))
    except KeyError:
        pass

    maxBidA = max(bidAmount)
    return bidAmount

def cleanExit():
    # Shutting down nicely
    print("Shutting down...")

    # trigger while loop to exitThread
    exitThread = True


    # close websocket manager
    try:
        bm.close()
    except:
        pass
    # cleanly exit

def fetchAsap(symbol):
    tickers = client.get_ticker(symbol=symbol)
    tempDict = dict()
    iterator = 0
    symbolList = ["p","P","w","x","c","Q","b","B","a","A","o","h","l","v","q","O","C","F","L","n"]

    tempDict["s"] = symbol
    for key,value in tickers.items():
        # print(str(key) + "  " + str(value))
        tempDict[symbolList[iterator]] = value
        iterator += 1

    return tempDict

import atexit
def exit_handler():
    cleanExit()
    print ('🚫  Bot wurde beendet.')
    # closeAllOrders()

atexit.register(exit_handler)
