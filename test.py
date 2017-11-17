from MAIN import *

symbol= "BCCBTC"

for coin in val["coins"]:
    print(coin + " " + val["coins"][coin]["minTrade"] + "ticksize: " + val["coins"][coin]["tickSize"])

print(val["coins"][symbol])
restartSocket(symbol)

val["bm"].start()

time.sleep(4)

# print(depthMsg)

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
