#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# by Jurek Baumann

"""Used for testing only. Not part of the app."""
import threading
import time
import pandas as pd
import stockstats
import logging
logging.basicConfig(filename="test.log", level=logging.DEBUG, format='%(asctime)s %(message)s')
from MAIN import *
symbol = "QSPBTC"
#
val["symbol"] = "BNBBTC"

apiAnswer = client.get_klines(symbol="BNBBTC", interval="5m")
with open("klineanser.txt", "w") as f:
        f.write(str(apiAnswer))


debugCoins = ["BNBBTC", "ETHBTC", "NEOBTC"]
start = time.time()
timeIntervals = ["1m", "5m", "15m", "30m", "1h"]
timeFrames = []
dataTable = []
coinInfoList = []


def getInfos(coin):
    val["symbol"] = coin
    klines = []
    for index in enumerate(timeIntervals):
        i = index[0]
        klines.append([])
        filename = str(timeIntervals[i])
        klines[i] = client.get_klines(symbol=val["symbol"], interval=timeIntervals[i])

        date, amount, closeP, high, low, openP, volume = ([] for i in range(7))

        for index2 in enumerate(klines[i]):
            j = index2[0]

            date.append(int(klines[i][j][6]))
            amount.append(float(klines[i][j][7]))
            closeP.append(float(klines[i][j][4]))
            high.append(float(klines[i][j][2]))
            low.append(float(klines[i][j][3]))
            openP.append(float(klines[i][j][1]))
            volume.append(float(klines[i][j][5]))


        dataTable = {'date': date, 'amount': amount, 'close': closeP, 'high': high, 'low': low, 'open': openP, 'volume': volume}

        # Build a DataFrame 'coinDataFrame' from the dict dataTable
        coinDataFrame = pd.DataFrame(dataTable, columns=['date', 'amount', 'close', 'high', 'low', 'open', 'volume'])

        # debug
        # coinDataFrame[j].to_csv("test_" + str(filename) + '.csv')
        stock = stockstats.StockDataFrame.retype(coinDataFrame)

        print(stock.iloc[0][0])

        stock.to_csv("TEST" + str(coin) + "-" + str(timeIntervals[i]) + ".csv")
        print("fetched " + str(coin) + " " + str(timeIntervals[i]) + " data.")
    # for value in enumerate(timeIntervals):
    #     k = value[0]
    #     stock = stockstats.StockDataFrame.retype(coinDataFrame[k])
    #     stock.to_csv("TEST" + str(val["symbol"]) + "-" + str(value[1] + ".csv"))


threads = [threading.Thread(target=getInfos, args=(coin,)) for coin in debugCoins]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()

# print "Elapsed Time: %s" % (time.time() - start)
print(str(coinInfoList))
infoFrame = pd.DataFrame(coinInfoList)
infoFrame.to_csv('info.csv')
# for coin in val["coins"]:
#     print(coin + " " + val["coins"][coin]["minTrade"] + "ticksize: " + val["coins"][coin]["tickSize"])
#
print("####################")
priceList = getCurrentPrices()

# print(val["coins"][symbol])
restartSocket(symbol)

val["bm"].start()
accHoldings = getHoldings()

time.sleep(4)


# coinInfoList = []
# i = 0
# for coin in val["coins"]:
#     i += 1
#     indicators = TA.getTA()
#     coinInfoList.append(indicators)
#
# print(str(coinInfoList))

#
# getTotalBtc()
# for index in enumerate(val["coins"]):
#     print(str(index[1]) + ": - " + str(calculateMinOrderSize(index[1], priceList)))

# val["avgBuyPrice"] = calculateAvgPrice("BUY", "100", "0.00011")
# print(str(val["avgBuyPrice"]))
# val["avgBuyPrice"] = calculateAvgPrice("BUY", "100", "0.00022")
# print(str(val["avgBuyPrice"]))
# val["avgBuyPrice"] = calculateAvgPrice("BUY", "150", "0.0003")
# print(str(val["avgBuyPrice"]))
# val["avgBuyPrice"] = calculateAvgPrice("BUY", "100", "0.000255")
# print(str("{:.8f}".format(float(val["avgBuyPrice"]))))
# val["avgBuyPrice"] = calculateAvgPrice("SELL", "300", "0.000255")
# print("sell")
# print(str("{:.8f}".format(float(val["avgBuyPrice"]))))
# val["avgBuyPrice"] = calculateAvgPrice("BUY", "100", "0.000255")
# print(str("{:.8f}".format(float(val["avgBuyPrice"]))))
# print(str(depthMsg["bids"][5][0]))
#
# priceRefiner(str(depthMsg["bids"][5][0]), str(depthMsg["asks"][5][0]))
#
# while True:
#     print(val["symbol"])
#     print(val["realBuyPrice"] + "  " + val["realSellPrice"])
#     priceRefiner(str(depthMsg["bids"][5][0]), str(depthMsg["asks"][5][0]))
#     # print("realbp: " + str(val["realBuyPrice"]) + " realsp: " + str(val["realSellPrice"]))
#
#     time.sleep(.5)
#
#
#
# # test max order size calculation
# for coin in val["coins"]:
#     maxsize = calculateMaxOrderSize(coin, priceList, "0.20811381")
#     print(coin + ": " + "max order size: " + str(maxsize))
#
# time.sleep(4)
#
# # test min order size calculation
# # for coin in val["coins"]:
# #     minsize = calculateMinOrderSize(coin, priceList)
# #     print(coin + ": " + "min order size: " + str(minsize))
#
# # print(depthMsg)
# test = getHoldings()
# print(len(test))
# print(accHoldings["BTC"])
# while True:
#
#     # print (validateOrderSize(symbol, "BUY"))
#     #
#     # print(float(validateOrderSize(symbol, "BUY")) * float(depthMsg["bids"][0][0]))
#     # print(userMsg)
#     time.sleep(.5)
#     findOrder()
#     cancelAllOrders()
#     logging.debug("test")







# while lookingToBuy == True:
#     priceInRange = checkPrices()
#     while priceInRange == True
#         priceInRange = checkPrices()
#
#         haveToCancel = compareOrder
#             if haveToCancel == True:
#                 cancelOrdersOfType("Buy")
#
#             if myBuyOrder == orderBook[0]
#                 val["status"] = "Buy Order #1"
#             else:
#                 createOrder(orderBook[0]+EINSAT)
#
# # Einkaufen: check if preis ist höchstens x
# def checkPrices(current, target, orderType):
#     if orderType == "BUY":
#         if currentPrice < target:
#             return True
#         else:
#             return False
#
#     if orderType == "SELL";
#         if currentPrice > target:
#             return True
#         else:
#             return False
