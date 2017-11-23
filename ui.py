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

# from ui_static import *



class AlgoForm(npyscreen.FormBaseNew):

    """Main algo bot form."""

    def while_waiting(self):
        # self.setIndicatorData()
        try:
            self.volume.value = str(round(float(tickerMsg["v"])*float(tickerMsg["w"]), 8))
            # self.debug.value = str(val["buyTarget"])
            # self.debug.value = str(val["coins"][symbol]["tickSize"])
            self.status2.value = "rbp: " + str(val["realBuyPrice"]) + " rsp: " + str(val["realSellPrice"])
        except KeyError:
            self.volume.value = "Key Error"

        if val["running"] is False:
            self.statusHead2.color = "CAUTIONHL"
        elif val["running"] is True:
            self.statusHead2.color = "VERYGOOD"



    def setStatus(self, statusMsg):
        self.status.value = str(statusMsg)

    def create(self):
        self.timeFrame = "1m"

        # htokey
        # key_of_choice = 'p'
        # what_to_display = 'Press {} for popup \n Press escape key to quit'.format(key_of_choice)
        #
        # self.how_exited_handers[npyscreen.wgwidget.EXITED_ESCAPE] = self.exit_application
        # self.add_handlers({key_of_choice: self.spawn_notify_popup})



        # SYMBOL
        self.symbolHead = self.add(npyscreen.FixedText, value="Trade pair: ", editable=False, color="NO_EDIT", relx=2, rely=1)

        self.symbol = self.add(npyscreen.FixedText, value=str(val["symbol"]), editable=False, color="WARNING", relx=2+len(self.symbolHead.value), rely=1)

        # TIME RUNNUNG
        self.runningHead = self.add(npyscreen.FixedText, value="Runtime: ", editable=False, relx=2, rely=3, color="WARNING")

        self.timeRunning = self.add(npyscreen.FixedText, value="0:00:00", editable=False,  relx=2+len(self.runningHead.value), rely=3)

        # DISPLAY STRATEGY
        self.stratHead = self.add(npyscreen.FixedText, value="Strategy: ", editable=False, relx=2, rely=4, color="WARNING")

        self.strat = self.add(npyscreen.FixedText, value="Boilinger Bot", editable=False,  relx=2+len(self.stratHead.value), rely=4)

        # DISPLAY TIME INTERVAL
        self.intervalHead = self.add(npyscreen.FixedText, value="Time interval: ", editable=False, relx=2, rely=5, color="WARNING")

        self.interval = self.add(npyscreen.FixedText, value="1 Minute", editable=False,  relx=2+len(self.intervalHead.value), rely=5)


        # BOLLINGER DISPLAY:

        # upper
        self.upperBollHead = self.add(npyscreen.FixedText, value="Upper Band: ", editable=False, relx=2, rely=7, color="WARNING")

        self.upperBoll = self.add(npyscreen.FixedText, value='{:.8f}'.format(float(val["indicators"][str(self.timeFrame)]["upperBoll"]))[:len(str(val["coins"][symbol]["tickSize"]))], editable=False,  relx=2+len(self.upperBollHead.value), rely=7)

        # middle
        self.medBollHead = self.add(npyscreen.FixedText, value="Median Band: ", editable=False, relx=2, rely=8, color="WARNING")

        self.medBoll = self.add(npyscreen.FixedText, value='{:.8f}'.format(float(val["indicators"][str(self.timeFrame)]["medBoll"]))[:len(str(val["coins"][symbol]["tickSize"]))], editable=False, relx=1+len(self.medBollHead.value), rely=8)


        # lower
        self.lowerBollHead = self.add(npyscreen.FixedText, value="Lower Band: ", editable=False, relx=2, rely=9, color="WARNING")

        self.lowerBoll = self.add(npyscreen.FixedText, value='{:.8f}'.format(float(val["indicators"][str(self.timeFrame)]["lowerBoll"]))[:len(str(val["coins"][symbol]["tickSize"]))], editable=False,  relx=2+len(self.lowerBollHead.value), rely=9)


        # Volume Delta
        self.volumeHead = self.add(npyscreen.FixedText, value="Volume: ", editable=False, relx=2, rely=11, color="WARNING")

        self.volume = self.add(npyscreen.FixedText, value="loading volume", editable=False,  relx=2+len(self.volumeHead.value), rely=11)

        # RSI
        self.rsiHead = self.add(npyscreen.FixedText, value="RSI: ", editable=False, relx=2, rely=12, color="WARNING")

        self.rsi = self.add(npyscreen.FixedText, value="loading rsi", editable=False,  relx=2+len(self.rsiHead.value), rely=12)

        # MACD
        self.macdHead = self.add(npyscreen.FixedText, value="MACD: ", editable=False, relx=2, rely=13, color="WARNING")

        self.macd = self.add(npyscreen.FixedText, value="loading macd", editable=False,  relx=2+len(self.macdHead.value), rely=13)


        # Time frame input
        self.selectTfHead = self.add(npyscreen.FixedText, value="Choose interval: ", editable=False, relx=2, rely=14, color="NO_EDIT")

        self.selectTf = self.add(timeFrameInput, value="1m", editable=True,  relx=2+len(self.selectTfHead.value), rely=14)


        # Sell condition
        self.sellCondHead = self.add(npyscreen.FixedText, value="Sell if price is >", editable=False, relx=2, rely=16, color="DANGER")

        self.sellTargetDisplay = self.add(npyscreen.FixedText, value="0", editable=False, relx=len(self.sellCondHead.value)+3, rely=16)

        self.sellPercent = self.add(userInput, value="0.5", editable=True, relx=2, rely=17, width=4)

        self.sellPercentHead = self.add(npyscreen.FixedText, value="%", editable=False, relx=6, rely=17)

        self.sellAboveBelow = self.add(userInput, value="above", relx=2, rely=18)

        self.sellBand = self.add(userInput, value="upper", relx=2, rely=19, width=7)

        self.sellBandHead = self.add(npyscreen.FixedText, value="Band", relx=9, rely=19, editable=False)


        # Buy condition
        self.buyCondHead = self.add(npyscreen.FixedText, value="Buy if price is <", editable=False, relx=2, rely=21, color="GOOD")

        self.buyTargetDisplay = self.add(npyscreen.FixedText, value="0", editable=False, relx=len(self.buyCondHead.value)+3, rely=21)


        self.buyPercent = self.add(buyInput, value="0.5", editable=True, relx=2, rely=22, max_width=4)

        self.buyPercentHead = self.add(npyscreen.FixedText, value="%", editable=False, relx=6, rely=22)

        self.buyAboveBelow = self.add(userInput, value="below", relx=2, rely=23)

        self.buyBand = self.add(userInput, value="lower", relx=2, rely=24, width=7)

        self.buyBandHead = self.add(npyscreen.FixedText, value="Band", relx=9, rely=24, editable=False)



        self.start_button = self.add(npyscreen.ButtonPress, name='Start', relx=4, hidden=False)
        self.start_button.whenPressed = self.start_button_pressed


        ##########

        self.debug = self.add(npyscreen.FixedText, value="debug")

        self.status2 = self.add(npyscreen.FixedText, value="fake status")

        self.statusLine0 = self.add(npyscreen.FixedText, value="2nd status", relx=2, rely=-5, editable=False)

        self.statusLine = self.add(npyscreen.FixedText, value="2nd status", relx=2, rely=-4, editable=False)

        self.statusHead = self.add(npyscreen.FixedText, value="[STATUS]", relx=2, rely=-3, editable=False, color="VERYGOOD")

        self.statusHead2 = self.add(npyscreen.FixedText, value=" ", relx=11, rely=-3, editable=False, color="CAUTIONHL")

        self.status = self.add(npyscreen.FixedText, value="Ready and awaiting orders, Sir [$]◡[$]", relx=13, rely=-3, editable=False)


        self.revalidate()
        self.setIndicatorData()
        self.parentApp.updateDepth()
        #
        #
        # self.debug2 = self.add(npyscreen.FixedText, value=val["coins"][symbol]["tickSize"])
        #
        # self.debug2 = self.add(npyscreen.FixedText, value=len(str(val["coins"][symbol]["tickSize"])))

        # self.testLOL  = self.add(npyscreen.FixedText, value = "#", relx=1, rely=-3)

    def spawn_notify_popup(self, code_of_key_pressed):
        message_to_display = 'I popped up \n passed: {}'.format(code_of_key_pressed)
        npyscreen.notify(message_to_display, title='Popup Title')
        time.sleep(5)  # needed to have it show up for a visible amount of time

    def exit_application(self):
        self.parentApp.setNextForm(None)
        self.editing = False

    def revalidate(self):
        isvalid = self.validateInput()
        if isvalid == "not valid":
            self.status.value = "INPUT NOT VALID"
        else:

            val["buyTarget"] = str(isvalid[0])[:len(str(val["coins"][symbol]["tickSize"]))]
            val["sellTarget"] = str(isvalid[1])[:len(str(val["coins"][symbol]["tickSize"]))]
            # self.debug.value = val["sellTarget"]
            logging.debug("revalidate: buy targget")
            logging.debug(str(self.timeFrame))
            logging.debug(str(val["buyTarget"]))
            logging.debug("revalidate: sell targget")
            logging.debug(str(val["sellTarget"]))


    # START BUTTON PRESSED
    def start_button_pressed(self):
        if self.start_button.name == "Start":
            self.start_button.name = "Stop"
            val["running"] = True
            # debug
            val["initiateBuy"] = True
        else:
            self.start_button.name = "Start"
            val["running"] = False
            cancelAllOrders()

        self.revalidate()


    # TODO: refactor
    def validateInput(self):
        notValid = False

        # CHeck sell percent input
        if isfloat(self.sellPercent.value) and float(self.sellPercent.value) > 0 and float(self.sellPercent.value) < 100:
            userSellPrice = self.sellPercent.value
        else:
            return "not valid"


        # Check buy percent input
        if isfloat(self.buyPercent.value) and float(self.buyPercent.value) > 0 and float(self.buyPercent.value) < 100:
            userBuyPrice = self.buyPercent.value
        else:
            return "not valid"


        # Check sell Band
        if str(self.sellBand.value) == "upper":
            sellBand = "upperBoll"
        elif str(self.sellBand.value) == "middle":
            sellBand = "medBoll"
        elif str(self.sellBand.value) == "lower":
            sellBand = "lowerBoll"
        else:
            return "not valid"

        # Check buy Band
        if str(self.buyBand.value) == "upper":
            buyBand = "upperBoll"
        elif str(self.buyBand.value) == "middle":
            buyBand = "medBoll"
        elif str(self.buyBand.value) == "lower":
            buyBand = "lowerBoll"
        else:
            return "not valid"


        # Check sell operator
        if self.sellAboveBelow.value == "below":
            targetSellPrice = float(val["indicators"][self.timeFrame][sellBand] * (1 - (float(userSellPrice) / 100)))

        elif self.sellAboveBelow.value == "above":
            targetSellPrice = float(val["indicators"][self.timeFrame][sellBand] * (1 + (float(userSellPrice) / 100)))

        else:
            return "not valid"

        # Check buy operator
        if self.buyAboveBelow.value == "below":
            targetBuyPrice = float(val["indicators"][self.timeFrame][buyBand] * (1 - (float(userBuyPrice) / 100)))

        elif self.buyAboveBelow.value == "above":
            targetBuyPrice = float(val["indicators"][self.timeFrame][buyBand] * (1 + (float(userBuyPrice) / 100)))





        if notValid is False:
            logging.debug("User inputs are valid.")
            finaltargetBuyPrice = '{:.8f}'.format(targetBuyPrice)[:len(str(val["coins"][symbol]["tickSize"]))]

            finaltargetSellPrice = '{:.8f}'.format(targetSellPrice)[:len(str(val["coins"][symbol]["tickSize"]))]

            return [finaltargetBuyPrice, finaltargetSellPrice]


        return "not valid"





    def setIndicatorData(self):
        self.upperBoll.value = '{:.8f}'.format(float(val["indicators"][str(self.timeFrame)]["upperBoll"]))[:len(str(val["coins"][symbol]["tickSize"]))]

        self.medBoll.value = '{:.8f}'.format(float(val["indicators"][str(self.timeFrame)]["medBoll"]))[:len(str(val["coins"][symbol]["tickSize"]))]

        self.lowerBoll.value = '{:.8f}'.format(float(val["indicators"][str(self.timeFrame)]["lowerBoll"]))[:len(str(val["coins"][symbol]["tickSize"]))]

        if self.start_button.name == "Stop":
            self.revalidate()
            # self.status.value = "SET BAND INFO"
        try:
            self.sellTargetDisplay.value = str(val["sellTarget"])
            self.buyTargetDisplay.value = str(val["buyTarget"])
        except KeyError:
            self.status.value = "buy/ sell targets not available"


        self.display()


class AlgoBot(npyscreen.NPSAppManaged):

    """MAIN app class."""

    # update interval too low causes bugs?
    keypress_timeout_default = 10


    # initiate Forms on start
    def onStart(self):
        self.addForm("MAIN", AlgoForm, name="Juris beeesr Binance Bot", color="GOOD")


    def periodicUpdate(self):
        self.getForm("MAIN").timeRunning.value = str(datetime.timedelta(seconds=int(val["runTime"])))
        self.getForm("MAIN").display()


    def hardRefresh(self):
        self.getForm("MAIN").DISPLAY()

    def updateDepth(self):
        try:
            self.getForm("MAIN").debug.value = str(val["depthTracker"])
            self.getForm("MAIN").statusLine.value = "Buy under: " + str(val["buyTarget"]) + " order at: " + str(val["realBuyPrice"])
            self.getForm("MAIN").statusLine0.value = "Sell over: " + str(val["sellTarget"]) + " order at: " + str(val["realSellPrice"])
            self.getForm("MAIN").display()

        except KeyError:
            pass


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
            self.parent.status.value = "was anderes"

        self.parent.revalidate()
        self.parent.setIndicatorData()
        self.parent.display()
        # self.parent.status.value = "Timeframe: " + str(self.value)
    tf1m = ["1m", "1 min", "1min", "1minute" "1 minute", "1 Minute"]
    tf5m = ["5", "5m", "5 min", "5min", "5minutes" "5 minutes", "5 Minutes", "5 minuten", "5 Minuten"]
    tf15m = ["15", "15m", "15 min", "15min", "15minutes" "15 minutes", "15 Minutes", "15 minuten", "15 Minuten"]
    tf30m = ["30", "30m", "30 min", "30min", "30minutes" "30 minutes", "30 Minutes", "30 minuten", "30 Minuten"]
    tf1h = ["1h", "1 hour", "1hour", "1 stunde" "1 Stunde"]


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
                "q": self.pressed_q,
                "s": self.pressed_s,
                "I": self.pressed_i,
            }
        )

    def pressed_enter(self, key):
        self.parent.status.value = "pressed enter"

    def pressed_r(self, key):
        self.parent.DISPLAY()

    def pressed_q(self, key):
        cleanExit()
        self.editing = False
        self.parentApp.switchForm(None)

    def pressed_s(self, key):
        self.parent.status.value = "pressed s"

    def pressed_i(self, key):
        npyscreen.notify_confirm("+++ INFO +++\nJuris Binance Boilinger Bot Version 0.1\n \n Achtung: \n Q:     exit program\nS:     start/stop the bot\nR:     refresh the screen\nI: this info window")

    def when_value_edited(self):
        self.parent.start_button.name = "Start"
        val["running"] = False
        cancelAllOrders()


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
