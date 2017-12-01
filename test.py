#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# by Jurek Baumann

"""Used for testing only. Not part of the app."""


import logging
logging.basicConfig(filename="test.log", level=logging.DEBUG, format='%(asctime)s %(message)s')
from MAIN import *
symbol = "QSPBTC"
#
for coin in val["coins"]:
    print(coin + " " + val["coins"][coin]["minTrade"] + "ticksize: " + val["coins"][coin]["tickSize"])
#
print("####################")
priceList = getCurrentPrices()

# print(val["coins"][symbol])
restartSocket(symbol)

val["bm"].start()
accHoldings = getHoldings()

time.sleep(4)

#
# getTotalBtc()
# for index in enumerate(val["coins"]):
#     print(str(index[1]) + ": - " + str(calculateMinOrderSize(index[1], priceList)))

val["avgBuyPrice"] = calculateAvgPrice("BUY", "100", "0.00011")
print(str(val["avgBuyPrice"]))
val["avgBuyPrice"] = calculateAvgPrice("BUY", "100", "0.00022")
print(str(val["avgBuyPrice"]))
val["avgBuyPrice"] = calculateAvgPrice("BUY", "150", "0.0003")
print(str(val["avgBuyPrice"]))
val["avgBuyPrice"] = calculateAvgPrice("BUY", "100", "0.000255")
print(str("{:.8f}".format(float(val["avgBuyPrice"]))))
val["avgBuyPrice"] = calculateAvgPrice("SELL", "300", "0.000255")
print("sell")
print(str("{:.8f}".format(float(val["avgBuyPrice"]))))
val["avgBuyPrice"] = calculateAvgPrice("BUY", "100", "0.000255")
print(str("{:.8f}".format(float(val["avgBuyPrice"]))))
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
