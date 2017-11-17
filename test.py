from MAIN import *

symbol= "BNBBTC"

for coin in val["coins"]:
    print(coin + " " + val["coins"][coin]["minTrade"] + "ticksize: " + val["coins"][coin]["tickSize"])

print(val["coins"][symbol])
restartSocket(symbol)

val["bm"].start()



# print(depthMsg)

print (validateOrderSize(symbol, "0.0417", "0.04187", "BUY"))




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
