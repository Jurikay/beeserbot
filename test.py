from MAIN import *

symbol= "BCCBTC"
#
for coin in val["coins"]:
    print(coin + " " + val["coins"][coin]["minTrade"] + "ticksize: " + val["coins"][coin]["tickSize"])
#
print("####################")
priceList = getCurrentPrices()

# print(val["coins"][symbol])
restartSocket(symbol)

val["bm"].start()

time.sleep(4)



# test max order size calculation
for coin in val["coins"]:
    maxsize = calculateMaxOrderSize(coin, priceList, "0.20811381")
    print(coin + ": " + "max order size: " + str(maxsize))

time.sleep(4)

# test min order size calculation
# for coin in val["coins"]:
#     minsize = calculateMinOrderSize(coin, priceList)
#     print(coin + ": " + "min order size: " + str(minsize))

# print(depthMsg)
test = getHoldings()
print(len(test))
print(accHoldings["BTC"])
while True:

    # print (validateOrderSize(symbol, "BUY"))
    #
    # print(float(validateOrderSize(symbol, "BUY")) * float(depthMsg["bids"][0][0]))
    # print(userMsg)
    time.sleep(.5)







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
