#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# by Jurek Baumann

"""console UI based on npyscreen.

Docs: npyscreen.readthedocs.io/form-objects.html
"""

import curses
import npyscreen
# from colorSyntax import *
import datetime

from botFunctions import *
from botLogic import *
# from colorSyntax import SyntaxObAsks, SyntaxObBids
# from ui_static import *
import TA
class AlgoForm2(npyscreen.FormBaseNew):
    def create(self):
        self.symbolHead = self.add(npyscreen.FixedText, value="SECOND FORM LOL:", editable=True, color="NO_EDIT", width=15)
        self.debug = self.add(npyscreen.Textfield, value="SECOND FORM LOL:", editable=True, color="NO_EDIT", width=15)
class AlgoForm(npyscreen.FormBaseNew):

    """Main algo bot form."""

    def while_waiting(self):

        # self.setIndicatorData()
        try:
            self.debug.value = "weighted Avg: " + str(val["avgBuyPrice"])

            self.volume.value = "{:.3f}".format(float(tickerMsg["v"])*float(tickerMsg["w"])) + " BTC"
            # self.debug.value = str(val["buyTarget"])
            # self.debug.value = str(val["coins"][symbol]["tickSize"])
            # self.status2.value = "rbp: " + str(val["realBuyPrice"]) + " rsp: " + str(val["realSellPrice"])
        except KeyError:
            self.volume.value = "loading..."
            # self.volume.value = "{:.3f}".format(float(val["coins"][val["symbol"]]["volume"]) * float(val["coins"][val["symbol"]]["close"])) + " BTC"


        # if val["running"] is False:
        #     self.statusHead2.color = "CAUTIONHL"
        #     self.statusHead2.value = "paused"
        #
        # elif val["running"] is True:
        #     self.statusHead2.color = "VERYGOOD"
        #     self.statusHead2.value = "running"




    obRange = 5

    def create(self):
        self.timeFrame = "1m"

        # htokey
        # key_of_choice = 'p'
        # what_to_display = 'Press {} for popup \n Press escape key to quit'.format(key_of_choice)
        #
        # self.how_exited_handers[npyscreen.wgwidget.EXITED_ESCAPE] = self.exit_application
        # self.add_handlers({key_of_choice: self.spawn_notify_popup})

        self.nextrely = 2

        # SYMBOL
        self.symbolHead = self.add(npyscreen.FixedText, value="COIN:", editable=False, color="NO_EDIT", width=15)

        self.nextrely -= 1
        self.nextrelx = 8

        self.chooseCoin = self.add(coinInput, value=str(val["symbol"])[:-3], editable=True, color="GOOD", width=10)

        self.nextrelx = 2

        # ACC VALUE
        self.accValueHead = self.add(npyscreen.FixedText, value="Account Value: ", editable=False, color="WARNING")

        self.nextrely -= 1
        self.nextrelx = len(self.accValueHead.value)+2

        self.accValue = self.add(npyscreen.FixedText, value="00000000", editable=False, clear=True)


        # self.toBtc = self.add(npyscreen.FixedText, value=" – BTC", editable=False, relx=21, rely=1)
        # self.test3 = self.add(npyscreen.FixedText, value="Open buy orders:", editable=False, relx=30, rely=1)

        # self.nextrely += 1
        self.nextrelx = 2

        # TIME RUNNUNG
        self.runningHead = self.add(npyscreen.FixedText, value="Runtime: ", editable=False, color="WARNING")

        self.nextrely -=1
        self.nextrelx = len(self.runningHead.value)+2

        self.timeRunning = self.add(npyscreen.FixedText, value="0:00:00", editable=False, clear=True)

        self.nextrelx = 2

        # DISPLAY STRATEGY
        self.stratHead = self.add(npyscreen.FixedText, value="Strategy: ", editable=False, color="WARNING")

        self.nextrely -= 1
        self.nextrelx = len(self.stratHead.value)+2

        self.strat = self.add(stratInput, value="Boilinger Bot", editable=True, width=14)

        self.nextrelx = 2

        # DISPLAY TIME INTERVAL
        self.ordersWitnessedHead = self.add(npyscreen.FixedText, value="Orders witnessed: ", editable=False, color="WARNING")

        self.nextrelx = 2+len(self.ordersWitnessedHead.value)
        self.nextrely -= 1

        self.ordersWitnessed = self.add(npyscreen.FixedText, value="0", editable=False, max_width=7, clear=True)

        self.nextrely += 1
        self.nextrelx = 2

        # BOLLINGER DISPLAY:

        # upper
        self.upperBollHead = self.add(npyscreen.FixedText, value="Upper Band: ", editable=False, color="WARNING")

        self.nextrelx=2+len(self.upperBollHead.value)
        self.nextrely -= 1

        self.upperBoll = self.add(npyscreen.FixedText, value='{:.8f}'.format(float(val["indicators"][str(self.timeFrame)]["upperBoll"]))[:len(str(val["coins"][symbol]["tickSize"]))], editable=False, clear=True)

        self.nextrelx = 2

        # middle
        self.medBollHead = self.add(npyscreen.FixedText, value="Median Band: ", editable=False, color="WARNING")

        self.nextrelx = 1+len(self.medBollHead.value)
        self.nextrely -= 1

        self.medBoll = self.add(npyscreen.FixedText, value='{:.8f}'.format(float(val["indicators"][str(self.timeFrame)]["medBoll"]))[:len(str(val["coins"][symbol]["tickSize"]))], editable=False, clear=True)

        self.nextrelx = 2

        # lower
        self.lowerBollHead = self.add(npyscreen.FixedText, value="Lower Band: ", editable=False, color="WARNING")

        self.nextrely -= 1
        self.nextrelx=2+len(self.lowerBollHead.value)

        self.lowerBoll = self.add(npyscreen.FixedText, value='{:.8f}'.format(float(val["indicators"][str(self.timeFrame)]["lowerBoll"]))[:len(str(val["coins"][symbol]["tickSize"]))], editable=False, clear=True)

        self.nextrely += 1
        self.nextrelx = 2

        # Volume Delta
        self.volumeHead = self.add(npyscreen.FixedText, value="Volume: ", editable=False, color="WARNING")

        self.nextrelx=2+len(self.volumeHead.value)
        self.nextrely -= 1

        self.volume = self.add(npyscreen.FixedText, value="loading volume", editable=False, clear=True)

        self.nextrelx = 2

        # RSI
        self.rsiHead = self.add(npyscreen.FixedText, value="RSI: ", editable=False, color="WARNING")

        self.nextrely -= 1
        self.nextrelx = 2+len(self.rsiHead.value)

        self.rsi = self.add(npyscreen.FixedText, value="loading rsi", editable=False, clear=True)

        self.nextrelx = 2

        # MACD
        self.macdHead = self.add(npyscreen.FixedText, value="MACD: ", editable=False, color="WARNING")

        self.nextrely -= 1
        self.nextrelx = 2+len(self.macdHead.value)

        self.macd = self.add(npyscreen.FixedText, value="loading macd", editable=False, clear=True)

        self.nextrelx = 2

        self.spreadsHead = self.add(npyscreen.FixedText, value="Current spread: ", editable=False, color="WARNING")

        self.nextrely -= 1
        self.nextrelx = 2+len(self.spreadsHead.value)

        self.spreads = self.add(npyscreen.FixedText, value="loading spread", editable=False, clear=True)

        self.nextrely += 1
        self.nextrelx = 2

        # Time frame input
        self.selectTfHead = self.add(npyscreen.FixedText, value="Interval: ", editable=False,  color="NO_EDIT")

        self.nextrelx = 2+len(self.selectTfHead.value)
        self.nextrely -= 1

        self.selectTf = self.add(timeFrameInput, value="1m", editable=True, max_width=12)

        self.nextrelx = 2
        self.nextrely += 1

        # Sell condition
        self.sellCondHead = self.add(npyscreen.FixedText, value="Sell ", editable=False, color="DANGER")

        self.nextrely -= 1
        self.nextrelx=len(self.sellCondHead.value)+2
        # self.nextrely -= 1

        self.sellQuant = self.add(sizeInput, value=sell_size, editable=True, max_width=16, name="sellQuant")


        self.nextrelx = 2

        self.sellPercent = self.add(userInput, value="0.5", editable=True, width=4, name="sellPercent")

        self.nextrelx = 6
        self.nextrely -= 1

        self.sellPercentHead = self.add(npyscreen.FixedText, value="%", editable=False)

        self.nextrelx = 8
        self.nextrely -= 1

        self.sellAboveBelow = self.add(userInput, value="above", name="sellAboveBelow", width=6)

        self.nextrely -= 1
        self.nextrelx = 14

        self.sellBand = self.add(userInput, value="upper", name="sellBand", width=6)

        self.nextrely -= 1
        self.nextrelx = 20

        self.sellBandHead = self.add(npyscreen.FixedText, value="Band", editable=False)

        self.nextrely +=1
        self.nextrelx = 2

        # Buy condition
        self.buyCondHead = self.add(npyscreen.FixedText, value="Buy ", editable=False, color="GOOD")

        self.nextrely -= 1
        self.nextrelx=len(self.buyCondHead.value)+2
        # self.nextrely -= 1

        self.buyQuant = self.add(sizeInput, value=buy_size, editable=True, max_width=16, name="buyQuant")


        self.nextrelx = 2

        self.buyPercent = self.add(userInput, value="0.5", editable=True, width=4, name="buyPercent")

        # self.buyPercent.exit_right()  # , exit_right

        self.nextrelx = 6
        self.nextrely -= 1

        self.buyPercentHead = self.add(npyscreen.FixedText, value="%", editable=False)

        self.nextrelx = 8
        self.nextrely -= 1

        self.buyAboveBelow = self.add(userInput, value="below", name="buyAboveBelow", width=6)

        self.nextrely -= 1
        self.nextrelx = 14

        self.buyBand = self.add(userInput, value="lower", name="buyBand", width=6)

        self.nextrely -= 1
        self.nextrelx = 20

        self.buyBandHead = self.add(npyscreen.FixedText, value="Band", editable=False)




        self.start_button = self.add(npyscreen.ButtonPress, name='[Start]', relx=4, rely=25, hidden=False)
        self.start_button.whenPressed = self.start_button_pressed

        self.sellTargetDisplay = self.add(npyscreen.FixedText, value="0", editable=False)
        self.buyTargetDisplay = self.add(npyscreen.FixedText, value="0", editable=False)



        ##########

        # self.debug = self.add(npyscreen.FixedText, value="debug")
        #
        # self.status2 = self.add(npyscreen.FixedText, value="fake status")
        #
        # self.statusLine0 = self.add(npyscreen.FixedText, value="2nd status", relx=2, rely=-5, editable=False)
        #
        # self.statusLine = self.add(npyscreen.FixedText, value="2nd status", relx=2, rely=-4, editable=False)

        self.statusHead = self.add(npyscreen.FixedText, value="STATUS:", relx=2, rely=-3, editable=False, color="CAUTIONHL")

        self.statusHead2 = self.add(npyscreen.FixedText, value="paused", relx=10, rely=-3, editable=False, color="CAUTIONHL")

        self.status = self.add(npyscreen.FixedText, value="Ready and awaiting orders, Sir [$]◡[$]", relx=17, rely=-3, editable=False)

        self.nextrely = 16

        self.test1 = self.add(npyscreen.FixedText, value="Open buy orders:", editable=False, relx=30)

        self.nextrely -= 1

        self.test2 = self.add(npyscreen.FixedText, value="Open sell orders:", editable=False, relx=52)


        self.debug = self.add(npyscreen.FixedText, value="debug", editable=False, relx=30)
        ###########################
        # Orderbook / trade history
        ###########################

        # initalize variables for various calculations
        self.bids = {}
        self.asks = {}
        self.asksIndex = {}
        self.bidsIndex = {}
        self.asksQuant = {}
        self.bidsQuant = {}
        self.oHistory, self.oHistoryTime, self.oHistoryQuant = {}, {}, {}
        self.obMargin = 30

        # ORDERBOOK

        # Create asks template
        for i in range(self.obRange):
            self.asksIndex[i] = self.add(npyscreen.FixedText, value=str(int(self.obRange)-i), editable=False, relx=self.obMargin, rely=i+2, clear=True)

            self.asks[(self.obRange)-(i+1)] = self.add(npyscreen.FixedText, value="0.00012345", editable=False, relx=self.obMargin+2, rely=i+2, color="DANGER", clear=True)

            self.asksQuant[(self.obRange)-(i+1)] = self.add(npyscreen.FixedText, value="12.345", editable=False, relx=self.obMargin+13, rely=i+2, clear=True)



        # Add Spread between asks and bids
        self.spread = self.add(npyscreen.FixedText, value="Spread", editable=False, relx=self.obMargin, rely=self.obRange+3, clear=True)

        for i in range(self.obRange):
            self.bidsIndex[i] = self.add(npyscreen.FixedText, value=str(i+1), editable=False, relx=self.obMargin, rely=i+self.obRange+5, clear=True)

            self.bids[i] = self.add(npyscreen.FixedText, value="0.00012345", editable=False, relx=self.obMargin+2, rely=i+self.obRange+5, clear=True, color="GOOD")

            self.bidsQuant[i] = self.add(npyscreen.FixedText, value="12.345", editable=False, relx=self.obMargin+13, rely=i+self.obRange+5, clear=True)




        # Create order history template TODO: add quantity and timestamp
        for i in range(self.obRange*2+3):
            self.oHistory[i] = self.add(npyscreen.FixedText, value="+*", editable=False, relx=self.obMargin+22, rely=i+2, clear=True)

            self.oHistoryQuant[i] = self.add(npyscreen.FixedText, value="0.00", editable=False, relx=self.obMargin+33, rely=i+2, clear=True)

            # self.oHistoryTime[i] = self.add(npyscreen.FixedText, value="13:37:00", editable=False, relx=self.obMargin+42, rely=i+3)





        self.revalidate()
        self.setIndicatorData()
        self.parentApp.updateDepth()
        #
        #
        # self.debug2 = self.add(npyscreen.FixedText, value=val["coins"][symbol]["tickSize"])
        #
        # self.debug2 = self.add(npyscreen.FixedText, value=len(str(val["coins"][symbol]["tickSize"])))

        # self.testLOL  = self.add(npyscreen.FixedText, value = "#", relx=1, rely=-3)

    # def spawn_notify_popup(self, code_of_key_pressed):
    #     message_to_display = 'I popped up \n passed: {}'.format(code_of_key_pressed)
    #     npyscreen.notify(message_to_display, title='Popup Title')
    #     time.sleep(5)  # needed to have it show up for a visible amount of time

    def update_order_book(self):
        self.ordersWitnessed.value = str(val["depthTracker"])
        if self.obRange > 0:
            for index in enumerate(range(self.obRange)):
                i = index[0]
                try:
                    if float(depthMsg["bids"][i][1]).is_integer():
                        self.bidsQuant[i].value = str(int(float(depthMsg["bids"][i][1]))).zfill(4)
                        self.asksQuant[i].value = str(int(float(depthMsg["asks"][i][1]))).zfill(4)
                    else:
                        self.bidsQuant[i].value = "{:.3f}".format(float(depthMsg["bids"][i][1]))
                        self.asksQuant[i].value = "{:.3f}".format(float(depthMsg["asks"][i][1]))

                    self.bids[i].value = depthMsg["bids"][i][0]
                    self.asks[i].value = depthMsg["asks"][i][0]

                except (KeyError, NameError):
                    pass


        try:
            spreadVal = ((float(depthMsg["asks"][0][0])-float(depthMsg["bids"][0][0]))/float(depthMsg["asks"][0][0]))*100
            self.spread.value = "Spread: " + str(round(spreadVal, 2))+"%"
        except (KeyError, ZeroDivisionError):
            pass


        ticksize = float(val["coins"][val["symbol"]]["minTrade"])

        histSizes = []
        try:
            for index in enumerate(globalList):
                histSizes.append(float(globalList[index[0]]["quantity"]))
            highestQuant = max(histSizes)
            numberOfDigits = int(len(str(highestQuant)))-2
        except:
            pass

        for i in range(self.obRange*2+3):
            if globalList[i]["order"] == "True":
                self.oHistory[i].value = str(globalList[i]["price"])
                self.oHistory[i].color = "DANGER"
            elif globalList[i]["order"] == "False":
                self.oHistory[i].value = str(globalList[i]["price"])
                self.oHistory[i].color = "GOOD"
            else:
                self.oHistory[i].value = "          "

            # self.oHistoryTime[i].value = datetime.date(int(str(globalList[i]["timestamp"])[:-3])).strftime("%M:%S")



            if ticksize.is_integer():
                self.oHistoryQuant[i].value = str(int(float(globalList[i]["quantity"]))).zfill(numberOfDigits)

            else:
                self.oHistoryQuant[i].value = "{:.8f}".format((float(globalList[i]["quantity"]))).rstrip('0').zfill(numberOfDigits).ljust(numberOfDigits+2, "0")

            self.display()




    def exit_application(self):
        self.parentApp.setNextForm(None)
        self.editing = False

    def revalidate(self):

        # Check sell order size
        if isfloat(self.sellQuant.value):
            val["sellSize"] = str(self.sellQuant.value)
        if isfloat(self.buyQuant.value):
            val["buySize"] = str(self.buyQuant.value)


        isvalid = self.validateInput()
        if isvalid == "not valid":
            self.status.value = "Please check inputs."
        else:

            val["buyTarget"] = str(isvalid[0])[:len(str(val["coins"][symbol]["tickSize"]))]
            val["sellTarget"] = str(isvalid[1])[:len(str(val["coins"][symbol]["tickSize"]))]
            try:
                self.sellTargetDisplay.value = str(val["sellTarget"])
                self.buyTargetDisplay.value = str(val["buyTarget"])
                # self.spreads.value = "{:.8f}".format(((float(val["sellTarget"]) / float(val["buyTarget"]))-1)*100)
                self.spreads.value = "{:.2f}".format(((float(val["sellTarget"]) - float(val["buyTarget"])) / float(val["sellTarget"]))*100) + "%"

                self.accValue.value = str(getTotalBtc())

                # call the function that is called when the enter key is pressed on the order size input
                # self.sellQuant.change_size("key")
                # self.buyQuant.change_size("key")

            except KeyError:
                self.status.value = "buy/ sell targets not available"


    # START BUTTON PRESSED
    def start_button_pressed(self):
        if self.start_button.name == "Start":
            self.start_button.name = "Stop"
            val["running"] = True
            self.status.value = " Buying " + str(val["buySize"]) + " below " + str(val["buyTarget"] + ". " + "Selling " + str(val["sellSize"]) + " above " + str(str(val["sellTarget"])))
            self.statusHead2.value = "running "
            self.statusHead2.color = "VERYGOOD"
            # debug
            val["initiateBuy"] = True
        else:
            self.start_button.name = "Start"
            val["running"] = False
            self.status.value = "Ready and awaiting orders, Sir [$]◡[$]"
            self.statusHead2.value = "paused"
            self.statusHead2.color = "CAUTIONHL"
            cancelAllOrders()

        self.revalidate()

    def turn_off_bot(self):
        """Disable bot activity and return everything back to normal."""

        self.start_button.name = "Stop"
        val["running"] = False
        self.status.value = "Ready and awaiting orders, Sir [$]◡[$]"
        cancelAllOrders()

    # TODO: refactor
    def validateInput(self):
        notValid = False



        # CHeck sell percent input
        if isfloat(self.sellPercent.value) and float(self.sellPercent.value) > 0 and float(self.sellPercent.value) < 100:
            userSellPrice = self.sellPercent.value
        else:
            self.sellPercent.color="DANGER"
            notValid = True


        # Check buy percent input
        if isfloat(self.buyPercent.value) and float(self.buyPercent.value) > 0 and float(self.buyPercent.value) < 100:
            userBuyPrice = self.buyPercent.value
        else:
            self.buyPercent.color="DANGER"
            notValid = True


        # Check sell Band
        if str(self.sellBand.value) == "upper":
            sellBand = "upperBoll"
        elif str(self.sellBand.value) == "middle" or str(self.sellBand.value) == "mid":
            sellBand = "medBoll"
        elif str(self.sellBand.value) == "lower":
            sellBand = "lowerBoll"
        else:
            self.sellBand.color="DANGER"
            notValid = True

        # Check buy Band
        if str(self.buyBand.value) == "upper":
            buyBand = "upperBoll"
        elif str(self.buyBand.value) == "middle" or str(self.buyBand.value) == "mid":
            buyBand = "medBoll"
        elif str(self.buyBand.value) == "lower":
            buyBand = "lowerBoll"
        else:
            self.buyBand.color="DANGER"
            notValid = True


        # Check sell operator
        try:
            if self.sellAboveBelow.value == "below":
                targetSellPrice = float(val["indicators"][self.timeFrame][sellBand] * (1 - (float(userSellPrice) / 100)))

            elif self.sellAboveBelow.value == "above":
                targetSellPrice = float(val["indicators"][self.timeFrame][sellBand] * (1 + (float(userSellPrice) / 100)))

            else:
                self.sellAboveBelow.color = "DANGER"
                notValid = True

            # Check buy operator
            if self.buyAboveBelow.value == "below":
                targetBuyPrice = float(val["indicators"][self.timeFrame][buyBand] * (1 - (float(userBuyPrice) / 100)))

            elif self.buyAboveBelow.value == "above":
                targetBuyPrice = float(val["indicators"][self.timeFrame][buyBand] * (1 + (float(userBuyPrice) / 100)))

            else:
                self.buyAboveBelow.color = "DANGER"
                notValid = True
        except UnboundLocalError:
            notValid = True



        if notValid is False:
            logging.debug("User inputs are valid.")
            finaltargetBuyPrice = '{:.8f}'.format(targetBuyPrice)[:len(str(val["coins"][symbol]["tickSize"]))]

            finaltargetSellPrice = '{:.8f}'.format(targetSellPrice)[:len(str(val["coins"][symbol]["tickSize"]))]

            self.sellPercent.color="DEFAULT"
            self.buyPercent.color="DEFAULT"
            self.sellBand.color="DEFAULT"
            self.buyBand.color="DEFAULT"
            self.sellAboveBelow.color="DEFAULT"
            self.buyAboveBelow.color="DEFAULT"

            return [finaltargetBuyPrice, finaltargetSellPrice]


        return "not valid"





    def setIndicatorData(self):
        self.upperBoll.value = '{:.8f}'.format(float(val["indicators"][str(self.timeFrame)]["upperBoll"]))[:len(str(val["coins"][symbol]["tickSize"]))]

        self.medBoll.value = '{:.8f}'.format(float(val["indicators"][str(self.timeFrame)]["medBoll"]))[:len(str(val["coins"][symbol]["tickSize"]))]

        self.lowerBoll.value = '{:.8f}'.format(float(val["indicators"][str(self.timeFrame)]["lowerBoll"]))[:len(str(val["coins"][symbol]["tickSize"]))]


        self.rsi.value = val["indicators"][str(self.timeFrame)]["rsi6h"]

        self.macd.value = val["indicators"][str(self.timeFrame)]["macd"]



        if self.start_button.name == "Stop":
            self.revalidate()
            # self.status.value = "SET BAND INFO"



        self.display()


class AlgoBot(npyscreen.NPSAppManaged):

    """MAIN app class."""

    # update interval too low causes bugs?
    keypress_timeout_default = 10

    def change_form(self, name):
        self.switchForm(name)

    # initiate Forms on start
    def onStart(self):
        self.addForm("MAIN", AlgoForm, name="Juris beeeser Binance Bot", color="GOOD")
        self.addForm("SECOND", AlgoForm2, name="second page")

    def setStatus(self, statusMsg):
        try:
            self.getForm("MAIN").status.value = str(statusMsg)
        except KeyError:
            pass

    def periodicUpdate(self):

        if val["depthTracker"] == 0:
            self.getForm("MAIN").statusHead.color = "CAUTIONHL"
            # self.getForm("MAIN").status.value = "Waiting for Websocket..."
        else:
            if self.getForm("MAIN").statusHead.color == "CAUTIONHL":
                self.getForm("MAIN").statusHead.color = "VERYGOOD"
                val["restartTimer"] = 0

            # if self.getForm("MAIN").status.value == "Waiting for Websocket...":
                self.getForm("MAIN").status.value = "Awaiting orders"


        try:
            self.getForm("MAIN").timeRunning.value = str(datetime.timedelta(seconds=int(val["runTime"])))

            self.getForm("MAIN").display()
        except KeyError:
            pass
        # self.getForm("MAIN").display()


    def hardRefresh(self):
        self.getForm("MAIN").DISPLAY()

    def updateDepth(self):
        pass
            # self.getForm("MAIN").debug.value = str(val["depthTracker"])
            # self.getForm("MAIN").statusLine.value = "Buy under: " + str(val["buyTarget"]) + " order at: " + str(val["realBuyPrice"])
            # self.getForm("MAIN").statusLine0.value = "Sell over: " + str(val["sellTarget"]) + " order at: " + str(val["realSellPrice"])
        # self.getForm("MAIN").display()


    def forward_update(self):
        try:
            self.getForm("MAIN").update_order_book()
        except KeyError:
            pass
        # try:
        #     for index in enumerate(range(self.getForm("MAIN").obRange)):
        #         i = index[0]
        #
        #         self.getForm("MAIN").bids[i].value = depthMsg["bids"][i][0]
        #         self.getForm("MAIN").bidsQuant[i].value = depthMsg["bids"][i][1]
        #
        #         self.getForm("MAIN").asks[i].value = depthMsg["asks"][i][0]
        #         self.getForm("MAIN").asksQuant[i].value = depthMsg["asks"][i][1]
        #
        #
        #         self.getForm("MAIN").timeRunning.value = str(datetime.timedelta(seconds=int(val["runTime"])))
        #         self.getForm("MAIN").display()
        # except KeyError:
        #     pass



app = AlgoBot()


class timeFrameInput(npyscreen.Textfield):

    """Input field class for defining the order size.

    Input is evaluated and colorized
    """

    def __init__(self, *args, **kwargs):
        """Overwrite init function to add key handlers."""
        super().__init__(*args, **kwargs)
        self.add_handlers(
            {
                curses.ascii.NL: self.pressed_enter,
                curses.ascii.CR: self.pressed_enter,
                curses.KEY_ENTER: self.pressed_enter,
            }
        )

    def when_value_edited(self):
        """Fire when value is edited."""

        if str(self.value) in self.tf1m or str(self.value) in self.tf5m or str(self.value) in self.tf15m or str(self.value) in self.tf30m or str(self.value) in self.tf1h:
            self.color = "GOOD"
        else:
            self.color = "DEFAULT"

    def pressed_enter(self, inputVal):

        # stop bot, recalc data
        self.parent.start_button.name = "Start"
        val["running"] = False

        if str(self.value) in self.tf1m:
            self.parent.timeFrame = "1m"
        elif str(self.value) in self.tf5m:
            self.parent.timeFrame = "5m"
        elif str(self.value) in self.tf15m:
            self.parent.timeFrame = "15m"
        elif str(self.value) in self.tf30m:
            self.parent.timeFrame = "30m"
        elif str(self.value) in self.tf1h:
            self.parent.timeFrame = "1h"
        else:
            self.parent.status.value = "Not a valid time interval."

        self.parent.revalidate()
        self.parent.setIndicatorData()
        self.parent.display()
        # self.parent.status.value = "Timeframe: " + str(self.value)
    tf1m = ["1m", "1 min", "1min", "1minute", "1 minute", "1 Minute"]
    tf5m = ["5", "5m", "5 min", "5min", "5minutes", "5 minutes", "5 Minutes", "5 minuten", "5 Minuten"]
    tf15m = ["15", "15m", "15 min", "15min", "15minutes", "15 minutes", "15 Minutes", "15 minuten", "15 Minuten"]
    tf30m = ["30", "30m", "30 min", "30min", "30minutes", "30 minutes", "30 Minutes", "30 minuten", "30 Minuten"]
    tf1h = ["1h", "1 hour", "1hour", "1 stunde", "1 Stunde"]


class userInput(npyscreen.Textfield):

    """general user input field class.

    Featuring hotkeys and automatic stopping behavior.
    """

    def __init__(self, *args, **kwargs):
        """Overwrite init function to add key handlers."""
        super().__init__(*args, **kwargs)
        self.add_handlers(
            {
                curses.ascii.NL: self.pressed_enter,
                curses.ascii.CR: self.pressed_enter,
                curses.KEY_ENTER: self.pressed_enter,
                "R": self.pressed_r,
                "Q": self.pressed_q,
                "S": self.pressed_s,
                "I": self.pressed_i,
            }
        )

    def pressed_enter(self, key):
        self.parent.start_button.name = "Start"
        val["running"] = False
        cancelAllOrders()

        self.parent.status.value = "Calculated new limits."
        self.parent.revalidate()

    def pressed_r(self, key):
        self.parent.DISPLAY()

    def pressed_q(self, key):
        cleanExit()
        self.editing = False
        self.parent.parentApp.switchForm(None)

    def pressed_s(self, key):
        self.parent.status.value = "pressed s"

    def pressed_i(self, key):
        npyscreen.notify_confirm("+++ INFO +++\nJuris Binance Boilinger Bot Version 0.1\n \n Achtung: \n Q:     exit program\nS:     start/stop the bot\nR:     refresh the screen\nI: this info window")

    def when_value_edited(self):
        if self.name == "sellAboveBelow" or self.name == "buyAboveBelow":
            if self.value == "below" or self.value == "above":
                self.color = "GOOD"
            else:
                self.color = "DEFAULT"

        if self.name == "sellPercent" or self.name == "buyPercent":
            if isfloat(self.value):
                if float(self.value) > 0 and float(self.value) < 100:
                    self.color = "GOOD"
                else:
                    self.color = "DEFAULT"

        if self.name == "sellBand" or self.name == "buyBand":
            if self.value == "upper" or self.value == "middle" or self.value == "lower" or self.value == "mid":
                self.color = "GOOD"
            else:
                self.color = "DEFAULT"


class userSelect(npyscreen.FixedText):
    """general user selection class.

    Contains global hotkeys like quit, start, refresh...
    """

    def __init__(self, *args, **kwargs):
        """Overwrite init function to add key handlers."""
        super().__init__(*args, **kwargs)
        self.add_handlers(
            {
                curses.ascii.NL: self.pressed_enter,
                curses.ascii.CR: self.pressed_enter,
                curses.KEY_ENTER: self.pressed_enter,
                "R": self.pressed_r,
                "Q": self.pressed_q,
                "S": self.pressed_s,
                "I": self.pressed_i,
            }
        )

    def pressed_enter(self, key):
        self.parent.start_button.name = "Start"
        val["running"] = False
        cancelAllOrders()

        self.parent.status.value = "Calculated new limits."
        self.parent.revalidate()

    def pressed_r(self, key):
        self.parent.DISPLAY()

    def pressed_q(self, key):
        cleanExit()
        self.editing = False
        self.parent.parentApp.switchForm(None)

    def pressed_s(self, key):
        self.parent.status.value = "pressed s"

    def pressed_i(self, key):
        npyscreen.notify_confirm("+++ INFO +++\nJuris Binance Boilinger Bot Version 0.1\n \n Achtung: \n Q:     exit program\nS:     start/stop the bot\nR:     refresh the screen\nI: this info window")



class buyInput(userInput):

    def when_value_edited(self):

        self.parent.start_button.name = "Start"
        val["running"] = False

        if isfloat(str(self.value)) and float(self.value) < 100 and float(self.value) >= 0:
            self.parent.buyPercentHead.value = "%"
            self.color = "DEFAULT"
        else:
            self.parent.buyPercentHead.value = ""
            self.color = "DANGER"
    pass


class NotifyInfo(npyscreen.Form):
    def create(self):
        key_of_choice = 'p'
        what_to_display = 'Press {} for popup \n Press escape key to quit'.format(key_of_choice)

        self.how_exited_handers[npyscreen.wgwidget.EXITED_ESCAPE] = self.exit_application
        self.add_handlers({key_of_choice: self.spawn_notify_popup})
        self.add(npyscreen.FixedText, value=what_to_display)

    def spawn_notify_popup(self, code_of_key_pressed):
        message_to_display = 'I popped up \n passed: {}'.format(code_of_key_pressed)
        npyscreen.notify(message_to_display, title='Popup Title')
        time.sleep(1)  # needed to have it show up for a visible amount of time


class coinInput(userInput):

    """Input field to change the selected coin."""

    def __init__(self, *args, **kwargs):
        """Overwrite init function to add key handlers."""
        super().__init__(*args, **kwargs)
        self.add_handlers(
            {
                curses.ascii.NL: self.change_coin,
                curses.ascii.CR: self.change_coin,
                curses.KEY_ENTER: self.change_coin,
            }
        )

    def key_pressed(self, inputVal):
        npyscreen.notify_wait(str(inputVal))
        self.parent.parentApp.hardRefresh()
        # self.value = self.value[:-1]

    # CHANGE COIN
    def change_coin(self, inputVal):
        if str(self.value).upper() + str("BTC") in val["coins"] and self.value + str("BTC") != val["symbol"]:
            val["symbol"] = str(self.value).upper() + str("BTC")
            self.color = "DEFAULT"

            # self.parent.symbol.value = str(val["symbol"])

            # unselect buy/sell and hide input fields and start button
            # self.parent.turnSelectorOff()
            # logging.debug("triggere clearDepth")
            # clearDepth()
            restartSocket(str(val["symbol"]))
            val["depthTracker"] = 0

            # npyscreen.notify_wait("Switching to " + str(self.value) + " please wait...")

            #
            # self.parent.clearOrderBook()
            fetchDepth(str(val["symbol"]))
            logging.debug("LÖSCHE GLOBALLIST!!!")
            del globalList[0:len(globalList)]
            fillList(str(val["symbol"]))
            app.forward_update()


            val["indicators"] = TA.getTA()
            self.parent.setIndicatorData()
            self.parent.revalidate()
            val["cs"] = 0


        elif self.value + str("BTC") != val["symbol"]:
            npyscreen.notify_wait("Was soll " + str(self.value) + " bitte für eine Coin sein?")
        # bm.stop_socket(conn_key)
        else:
            pass

    def when_value_edited(self):
        # saved_val = str(self.value)
        # self.value = ""
        # # self.parent.chooseCoin.width=len(self.value)
        #
        # self.parent.chooseCoin= self.parent.add(coinInput, value=str(saved_val), editable=True, relx=16, rely=1, width=len(saved_val))
        # self.parent.toBtc = self.parent.add(npyscreen.FixedText, value="– BTC", editable=False, relx=17+len(saved_val), rely=1, width=6)
        # self.value = self.value
        # self.parent.symbolHead.value= "Trade pair: "
        if str(self.value).upper() + str("BTC") in val["coins"]:
            self.color = "LABEL"
            self.value = str(self.value).upper()
        elif len(str(self.value)) < 6:
            self.color = "WARNING"

        else:
            self.color = "DANGER"

class stratInput (userSelect):
    def __init__(self, *args, **kwargs):
        """Overwrite init function to add key handlers."""
        super().__init__(*args, **kwargs)
        self.add_handlers(
            {
                curses.ascii.NL: self.change_strat,
                curses.ascii.CR: self.change_strat,
                curses.KEY_ENTER: self.change_strat,

                curses.KEY_LEFT: self.select_strat,
                curses.KEY_RIGHT: self.select_strat,
            }
        )

    def select_strat(self, key):
        if self.value == "Boilinger Bot":
            self.value = "andere strat"
        else:
            self.value = "Boilinger Bot"

    def change_strat(self, key):
        self.parent.editing = False
        self.parent.parentApp.switchForm("SECOND")
        # self.parent.parentApp.change_form("SECOND")

class sizeInput(userInput):
    def __init__(self, *args, **kwargs):
        """Overwrite init function to add key handlers."""
        super().__init__(*args, **kwargs)
        self.add_handlers(
            {
                curses.ascii.NL: self.change_size,
                curses.ascii.CR: self.change_size,
                curses.KEY_ENTER: self.change_size,
            }
        )

    def key_pressed(self, inputVal):
        npyscreen.notify_wait(str(inputVal))
        self.parent.parentApp.hardRefresh()
        # self.value = self.value[:-1]

    def change_size(self, key):
        if self.color == "GOOD" or self.color == "WARNING":
            if self.name == "sellQuant":
                val["sellSize"] = self.value
            elif self.name == "buyQuant":
                val["buySize"] = self.value

    def when_value_edited(self):
        sizeValidation = validateOrderSize(self.value, val["symbol"], val["priceList"], float(getTotalBtc()))
        if sizeValidation == "GOOD":
            self.color = "GOOD"
        elif sizeValidation == "OK":
            self.color = "WARNING"
        else:
            self.color = "DANGER"
