#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# by Jurek Baumann
"""API/ calculation functions."""

# IMPORTS

import time
from math import fabs, ceil, floor

import copy

# import os
import atexit
import logging
import datetime
# currently not needed

# import sys
# import os

from botLogic import *  # val, Client, api_key, api_secret, lock, globalList
import ui


# from binance.websockets import BinanceSocketManager
# from binance.enums import *

from twisted.internet.error import ReactorNotRunning




def cleanExit():
    """Stop threads, npyscreen and the socket manager before exiting."""
    # Shutting down nicely
    print("     Shutting down...                  ")

    cancelAllOrders()

    # trigger while loop to val["exitThread"]
    val["exitThread"] = True
    val["exitSecondThread"] = True

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
        if "BTC" in products["data"][i]["symbol"] and not "USDT" in products["data"][i]["symbol"] and float(products["data"][i]["volume"]) > 0.0:
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


def getTotalBtc():
    """Get all coin balances and calculate total account value in BTC."""

    btcValues = []

    for index in enumerate(accHoldings):
        coinQuant = "{:.8f}".format(float(accHoldings[index[1]]["free"]) + float(accHoldings[index[1]]["locked"]))

        if float(coinQuant) > 0:
            if index[1] != "BTC" and index[1] != "USDT":
                btcValues.append(float(coinQuant) * float(val["coins"][index[1] + "BTC"]["close"]))
            elif index[1] == "BTC":
                btcValues.append(float(coinQuant))
            elif index[1] == "USDT":
                btcValues.append(float(coinQuant) / float(val["coins"]["BTCUSDT"]["close"]))
                logging.debug("ADDE USDT: ")
                logging.debug(str(float(coinQuant)) + " and: " + str(float(val["coins"]["BTCUSDT"]["close"])))

    accValue = "{:.8f}".format(sum(btcValues))
    return accValue


def restartSocket(symbol):
    """Check if websocket connections are open, closeses them and starts new ones based on the given symbol."""
    logging.debug("RESTART SOCKET")

    # bm = BinanceSocketManager(client)
    # with lock:
    #     try:
    try:
        val["bm"].stop_socket(val["socket1"])
        val["bm"].stop_socket(val["socket2"])
        val["bm"].stop_socket(val["socket3"])
        val["bm"].stop_socket(val["socket5"])
    except KeyError:
        pass
        # logging.debug("SOCKETS CLOSED")
        # time.sleep(1)

    # except Exception as e:
    #     logging.debug("COULD NOT CLOSE SOCKETS")
    #     logging.debug(str(e))
    #     logging.debug

    # FIXME would be nice to remove
    # time.sleep(0.1)

# tradesMsg.clear()
    val["socket1"] = val["bm"].start_depth_socket(symbol, depth_callback, depth=20)
    val["socket2"] = val["bm"].start_trade_socket(symbol, trade_callback)
    val["socket3"] = val["bm"].start_ticker_socket(ticker_callback)
    val["socket5"] = val["bm"].start_kline_socket(symbol, kline_callback)
    logging.debug("SOCKETS OPENED")


######################################################
# WebSocket Callback functions
######################################################
def depth_callback(msg):

    # assign values from callback to global dictionary
    with lock:
        for key, value in msg.items():
            depthMsg[key] = value

    # run certain logic everytime an order is placed
    # botCalc()

    # MainForm.updateOrderbook()

    # count number of order updates
    val["depthTracker"] += 1


    # draw orderbook changes right as they are received
    # ui.app.getForm("MAIN").update_order_book()
    # ui.app.updateDepth()
    # try:
    ui.app.forward_update()
    # except:
    #     print("EXCEPT!")
    # priceRefiner()
    val["currentGains"] = calculatePercent(float(depthMsg["asks"][0][0]) - float(val["coins"][val["symbol"]]["tickSize"]), float(val["avgBuyPrice"]))


def trade_callback(msg):
    # print("\033[91mtrade update:")
    # print(msg)
    for key, value in msg.items():
        tradesMsg[key] = value

    # add last trade to the front of globalList
    globalList.insert(0, {"price": str(tradesMsg["p"]), "quantity": str(tradesMsg["q"]), "order": str(tradesMsg["m"])})

    # if globalList has more than 15 elements, remove all above
    if len(globalList) >= 15:
        # logging.debug("REDUCE LIST!!")
        del globalList[15:len(globalList)]
    # try:
    #     globalList = globalList[-5:]
    #     logging.debug("REDUCE LIST")
    # except:
    #     logging.debug("KONNTE GLOBAL LIST NICHT SCHRUMPFEN")
    # logging.debug("Global list: " + str(globalList))
    # with open("tradeCallback.txt", "w") as f:
    #     f.write(str(tradesMsg))


def ticker_callback(msg):
    # print("\033[92mticker update:")
    # print(msg)
    if msg[0]["s"] == val["symbol"]:

        for key, value in msg[0].items():
            tickerMsg[key] = value



def user_callback(msg):
    # iterate through callback
    for key, value in msg.items():
        userMsg[key] = value

    # if callback message contains account info:
    if userMsg["e"] == "outboundAccountInfo":
        for i in range(len(userMsg["B"])):

            # put account info in accHoldings dictionary. Access free and locked holdings like so: accHoldings["BTC"]["free"]
            accHoldings[userMsg["B"][i]["a"]] = {"free": userMsg["B"][i]["f"], "locked": userMsg["B"][i]["l"]}

    elif userMsg["e"] == "executionReport":
        if userMsg["X"] == "NEW":
            val["myOrders"][userMsg["i"]] = {"symbol": userMsg["s"], "price": userMsg["p"], "quantity": userMsg["q"], "side": userMsg["S"], "id": userMsg["i"]}

        elif userMsg["X"] == "CANCELED":
            val["myOrders"].pop(userMsg["i"], None)
            if val["angelSellId"] == userMsg["i"]:
                val["angelSellId"] = None

        elif userMsg["X"] == "FILLED":
            val["myOrders"].pop(userMsg["i"], None)
            val["newTrade"] = True

            # store filled trades

            filledTrades.append({"date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "symbol": userMsg["s"], "price": userMsg["p"], "quantity": userMsg["q"], "side": userMsg["S"], "id": userMsg["i"], "account value": str(getTotalBtc())})

            if val["angelBuyId"] == userMsg["i"]:
                val["angelBuyId"] = None

            # calculate weighted average buy price
            val["avgBuyPrice"] = calculateAvgPrice(userMsg["S"], userMsg["q"], userMsg["p"])


    else:
        print("order created/filled/deleted")


def kline_callback(msg):
    for key, value in msg.items():
        klineMsg[key] = value
    with open("klineCallback.txt", "w") as f:
        f.write(str(klineMsg))


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

    except (ValueError, TypeError):
        return False


# TODO refactor
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

            return "BAD"

        elif order == "SELL":
            if float(priceTarget) > float(currentBid) and float(priceTarget) < float(currentAsk):
                return "PERFECT"

            return "OK"
    return "BAD"


def calculateMinOrderSize(symbol, priceList):
    """Calculate the lowest possible buy order size."""
    # Define variables for better overview
    MIN_AMOUNT = 0.001

    currentBid = priceList[symbol]["bidPrice"]
    # currentAsk = priceList[symbol]["askPrice"]

    minTrade = float(val["coins"][symbol]["minTrade"])
    roundTo = len(str(minTrade).rstrip("0"))-2

    ticksize = str(val["coins"][symbol]["tickSize"])

    # smallestUnit = float(val["coins"]["ETHBTC"]["minQty"])

    if minTrade == 1:

        minSellOrderSize = ceil(MIN_AMOUNT / (float(currentBid) + float(ticksize)))
        # print("current bid: " + str(currentBid) + " ticksize: " + str(ticksize) + "minTrade: " + str(minTrade))
        return minSellOrderSize

    minSellOrderSize = round(MIN_AMOUNT / (float(currentBid) + float(ticksize)), roundTo)
    return round(minSellOrderSize, roundTo)


def calculateMaxOrderSize(symbol, priceList, btcBalance):
    """Calculate the maximum possible order size (dependant on btc balance).

    discard (not round decimal places):
    https://stackoverflow.com/questions/17264733/remove-decimal-places-to-certain-digits-without-rounding

    maximum coin sell size = coin balance
    """
    minTrade = float(val["coins"][symbol]["minTrade"])
    roundTo = len(str(minTrade).rstrip("0"))-2

    currentBid = priceList[symbol]["bidPrice"]
    ticksize = str(val["coins"][symbol]["tickSize"])
    # roundToBtc = len(str(ticksize))-2

    maxSize = float(btcBalance) / (float(currentBid) + float(ticksize))

    if minTrade == 1:
        maxSizeRounded = int(maxSize)

    else:
        maxSizeRounded = int(maxSize * 10**roundTo) / 10.0**roundTo

    return maxSizeRounded


# return true if two values are identical in satoshis/smallest unit
def satCheckEqual(val1, val2):
    tickSize = str(val["coins"][val["symbol"]]["tickSize"])
    return round(fabs(val1 - val2), 8) >= 0.0 and round(fabs(val1 - val2), 8) < float(tickSize)


# returns True if difference between two values is exaclty one satoshi/smallest unit
def satCheckOneDiff(val1, val2):
    tickSize = str(val["coins"][val["symbol"]]["tickSize"])
    return round(fabs(val1 - val2), 8) > 0.0 and round(fabs(val1 - val2), 8) <= float(tickSize)


# returns True if difference between two values is at least two satoshi/smallest unit
def satCheckTwoDiff(val1, val2):
    tickSize = str(val["coins"][val["symbol"]]["tickSize"])
    return round(fabs(val1 - val2), 9) >= 0.0 and round(fabs(val1 - val2), 9) > float(tickSize)



def getOrders(symbol):
    # API Call
    orders = client.get_open_orders(symbol=symbol)
    return orders


def findInOrders(side, price, size):
    for order in enumerate(val["openOrders"]):

        if order[1]["symbol"] == val["symbol"] and str(order[1]["price"]) == str(price) and float(order[1]["origQty"]) == float(size) and order[1]["side"] == side:

            return str("FOUND")

    return str("NOT FOUND")


def findInOrdersN(price):
    myOrders = copy.deepcopy(val["myOrders"])
    for index, value in myOrders.items():
        if value["symbol"] == val["symbol"] and float(value["price"]) == float(price):
            return True
    return False


def cancelOrdersOfType(symbol, orderType):
    myOrders = copy.deepcopy(val["myOrders"])
    for index, order in myOrders.items():
        logging.debug("FOUND OPEN ORDER " + str(index))
        if order["symbol"] == val["symbol"] and str(order["side"]) == orderType:
            orderID = str(order["id"])
            try:
                client.cancel_order(symbol=symbol, orderId=orderID)
            except BinanceAPIException:
                pass


def cancelAllOrders():
    myOrders = copy.deepcopy(val["myOrders"])
    for index, order in myOrders.items():
        orderID = str(order["id"])
        logging.debug("CANCELE " + str(index))
        try:
            logging.debug(" ORDER ID: " + str(orderID))
            order = client.cancel_order(symbol=val["symbol"], orderId=orderID)
        except (TypeError, BinanceAPIException):
            pass

        try:
            client.cancel_order(symbol=symbol, orderId=orderID)
        except BinanceAPIException:
            pass


def cancelOrderById(orderId):
    try:
        with lock:
            order = client.cancel_order(symbol=val["symbol"], orderId=orderId)
            return order
    except BinanceAPIException:
        pass


def createOrder(coinPair, side, price, size):
    logging.debug("###CREATING ORDER###")
    logging.debug("SIDE: " + str(side) + " price: " + str(price) + " size: " + str(size))
    if side == "BUY":
        try:
            with lock:
                order = client.order_limit_buy(
                    symbol=coinPair,
                    quantity=size,
                    price=price)
        except BinanceAPIException as apiError:
            logging.debug("create BUY order failed !!!" + str(apiError))
            logging.debug(str(price))
            logging.debug(str(size))
            return None
        return order["orderId"]

    elif side == "SELL":
        try:
            with lock:
                order = client.order_limit_sell(
                    symbol=coinPair,
                    quantity=size,
                    price=price)
        except BinanceAPIException as apiError:
            logging.debug("create SELL order failed !!!" + str(apiError))

            return None
        return order["orderId"]



def validateOrderSize(size, symbol, priceList, btcBalance):
    minSize = calculateMinOrderSize(symbol, priceList)
    maxSize = calculateMaxOrderSize(symbol, priceList, btcBalance)
    if isfloat(size):
        if float(size) >= minSize and float(size) <= maxSize:
            return "GOOD"
        elif float(size) >= minSize:
            return "OK"

    return "BAD"


def getRealOrderSize():

    minSize = calculateMinOrderSize(val["symbol"], val["priceList"])
    maxSize = calculateMaxOrderSize(val["symbol"], val["priceList"], accHoldings["BTC"]["free"])

    totalAvailable = float(accHoldings[val["symbol"][:-3]]["free"]) + float(accHoldings[val["symbol"][:-3]]["locked"])

    minTrade = float(val["coins"][symbol]["minTrade"])
    roundTo = len(str(minTrade).rstrip("0"))-2

    buySize = val["buySize"]
    sellSize = val["sellSize"]


    # if side = "SELL":
    if float(buySize) > float(maxSize):
        buySize = maxSize
    if float(buySize) < float(minSize):
        buySize = minSize

    if float(sellSize) > totalAvailable:
        logging.debug("> total")

        sellSize = totalAvailable
    if float(sellSize) < float(minSize):
        logging.debug("< minsize")

        sellSize = minSize


    if minTrade == 1:
        sellSizeRounded = int(sellSize)
        logging.debug("mintrade")
        buySizeRounded = int(buySize)

    else:
        sellSizeRounded = int(sellSize * 10**roundTo) / 10.0**roundTo
        buySizeRounded = int(maxSize * 10**roundTo) / 10.0**roundTo

    logging.debug("sell SIZE ROUNDED: " + str(sellSizeRounded))
    return (buySizeRounded, sellSizeRounded)


    # return (val["buySize"], val["sellSize"])




    # if isfloat(size):
    #     if float(size) >= minSize and float(size) <= maxSize:
    #         return "GOOD"
    #     elif float(size) >= minSize:
    #         return "OK"
    #
    # return "BAD"


def validateHoldings(side):

    # val["buySize"] = buy_size
    # val["sellSize"] = sell_size

    btc = float(accHoldings["BTC"]["free"]) + float(accHoldings["BTC"]["locked"])
    coin = float(accHoldings[val["symbol"][:-3]]["free"]) + float(accHoldings[val["symbol"][:-3]]["locked"])

    minOrder = calculateMinOrderSize(val["symbol"], val["priceList"])

    if side == "BUY":
        logging.debug("validateholdings buy: " + str(float(coin)) + " and: " + str(float(val["buySize"])))
        if float(btc) >= 0.001:
            return True

    elif side == "SELL":
        logging.debug("validateholdings sell: " + str(float(coin)) + " and: " + str(float(val["sellSize"])))
        if float(coin) >= float(val["sellSize"]):
            return True
        elif float(coin) >= float(minOrder):
            val["sellSize"] = float(coin)
            return True

    return False


# def buyLogic():
def besereLogicBuy():
    reduceGap = False
    if float(val["buySize"]) > 0:
        if val["angelBuyId"] in val["myOrders"]:
            if float(val["myOrders"][val["angelBuyId"]]["price"]) == float(val["realBuyPrice"]):
                logging.debug("trigger sat check")

                for index, value in enumerate(depthMsg["bids"]):
                    logging.debug(str(value[0]) + " " + str(index))

                    if findInOrdersN(value[0]):

                        if not satCheckTwoDiff(float(val["myOrders"][val["angelBuyId"]]["price"]), float(depthMsg["bids"][int(index)+1][0])):
                            logging.debug("SAT CHECK FALSE")
                            return
                        logging.debug("SAT CHECK TRUE")
                        reduceGap = True
                if reduceGap is False:
                    return

                logging.debug("open order not within first 20 bids.")

            with lock:
                cancelOrderById(val["angelBuyId"])

        if validateHoldings("BUY"):
            with lock:
                val["angelBuyId"] = createOrder(val["symbol"], "BUY", val["realBuyPrice"], val["buySize"])


def neueAlgoLogic():
    val["buySize"], val["sellSize"] = getRealOrderSize()
    logging.debug("BUY SIZE: " + str(val["buySize"]))
    if val["realBuyPrice"] is None or val["realSellPrice"] is None:
        return

    besereLogicBuy()
    # if float(val["buySize"]) > 0:
    #     if val["angelBuyId"] in val["myOrders"]:
    #
    #         # wenn ich schon eine habe beim aktuellen Zielpreis ist alles gut need satcheck
    #
    #         if float(val["myOrders"][val["angelBuyId"]]["price"]) == float(val["realBuyPrice"]):
    #             logging.debug("trigger sat check")
    #         else:
    #             # wenn nicht canceln und neu erstellen
    #             cancelOrderById(val["angelBuyId"])
    #
    #             if validateHoldings("BUY"):
    #                 val["angelBuyId"] = createOrder(val["symbol"], "BUY", val["realBuyPrice"], val["buySize"])
    #             else:
    #                 logging.debug("NICHT GENUG BTC ZUM SHOPPEN")
    #     else:
    #         # wenn ich noch keine offene order habe: neu erstellen
    #
    #         if validateHoldings("BUY"):
    #             val["angelBuyId"] = createOrder(val["symbol"], "BUY", val["realBuyPrice"], val["buySize"])
    #         else:
    #             logging.debug("NICHT GENUG COINS ZUM SHOPPEN")


    if float(val["sellSize"]) > 0:

        # habe ich eine offene buy order
        if val["angelSellId"] in val["myOrders"]:

            # wenn ich schon eine habe beim aktuellen Zielpreis ist alles gut
            if float(val["myOrders"][val["angelSellId"]]["price"]) == float(val["realSellPrice"]):
                logging.debug("found my order")
            else:
                logging.debug("vergleiche meine order:" + str(val["myOrders"][val["angelSellId"]]["price"]) + " und: " + str(val["realSellPrice"]))

                # wenn nicht canceln und neu erstellen
                cancelOrderById(val["angelSellId"])

                if validateHoldings("SELL"):
                    val["angelSellId"] = createOrder(val["symbol"], "SELL", val["realSellPrice"], val["sellSize"])
                else:
                    logging.debug("NICHT GENUG COINS ZUM SELLEN")
        else:
            # wenn ich noch keine offene order habe: neu erstellen

            if validateHoldings("SELL"):
                val["angelSellId"] = createOrder(val["symbol"], "SELL", val["realSellPrice"], val["sellSize"])
            else:
                logging.debug("NICHT GENUG COINS ZUM SELLEN")


def priceRefiner(buyTarget, sellTarget):

    """Be greedy and calculate how much higher or lower one can get away with while staying within targeted price range. (Dependant on current orders)."""

    # logging.debug("PRICE REFINER:")
    if isfloat(buyTarget) and isfloat(sellTarget):
        # logging.debug("buy und sell targets sind float")
        val["realBuyPrice"] = getRealBuyPrice(buyTarget)

        val["realSellPrice"] = getRealSellPrice(sellTarget)
        # logging.debug(str(val["realBuyPrice"]) + " and: " + str(val["realSellPrice"]))
        return True
    logging.debug("price refiner hat gefailed")
    return False


def getRealBuyPrice(buyTarget):
    ticksize = str(val["coins"][val["symbol"]]["tickSize"])
    roundTo = len(str(ticksize).rstrip("0"))-2
    # logging.debug("test: " + str(ticksize).rstrip("0"))
    # roundTo = len(str(float(ticksize)))
    # logging.debug("r" + str(float(ticksize)))
    # logging.debug("roudnto: " + str(roundTo))
    for index, value in enumerate(depthMsg["bids"]):
        # logging.debug(str(value[0]) + " " + str(index))
        if float(value[0]) < float(buyTarget):
            logging.debug("FOUND CHEAPER BUY ORDER")
            if findInOrdersN(value[0]):
                return str(value[0])

            if float(value[0]) + float(ticksize) <= float(buyTarget):

                realBuyPrice = "{:.8f}".format(float(value[0]) + float(ticksize))
                return str(realBuyPrice)
    realBuyPrice = "{:.8f}".format(float(buyTarget))
    return str(round(float(realBuyPrice), roundTo))


def getRealSellPrice(sellTarget):
    ticksize = str(val["coins"][symbol]["tickSize"])
    roundTo = len(str(ticksize).rstrip("0"))-2

    for index, value in enumerate(depthMsg["asks"]):
        # logging.debug("checke sell order: " + str(index) + " price: " + str(value[0]) + "soll > " + str(float(sellTarget)))
        if float(value[0]) > float(sellTarget):
            logging.debug("found more expansive oder: " + str(index) + "  price:" + str(float(value[0])))

            if findInOrdersN(value[0]):
                logging.debug("meine eigene sell order gefunden")
                return str(value[0])

                # sat check logic

            if float(value[0]) - float(ticksize) >= float(sellTarget):

                realSellPrice = "{:.8f}".format(float(value[0]) - float(ticksize))
                return str(realSellPrice)

    realSellPrice = "{:.8f}".format(float(sellTarget))
    return str(round(float(realSellPrice), roundTo))


def calculateAvgPrice(side, amount, price):
    if val["amountBought"] < 0:
        val["amountBought"] = 0
    if val["totalCost"] < 0:
        val["totalCost"] = 0

    ticksize = str(val["coins"][val["symbol"]]["tickSize"])
    roundTo = len(str(ticksize).rstrip("0"))-2

    average = val["avgBuyPrice"]

    if side == "BUY":
        val["amountBought"] += float(amount)
        val["totalCost"] += float(amount) * float(price)
        # print(str(val["totalCost"])+str(float(amount))+str(float(price)))
    elif side == "SELL":
        val["amountBought"] -= float(amount)
        val["totalCost"] -= float(amount) * float(average)

    if float(amount) > 0:
        average = float(val["totalCost"]) / float(val["amountBought"])
        averageRounded = int(average * 10**roundTo) / 10.0**roundTo
    return float(averageRounded)


def calculatePercent(value1, value2):
    if float(value1) > 0 and float(value2) > 0:
        return round(((float(value1) - float(value2)) / float(value1)) * 100, 2)
    return 0


val["coins"] = dict()

# tickerMsg = fetchAsap(val["symbol"])

val["coins"] = availablePairs()

# val["openOrders"] = getOrders(val["symbol"])
