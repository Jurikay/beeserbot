#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# by Jurek Baumann
"""API/ calculation functions."""

# IMPORTS

import time
# from math import fabs,ceil,floor

# import os
import atexit
import logging
from math import ceil
# currently not needed

# import sys
# import os

from botLogic import *
import ui


# from binance.websockets import BinanceSocketManager
from binance.enums import *

from twisted.internet.error import ReactorNotRunning




def cleanExit():
    """Stop threads, npyscreen and the socket manager before exiting."""
    # Shutting down nicely
    print("     Shutting down...                  ")

    # trigger while loop to val["exitThread"]
    val["exitThread"] = True

    try:
        val["bm"].close()
        logging.debug("CLOSING MANAGER")
    except ReactorNotRunning as e:
        logging.debug("Error while closing socket manager: " + str(e))


def exit_handler():
    """Handle exit gracefully."""
    try:
        ui.app.switchForm(None)
    except AttributeError:
        pass
    print("\033c")
    print('🚫  Bot has shut down.')
    # closeAllOrders()


atexit.register(exit_handler)


client = Client(api_key, api_secret)


def availablePairs():
    """
    Create a dictonary containing all BTC tradepairs excluding USDT.

    Keys are:
    {'symbol': 'ETHBTC', 'tradedMoney': 3024.89552855, 'baseAssetUnit': 'Ξ', 'active': True, 'minTrade': '0.00100000', 'baseAsset': 'ETH', 'activeSell': 66254.102, 'withdrawFee': '0', 'tickSize': '0.000001', 'prevClose': 0.044214, 'activeBuy': 0, 'volume': '66254.102000', 'high': '0.047998', 'lastAggTradeId': 2809764, 'decimalPlaces': 8, 'low': '0.043997', 'quoteAssetUnit': '฿', 'matchingUnitType': 'STANDARD', 'close': '0.047656', 'quoteAsset': 'BTC', 'open': '0.044214', 'status': 'TRADING', 'minQty': '1E-8'}
    """
    # create a local dictionary
    coins = dict()

    # API Call
    products = client.get_products()

    # For every entry in API answer:
    for i in range(len(products["data"])):

        # Check if pair contains BTC, does not contain USDT and if volume is >0
        if "BTC" in products["data"][i]["symbol"] and "USDT" not in products["data"][i]["symbol"] and float(products["data"][i]["volume"]) > 0.0:
            # Create a temporary dictionary to store keys and values
            tempdict = dict()

            # Add every key-value pair to the temp dictionary
            for key, value in products["data"][i].items():
                tempdict[key] = value
            # Add every temp dictionary to the coin dictionary
            coins[tempdict["symbol"]] = tempdict
    # return the newly created coin dictionary

    # with open("coins.txt", "w") as f:
    #         f.write(str(coins))
    return coins


# unused; TODO refactor
def amountNumbers(bidAsk):
    """Calculate the amount of numbers needed to properly display the order size."""
    bidAmount = list()
    try:
        for i in range(len(depthMsg[bidAsk])):
            bidAmount.append(int(float(depthMsg[bidAsk][i][1])))
    except KeyError:
        pass
    # maxBidA = max(bidAmount)
    return bidAmount
    # time.sleep(0.1)
    # os._exit(0)
    # cleanly exit


def fetchAsap(symbol):
    """Make a seperate API call to instantly get new ticker values after changing the coin."""
    tickers = client.get_ticker(symbol=symbol)
    tempDict = dict()
    iterator = 0
    symbolList = ["p", "P", "w", "x", "c", "Q", "b", "B", "a", "A", "o", "h", "l", "v", "q", "O", "C", "F", "L", "n"]

    tempDict["s"] = symbol
    for value in tickers.items():
        # print(str(key) + "  " + str(value))
        tempDict[symbolList[iterator]] = value
        iterator += 1

    return tempDict


def fetchDepth(symbol):
    """Make a seperate API call to instantly get new orderbook values after changing the coin."""
    logging.debug("FETCHE DEPTH!!")
    depth = client.get_order_book(symbol=symbol)
    for key, value in depth.items():
        depthMsg[key] = value
    depthMsg["lastUpdateId"] = "WAITING"


def fillList(symbol):
    """Make a seperate API call to instantly get the trade history after changing the coin."""
    logging.debug("FILL LIST CALLED")

    # API Call
    trades = client.get_aggregate_trades(symbol=symbol, limit=15)

    for i in range(15):
        globalList.insert(0, {"price": str(trades[i]["p"]), "quantity": str(trades[i]["q"]), "order": str(trades[i]["m"]), "timestamp": str(trades[i]["T"])})


def getHoldings():
    """Make an inital API call to get BTC and coin holdings."""
    # API Call:
    order = client.get_account()

    for i in range(len(order["balances"])):
        accHoldings[order["balances"][i]["asset"]] = {"free": order["balances"][i]["free"], "locked": order["balances"][i]["locked"]}

    return accHoldings




def restartSocket(symbol):
    """Check if websocket connections are open, closeses them and starts new ones based on the given symbol."""
    logging.debug("RESTART SOCKET")


    # tickerMsg = fetchAsap(symbol)

    # bm = BinanceSocketManager(client)
    with lock:
        if val["socket1"] != 0:
            val["bm"].stop_socket(val["socket1"])
            val["bm"].stop_socket(val["socket2"])
            val["bm"].stop_socket(val["socket3"])
            val["bm"].stop_socket(val["socket4"])

            logging.debug("SOCKETS CLOSED")
            # time.sleep(1)

        else:
            logging.debug("KONNTE SOCKETS NICHT BEENDEN!!!")

        # FIXME would be nice to remove
        time.sleep(0.1)

        # tradesMsg.clear()
        val["socket1"] = val["bm"].start_depth_socket(symbol, depth_callback, depth=10, update_time="0ms")
        val["socket2"] = val["bm"].start_trade_socket(symbol, trade_callback)
        val["socket3"] = val["bm"].start_ticker_socket(ticker_callback, update_time="0ms")
        val["socket4"] = val["bm"].start_user_socket(user_callback)
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
    # run certain logic everytime an order is placed
    botCalc()
    # MainForm.updateOrderbook()

    # draw orderbook changes right as they are received
    ui.app.updateDepth()

    # with open("depthCallback.txt", "w") as f:
    #     f.write(str(depthMsg))
    if val["tryToBuy"] == 1:
        logging.debug("API BUY TRIGGER")


def trade_callback(msg):
    # print("\033[91mtrade update:")
    # print(msg)
    for key, value in msg.items():
        tradesMsg[key] = value

    # add last trade to the front of globalList
    globalList.insert(0, {"price": str(tradesMsg["p"]), "quantity": str(tradesMsg["q"]), "order": str(tradesMsg["m"])})

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
    # with open("tradeCallback.txt", "w") as f:
    #     f.write(str(tradesMsg))


def ticker_callback(msg):
    # print("\033[92mticker update:")
    # print(msg)
    if msg[0]["s"] == val["symbol"]:

        for key, value in msg[0].items():
            tickerMsg[key] = value
        # with open("tickerCallback.txt", "w") as f:
        #     f.write(str(tickerMsg))


def user_callback(msg):
    # iterate through callback
    for key, value in msg.items():
        userMsg[key] = value

    # if callback message contains account info:
    if userMsg["e"] == "outboundAccountInfo":
        for i in range(len(userMsg["B"])):

            # put account info in accHoldings dictionary. Access free and locked holdings like so: accHoldings["BTC"]["free"]
            accHoldings[userMsg["B"][i]["a"]] = {"free": userMsg["B"][i]["f"], "locked": userMsg["B"][i]["l"]}




    else:
        print("order created/filled/deleted")


###################################################
# VALIDATION
##################################################
def isfloat(value):
    """Check if a value is convertable to float. Be aware of 'NaN', '-inf', 'infinity', 'True' etc.

    https://stackoverflow.com/questions/736043/checking-if-a-string-can-be-converted-to-float-in-python
    """
    try:
        float(value)
        return True

    except ValueError:
        return False


def validateOrderPrice(priceTarget, currentBid, currentAsk, order):
    """Check if entered buy price is reasonable.

    Returns "PERFECT", "GOOD", "OK" or "BAD" depending on evaluation

    """
    if isfloat(priceTarget):
        if order == "BUY":
            if float(priceTarget) > float(currentBid) and float(priceTarget) < float(currentAsk):
                return "PERFECT"
            elif float(priceTarget) > float(currentBid) * 0.9 and float(priceTarget) < float(currentAsk):
                    return "GOOD"
            elif float(priceTarget) > float(currentBid) * 0.75 and float(priceTarget) < float(currentAsk) * 1.05:
                    return "OK"
            else:
                return "BAD"

        elif order == "SELL":
            if float(priceTarget) > float(currentBid) and float(priceTarget) < float(currentAsk):
                return "PERFECT"
            else:
                return "OK"

        else:
            return "BAD"

    else:
        return "BAD"


def calculateMinOrderSize(symbol, priceList):
    """Calculate the lowest possible buy order size."""
    # Define variables for better overview
    MIN_AMOUNT = 0.001

    currentBid = priceList[symbol]["bidPrice"]
    # currentAsk = priceList[symbol]["askPrice"]

    minTrade = float(val["coins"][symbol]["minTrade"])
    roundTo = len(str(minTrade))-2

    ticksize = str(val["coins"][symbol]["tickSize"])

    # smallestUnit = float(val["coins"]["ETHBTC"]["minQty"])

    if minTrade == 1:

        minSellOrderSize = ceil(MIN_AMOUNT / (float(currentBid) + float(ticksize)))
        # print("current bid: " + str(currentBid) + " ticksize: " + str(ticksize) + "minTrade: " + str(minTrade))
        return minSellOrderSize
    else:
        minSellOrderSize = round(MIN_AMOUNT / (float(currentBid) + float(ticksize)), roundTo)
        return round(minSellOrderSize, roundTo)


def calculateMaxOrderSize(symbol, priceList, btcBalance):
    """Calculate the maximum possible order size (dependant on btc balance).

    discard (not round decimal places):
    https://stackoverflow.com/questions/17264733/remove-decimal-places-to-certain-digits-without-rounding

    maximum coin sell size = coin balance
    """
    minTrade = float(val["coins"][symbol]["minTrade"])
    roundTo = len(str(minTrade))-2

    currentBid = priceList[symbol]["bidPrice"]
    ticksize = str(val["coins"][symbol]["tickSize"])
    # roundToBtc = len(str(ticksize))-2

    maxSize = float(btcBalance) / (float(currentBid) + float(ticksize))

    if minTrade == 1:
        maxSizeRounded = int(maxSize)

    else:
        maxSizeRounded = int(maxSize * 10**roundTo) / 10.0**roundTo

    return maxSizeRounded


def validateOrderSize(size, symbol, priceList, btcBalance):
    minSize = calculateMinOrderSize(symbol, priceList)
    maxSize = calculateMaxOrderSize(symbol, priceList, btcBalance)
    if isfloat(size):
        if float(size) >= minSize and float(size) <= maxSize:
            return "GOOD"
        elif float(size) >= minSize:
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


val["coins"] = dict()


val["coins"] = availablePairs()
