#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# by Jurek Baumann

# IMPORTS
import npyscreen
import datetime
import time
import threading
from math import fabs,ceil,floor

import os

import logging
# currently not needed
import curses
# import sys
# import os

from config import *
from botLogic import *

from binance.client import Client
from binance.websockets import BinanceSocketManager
from binance.enums import *

import atexit
def exit_handler():
    '''
    Handle exit gracefully
    '''
    cleanExit()
    print ('🚫  Bot wurde beendet.')
    # closeAllOrders()

atexit.register(exit_handler)

client = Client(api_key, api_secret)

def availablePairs():

    # API related variables



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

    with lock:
        try:
            val["bm"].close()
            logging.debug("CLOSING MANAGER")
        except:
            pass

    time.sleep(0.1)
    os._exit(0)
    # cleanly exit

def fetchAsap(symbol):
    '''
    Make a seperate API call to instantly get new ticker values after changing the coin.
    '''
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


def fetchDepth(symbol):
    '''
    Make a seperate API call to instantly get new orderbook values after changing the coin.
    '''
    logging.debug("FETCHE DEPTH!!")
    depth = client.get_order_book(symbol=symbol)
    for key,value in depth.items():
        depthMsg[key] = value
    depthMsg["lastUpdateId"] = "WAITING"

def fillList(symbol):
    '''
    Make a seperate API call to instantly get the trade history after changing the coin.
    '''
    logging.debug("FILL LIST CALLED")

    # API Call
    trades = client.get_aggregate_trades(symbol=symbol, limit=15)

    for i in range(15):
        globalList.insert(0,{"price": str(trades[i]["p"]), "quantity": str(trades[i]["q"]), "order": str(trades[i]["m"]),
        "timestamp": str(trades[i]["T"])
        })




def restartSocket(symbol):
    logging.debug("RESTART SOCKET")


    # tickerMsg = fetchAsap(symbol)
    client = Client(api_key, api_secret)
    # bm = BinanceSocketManager(client)
    with lock:
        if val["socket1"] != 0:
            val["bm"].stop_socket(val["socket1"])
            val["bm"].stop_socket(val["socket2"])
            val["bm"].stop_socket(val["socket3"])
            logging.debug("SOCKETS CLOSED")
            # time.sleep(1)

        else:
            logging.debug("KONNTE SOCKETS NICHT BEENDEN!!!")
            pass

        # FIXME would be nice to remove
        # time.sleep(.1)

        # tradesMsg.clear()
        val["socket1"] = val["bm"].start_depth_socket(symbol, depth_callback, depth=10, update_time="0ms")
        val["socket2"] = val["bm"].start_trade_socket(symbol, trade_callback)
        val["socket3"] = val["bm"].start_ticker_socket(ticker_callback, update_time="0ms")
        logging.debug("SOCKETS OPENED")

######################################################
# WebSocket Callback functions
######################################################
def depth_callback(msg):
    # logging.debug("BID: " + str(msg["bids"][0][0]))
    # logging.debug("ASK: " + str(msg["asks"][0][0]))

    # depthMsg.clear()
    # depthMsg=dict()
    # assign values from callback to global dictionary
    with lock:
        for key, value in msg.items():
            depthMsg[key] = value
    botCalc()
    # MainForm.updateOrderbook()

    # draw orderbook changes right as they are received
    ui.app.updateDepth()




def trade_callback(msg):
    # print ("\033[91mtrade update:")
    # print(msg)
    for key, value in msg.items():
        tradesMsg[key] = value

    # add last trade to the front of globalList
    globalList.insert(0,{"price": str(tradesMsg["p"]), "quantity": str(tradesMsg["q"]), "order": str(tradesMsg["m"])})

    # if globalList has more than 15 elements, remove all above
    if len(globalList) >= 15:
        logging.debug("REDUCE LIST!!")
        del globalList[15:len(globalList)]
    # try:
    #     globalList = globalList[-5:]
    #     logging.debug("REDUCE LIST")
    # except:
    #     logging.debug("KONNTE GLOBAL LIST NICHT SCHRUMPFEN")
    logging.debug("Global list: " + str(globalList))


def ticker_callback(msg):
    # print ("\033[92mticker update:")
    # print(msg)
    if msg[0]["s"] == val["symbol"]:

        for key, value in msg[0].items():
            tickerMsg[key] = value
        # with open("myfile.txt", "w") as f:
        #     f.write(str(tickerMsg))


###################################################
# VALIDATION
##################################################

def isfloat(value):
    '''
    Check if a value is convertable to float. Be aware of NaN, -inf, infinity, True etc.
    https://stackoverflow.com/questions/736043/checking-if-a-string-can-be-converted-to-float-in-python
    '''
    try:
        float(value)
        return True

    except ValueError:
        return False


def validateOrderPrice(priceTarget, currentBid, currentAsk, order):
    '''
    Check if entered buy price is reasonable. Returns "PERFECT", "GOOD", "OK" or "BAD" depending on evaluation
    '''

    if isfloat(priceTarget):
        if order == "BUY":
            if float(priceTarget) < float(currentBid) and float(priceTarget) > float(currentAsk):
                return "PERFECT"
            elif float(priceTarget) < float(currentBid) and float(priceTarget) > float(currentAsk) * 0.95:
                return "GOOD"
            elif float(priceTarget) < float(currentBid) * 1.05 and float(priceTarget) > float(currentAsk) * 0.8:
                return "OK"
            else:
                return "BAD"


        elif order == "SELL":
            if float(priceTarget) < float(currentAsk) and float(priceTarget) > float(currentBid):
                return "PERFECT"
            else:
                return "OK"


        else:
            return "BAD"

    else:
        return "BAD"









############
    # if order == "BUY":
    #     if isfloat(priceTarget):
    #         if float(priceTarget) < float(currentAsk):
    #             if float(priceTarget) > float(currentAsk) * 0.9:
    #                 return "GOOD"
    #             elif float(priceTarget) > float(currentAsk) * 0.8:
    #                 return "OK"
    #             else:
    #                 return "BAD"
    #         elif float(priceTarget) < float(currentAsk) * 1.05:
    #             return "OK"
    #         else:
    #             return "BAD"
    #     else:
    #         return "BAD"
    #
    # elif order == "SELL":
    #     if isfloat(priceTarget):
    #         if float(priceTarget) > float(currentAsk):
    #             if float(priceTarget) < float(currentAsk) * 0.9:
    #                 return "GOOD"
    #             elif float(priceTarget) < float(currentAsk) * 0.8:
    #                 return "OK"
    #             else:
    #                 return "BAD"
    #         elif float(priceTarget) > float(currentAsk) * 1.05:
    #             return "OK"
    #         else:
    #             return "BAD"
    #     else:
    #         return "BAD"
    #
    # else:
    #     return "BAD"


coins=dict()
coins = availablePairs()
