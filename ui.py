#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# by Jurek Baumann
import npyscreen
import curses
from colorSyntax import *
import datetime

from botFunctions import *
from botLogic import *
import logging

logging.basicConfig(filename="test.log", level=logging.DEBUG, format='%(asctime)s %(message)s')


'''
COLORS:

    'DEFAULT'     : 'WHITE_BLACK',
    'FORMDEFAULT' : 'WHITE_BLACK',
    'NO_EDIT'     : 'BLUE_BLACK',
    'STANDOUT'    : 'CYAN_BLACK',
    'CURSOR'      : 'WHITE_BLACK',
    'CURSOR_INVERSE': 'BLACK_WHITE',
    'LABEL'       : 'GREEN_BLACK',
    'LABELBOLD'   : 'WHITE_BLACK',
    'CONTROL'     : 'YELLOW_BLACK',
    'IMPORTANT'   : 'GREEN_BLACK',
    'SAFE'        : 'GREEN_BLACK',
    'WARNING'     : 'YELLOW_BLACK',
    'DANGER'      : 'RED_BLACK',
    'CRITICAL'    : 'BLACK_RED',
    'GOOD'        : 'GREEN_BLACK',
    'GOODHL'      : 'GREEN_BLACK',
    'VERYGOOD'    : 'BLACK_GREEN',
    'CAUTION'     : 'YELLOW_BLACK',
    'CAUTIONHL'   : 'BLACK_YELLOW',

'''


class MainForm(npyscreen.FormBaseNew):

    def hotkeyFix(self):
        self.coinPair.value="BUTTON PRESSED"
        logging.debug("BUTTON PRESSED")

    def switchCoin(self):
        self.coinPair.value = "LOADING"
        for i in range(self.obRange*2+5):
            self.oHistory[i] = self.add(npyscreen.FixedText, value="                    ", editable=False, relx=50,rely=i+2)

    gridBuy=True


    #################################################################
    # WHILE WAITING LOOP
    #################################################################
    def while_waiting(self):

        # update buy input coloring
        try:
            buyValidation = validateOrderPrice(self.BuyInput.value, depthMsg["bids"][0][0], depthMsg["asks"][0][0],"BUY")
            if buyValidation == "PERFECT":
                self.BuyInput.color="STANDOUT"
            elif buyValidation == "GOOD":
                self.BuyInput.color="GOOD"
            elif buyValidation == "OK":
                self.BuyInput.color="WARNING"
            else:
                self.BuyInput.color="DANGER"

            sellValidation = validateOrderPrice(self.SellInput.value, depthMsg["bids"][0][0], depthMsg["asks"][0][0],"SELL")
            if sellValidation == "PERFECT":
                self.SellInput.color="STANDOUT"
            elif sellValidation == "GOOD":
                self.SellInput.color="GOOD"
            elif sellValidation == "OK":
                self.SellInput.color="WARNING"
            else:
                self.SellInput.color="DANGER"

        except:
            pass




        self.display()

    #################################################################
    # CREATE FUNCTION
    #################################################################
    def create(self):
        # EXIT APP on ESC
        self.how_exited_handers[npyscreen.wgwidget.EXITED_ESCAPE]  = self.exit_application

        # Add F1 handler to fix display FIXME make it work
        self.add_handlers({"KEY_F(1)": self.hotkeyFix})

        # Add various values TODO add values; implement headlines
        self.coinPair = self.add(npyscreen.FixedText, value=val["symbol"], editable=False, color="WARNING")
        self.timeHeadline = self.add(npyscreen.FixedText, value="Orders:", editable=False)
        self.date_widget = self.add(npyscreen.FixedText, value="LOADING", editable=False)

        self.spacer = self.add(npyscreen.FixedText, value="", editable=False)


        self.timeHeadline = self.add(npyscreen.FixedText, value="Running for:", editable=False)

        self.runningSince = self.add(npyscreen.FixedText, value="0:00:00", editable=False)
        self.spacer = self.add(npyscreen.FixedText, value="", editable=False)

        self.tradesHeadline = self.add(npyscreen.FixedText, value="Trades:", editable=False)
        self.tradesSinceStart = self.add(npyscreen.FixedText, value="0", editable=False)

        self.tpmHeadline = self.add(npyscreen.FixedText, value="Trades per minute:", editable=False)
        self.tpm = self.add(npyscreen.FixedText, value="0", editable=False)

        # initalize variables for various calculations
        self.bids = {}
        self.asks = {}
        self.oHistory = {}
        self.obRange = 5


        # Create asks template
        for i in range(self.obRange):
            self.asks[i] = self.add(SyntaxObAsks,npyscreen.FixedText, value="01 0.00001337 ", editable=False, relx=25,rely=i+2)
            self.asks[i].syntax_highlighting=True

        # Add Spread between asks and bids
        self.spacer = self.add(npyscreen.FixedText, value="", editable=False)
        self.spread = self.add(npyscreen.FixedText, value="Spread", editable=False, relx=25, rely=self.obRange+3)

        # Create bids template
        for i in range(self.obRange):
            self.bids[i] = self.add(SyntaxObBids,npyscreen.FixedText, value="01 0.00001337 ", editable=False, relx=25,rely=i+self.obRange+5)
            self.bids[i].syntax_highlighting=True


        # Create order history template TODO: add quantity and timestamp
        for i in range(self.obRange*2+3):
            self.oHistory[i] = self.add(npyscreen.FixedText, value="+*", editable=False, relx=50,rely=i+2)
            # self.OBasks+str(i) = self.add(npyscreen.FixedText, value="asks "+str(i  ), editable=False)

        # Create Coin input field
        self.coinHeadline = self.add(npyscreen.FixedText, value="Coin:", editable=False, color="WARNING", relx=2, rely=self.obRange*2+5)
        self.editT = self.add(coinInput, value=symbol.strip("BTC"), editable=True, relx=8, rely=self.obRange*2+5)

        # self.spacer = self.add(npyscreen.FixedText, value="", editable=False)


        # BUY / SELL selector; shows price input field
        self.selectBS= self.add(buySellSelector, max_height=2, value = [], name="Pick Several", values = ["Buy","Sell",], scroll_exit=True)

        self.spacer = self.add(npyscreen.FixedText, value="", editable=False)


        # Buy/Sell price inputs (hidden by default)
        self.BuyInputHead = self.add(npyscreen.FixedText, value="Buy up to:", color="GOOD", relx=2, rely=19, editable=False, hidden=True)
        self.BuyInput = self.add(buyInput, value="0.00000000", relx=13, rely=19, color="DEFAULT", hidden=True)

        self.BuyQuantHead = self.add(npyscreen.FixedText, value="Quantity:", color="DEFAULT", relx=2, rely=20, editable=False, hidden=True)
        self.BuyQuant = self.add(buyInput, value="50", relx=13, rely=20, color="DEFAULT", hidden=True)


        self.SellInputHead = self.add(npyscreen.FixedText, value="Sell from:", color="DANGER", relx=2, rely=21, editable=False, hidden=True)
        self.SellInput = self.add(sellInput, value="0.00000000", relx=13, rely=21, color="CRITICAL", hidden=True)

        self.SellQuantHead = self.add(npyscreen.FixedText, value="Quantity:", color="DEFAULT", relx=2, rely=22, editable=False, hidden=True)
        self.SellQuant = self.add(buyInput, value="50", relx=13, rely=22, color="DEFAULT", hidden=True)

        self.spacer = self.add(npyscreen.FixedText, value="", editable=False)

        # Start Button
        self.start_button = self.add(npyscreen.ButtonPress, name = 'Start', relx=4, hidden=True)
        self.start_button.whenPressed = self.start_button_pressed

        self.debug = self.add(npyscreen.FixedText, value="Debug")

        # Status indicator
        self.statusIndicator = self.add(npyscreen.FixedText, value="STATUS:", editable=False, relx=2,rely=-3,color="DANGER")


    def start_button_pressed(self):
        npyscreen.notify_wait("HI")
        # self.start_button.name="lul"
        if self.start_button.name == "Start":
            self.start_button.name="Stop"
        else:
            self.start_button.name="Start"

    # @classmethod
    # def on_ok():
    #     # Do stuff when the OK Button is pressed
    #     npyscreen.notify_confirm("OK Button Pressed!")


    def exit_application(self):
        # curses.beep()
        # npyscreen.notify_wait("Shutting down")

        cleanExit()
        self.editing = False
        self.parentApp.switchForm(None)

# buy/sell order unput field VALIDATE input
class buyInput(npyscreen.Textfield):
    def when_value_edited(self):
        buyValidation = validateOrderPrice(self.value, depthMsg["bids"][0][0], depthMsg["asks"][0][0],"BUY")
        if buyValidation == "PERFECT":
            self.color="STANDOUT"
        elif buyValidation == "GOOD":
            self.color="GOOD"
        elif buyValidation == "OK":
            self.color="WARNING"
        else:
            self.color="DANGER"



class sellInput(npyscreen.Textfield):
    def when_value_edited(self):
        buyValidation = validateOrderPrice(self.value, depthMsg["bids"][0][0], depthMsg["asks"][0][0], "SELL")
        if buyValidation == "PERFECT":
            self.color="STANDOUT"
        elif buyValidation == "GOOD":
            self.color="GOOD"
        elif buyValidation == "OK":
            self.color="WARNING"
        else:
            self.color="DANGER"

# Buy/Sell Selector Class
class buySellSelector(npyscreen.MultiSelect):
    def when_value_edited(self):

        # Hide/Show Buy/Sell input based on selector switches
        if 0 in self.value:
            self.parent.BuyInputHead.hidden=False
            self.parent.BuyInput.hidden=False

            self.parent.BuyQuantHead.hidden=False
            self.parent.BuyQuant.hidden=False

            try:
                self.parent.BuyInput.value=depthMsg["bids"][0][0]
            except:
                pass
        else:
            self.parent.BuyInputHead.hidden=True
            self.parent.BuyInput.hidden=True

            self.parent.BuyQuantHead.hidden=True
            self.parent.BuyQuant.hidden=True

        if 1 in self.value:
            self.parent.SellInputHead.hidden=False
            self.parent.SellInput.hidden=False

            self.parent.SellQuantHead.hidden=False
            self.parent.SellQuant.hidden=False

            try:
                self.parent.SellInput.value=depthMsg["asks"][0][0]
            except:
                pass
        else:
            self.parent.SellInputHead.hidden=True
            self.parent.SellInput.hidden=True

            self.parent.SellQuantHead.hidden=True
            self.parent.SellQuant.hidden=True

        # Show/ Hide start button
        if self.value != []:
            self.parent.start_button.hidden=False
        else:
            self.parent.start_button.hidden=True

        self.parent.display()

# Coin Input class
class coinInput(npyscreen.Textfield):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_handlers(
            {
                curses.ascii.NL: self.do_something,
                curses.ascii.CR: self.do_something,
                curses.KEY_ENTER:self.do_something

            }
        )
        # npyscreen.notify_wait("EDITED")

        # TODO Compare with accepted pairs/val["coins"]
        # self.value="VAL"


    # CHANGE COIN
    def do_something(self, inputVal):
        if str(self.value).upper() + str("BTC") in val["coins"] and self.value + str("BTC") != val["symbol"]:
            val["symbol"] = str(self.value).upper() + str("BTC")
            self.color="DEFAULT"

            # logging.debug("triggere clearDepth")
            # clearDepth()
            restartSocket(str(val["symbol"]))
            npyscreen.notify_wait("Switching to " + str(self.value) + " please wait...")

            #
            # self.parent.clearOrderBook()
            fetchDepth(str(val["symbol"]))
            logging.debug("LÖSCHE GLOBALLIST!!!")
            del globalList[0:len(globalList)]
            fillList(str(val["symbol"]))
            app.updateDepth()
            self.parent.coinPair.value=str(val["symbol"])

            val["cs"]=0

        elif self.value + str("BTC") != val["symbol"]:
            npyscreen.notify_wait("Was soll " + str(self.value) + " bitte für eine Coin sein?")
        # bm.stop_socket(conn_key)
        else:
            pass

    def when_value_edited(self):
        if str(self.value).upper() + str("BTC") in val["coins"]:
            self.color="LABEL"
            self.value= str(self.value).upper()
        elif len(str(self.value)) < 6:
            self.color="WARNING"

        else:
            self.color="DANGER"
# npyscreen App Class
class MainApp(npyscreen.NPSAppManaged):

    # update interval too low causes bugs?
    keypress_timeout_default = 5

    # initiate Forms on start
    def onStart(self):
        self.addForm("MAIN", MainForm, name="Juris beeesr Binance Bot", color="STANDOUT")


    def updateDepth(self):
        # self.getForm("MAIN").statusIndicator.color="VERYGOOD"
        with lock:
            # logging.debug("testzugriff start")
            try:
                self.getForm("MAIN").date_widget.value=str(depthMsg["lastUpdateId"])
                if str(depthMsg["lastUpdateId"]) == "WAITING":
                    self.getForm("MAIN").date_widget.color="DANGER"
                    self.getForm("MAIN").statusIndicator.color="CRITICAL"
                else:
                    self.getForm("MAIN").date_widget.color="DEFAULT"
                    self.getForm("MAIN").statusIndicator.color="VERYGOOD"


                    self.getForm("MAIN").runningSince.value = str(datetime.timedelta(seconds=int(val["s"])))

                # update Orderbook
                for i in range(self.getForm("MAIN").obRange):

                    self.getForm("MAIN").bids[i].value ="[" + str((i+1)).zfill(1)+ "]" + str(depthMsg["bids"][i][0]) + " | " + str(float(depthMsg["bids"][i][1])).ljust(6,"0")

                    self.getForm("MAIN").asks[i].value ="[" + str((self.getForm("MAIN").obRange-i)).zfill(1)+ "]" + str(depthMsg["asks"][self.getForm("MAIN").obRange-i-1][0]) + " | " + str(float(depthMsg["asks"][self.getForm("MAIN").obRange-i-1][1])).ljust(6,"0")
            except:
                pass
            # update spread
            try:
                self.spreadVal = ((float(depthMsg["asks"][0][0])-float(depthMsg["bids"][0][0]))/float(depthMsg["asks"][0][0]))*100
                self.getForm("MAIN").spread.value = "Spread: " + str(round(self.spreadVal,2))+"%"
            except:
                pass

            # Update trade history values
            try:
                # logging.debug("DRAWE ORDER HISTORY")

                for i in range(13):
                    if globalList[i]["order"] == "True":
                        # logging.debug("order True")

                        self.getForm("MAIN").oHistory[i].value=str(globalList[i]["price"])
                        self.getForm("MAIN").oHistory[i].color="DANGER"
                    elif globalList[i]["order"] == "False":
                        # logging.debug("order False")
                        self.getForm("MAIN").oHistory[i].value=str(globalList[i]["price"])
                        self.getForm("MAIN").oHistory[i].color="GOOD"
                    else:
                        # overwriting empty values
                        self.getForm("MAIN").oHistory[i].value="          "

            except Exception as err:
                logging.debug("UPDATE_ERROR: " + str(err))

            try:
                self.getForm("MAIN").display()
            except:
                pass



    def setStatus(self, statusStr, statusTitle):
        with lock:
            self.getForm("MAIN").statusBar.name=str(statusTitle)
            self.getForm("MAIN").statusBar.value=" " + str(statusTitle)

            # try:
            #     self.getForm("MAIN").display()
            # except:
            #     pass


    def periodicUpdate(self):
        logging.debug("periodic update")
        # self.getForm("MAIN").coinPair.value = str(tickerMsg["s"])
        self.getForm("MAIN").runningSince.value = str(datetime.timedelta(seconds=int(val["s"])))

        try:
            self.getForm("MAIN").tpm.value =  int(float(len(globalList))/(float(int(val["cs"])/60)))
        except:
            pass
        self.getForm("MAIN").display()



    def hardRefresh(self):
        self.getForm("MAIN").DISPLAY()

    def refreshDisplay(self):
        self.getForm("MAIN").display()

app = MainApp()
