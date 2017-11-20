import npyscreen
import curses
from colorSyntax import *
import datetime

from botFunctions import *
from botLogic import *
import logging

class MainForm(npyscreen.FormBaseNew):
    """
    Main Form Class of npyscreen.

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
    """
    # Overload init function to add key handlers
    def __init__(self, *args, **keywords):
        super(npyscreen.FormBaseNew, self).__init__(*args, **keywords)
        self.add_handlers(
            {

                curses.KEY_F1: self.start_button_pressed,
                curses.KEY_F2: self.select_switcher,
                "r": self.hotkeyFix
            }
        )


    def select_switcher(self, keyCode):
        # self.coinPair.value = str(self.editw)
        # self.selectBS.hidden=True
        self.editw = 37
        self.how_exited = False
        self.SellQuant.editing = False
        self.BuyInput.editing = False
        self.selectBS.editing = False
        # self.selectBS.get_content().hidden=True
        self.selectBS.h_select_exit(None)
        self.editw = 37
        self.selectBS.editing = False
        # self.selectBS.hidden=False

        # self.h_exit_down()

        # self.editT.edit()


    def hotkeyFix(self, keyCode):
        self.DISPLAY()

    def switchCoin(self):
        self.coinPair.value = "LOADING"

        for i in range(self.obRange*2+5):
            self.oHistory[i] = self.add(npyscreen.FixedText, value="                    ", editable=False, relx=50, rely=i+2)

    gridBuy = True


    #################################################################
    # WHILE WAITING LOOP
    #################################################################
    def while_waiting(self):
        # update buy input coloring
        try:
            buyValidation = validateOrderPrice(self.BuyInput.value, depthMsg["bids"][0][0], depthMsg["asks"][0][0], "BUY")
            if buyValidation == "PERFECT":
                self.BuyInput.color = "STANDOUT"
            elif buyValidation == "GOOD":
                self.BuyInput.color = "GOOD"
            elif buyValidation == "OK":
                self.BuyInput.color = "WARNING"
            else:
                self.BuyInput.color = "DANGER"

            sellValidation = validateOrderPrice(self.SellInput.value, depthMsg["bids"][0][0], depthMsg["asks"][0][0], "SELL")
            if sellValidation == "PERFECT":
                self.SellInput.color = "STANDOUT"
            elif sellValidation == "GOOD":
                self.SellInput.color = "GOOD"
            elif sellValidation == "OK":
                self.SellInput.color = "WARNING"
            else:
                self.SellInput.color = "DANGER"

            if str(self.date_widget.value) != str("WAITING") and self.status.value == "Waiting for Websocket...":
                self.status.value = "just watching the market"

            # indicator test
            try:
                self.debug.value=val["indicators"]["1m"]["medBoll"]
            except TypeError:
                self.debug.value="Type Error"

        except KeyError:
            pass




        self.display()

    #################################################################
    # CREATE FUNCTION
    #################################################################
    def create(self):
        # EXIT APP on ESC
        self.how_exited_handers[npyscreen.wgwidget.EXITED_ESCAPE] = self.exit_application


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

        # ORDERBOOK

        # Create asks template
        for i in range(self.obRange):
            self.asks[i] = self.add(SyntaxObAsks, npyscreen.FixedText, value="01 0.00001337 ", editable=False, relx=25, rely=i+2)
            self.asks[i].syntax_highlighting = True

        # Add Spread between asks and bids
        self.spacer = self.add(npyscreen.FixedText, value="", editable=False)
        self.spread = self.add(npyscreen.FixedText, value="Spread", editable=False, relx=25, rely=self.obRange+3)

        # Create bids template
        for i in range(self.obRange):
            self.bids[i] = self.add(SyntaxObBids, npyscreen.FixedText, value="01 0.00001337 ", editable=False, relx=25, rely=i+self.obRange + 5)
            self.bids[i].syntax_highlighting = True


        # Create order history template TODO: add quantity and timestamp
        for i in range(self.obRange*2+3):
            self.oHistory[i] = self.add(npyscreen.FixedText, value="+*", editable=False, relx=50, rely=i+2)
            # self.OBasks+str(i) = self.add(npyscreen.FixedText, value="asks "+str(i  ), editable=False)

        # Create Coin input field
        self.coinHeadline = self.add(npyscreen.FixedText, value="Coin:", editable=False, color="WARNING", relx=2, rely=self.obRange*2+5)


        self.editT = self.add(coinInput, value=str(val["symbol"])[:-3], editable=True, relx=8, rely=self.obRange*2+5)

        # self.spacer = self.add(npyscreen.FixedText, value="", editable=False)


        # BUY / SELL selector; shows price input field
        self.selectBS = self.add(buySellSelector, max_height=2, value=[], name="Pick Several", values=["Buy", "Sell", ], scroll_exit=True)

        self.spacer = self.add(npyscreen.FixedText, value="", editable=False)


        # Buy/Sell price inputs (hidden by default)
        self.BuyInputHead = self.add(npyscreen.FixedText, value="Buy up to:", color="GOOD", relx=2, rely=19, editable=False, hidden=True)
        self.BuyInput = self.add(buyInput, value="0.00000000", relx=13, rely=19, color="GOOD", hidden=True)

        self.BuyQuantHead = self.add(npyscreen.FixedText, value="Quantity:", color="DEFAULT", relx=2, rely=20, editable=False, hidden=True)
        self.BuyQuant = self.add(orderSizeInput, value="50", relx=13, rely=20, color="GOOD", hidden=True)


        self.SellInputHead = self.add(npyscreen.FixedText, value="Sell from:", color="DANGER", relx=2, rely=21, editable=False, hidden=True)
        self.SellInput = self.add(sellInput, value="0.00000000", relx=13, rely=21, color="GOOD", hidden=True)

        self.SellQuantHead = self.add(npyscreen.FixedText, value="Quantity:", color="DEFAULT", relx=2, rely=22, editable=False, hidden=True)
        self.SellQuant = self.add(orderSizeInput, value="50", relx=13, rely=22, color="GOOD", hidden=True)

        self.spacer = self.add(npyscreen.FixedText, value="", editable=False)

        # Start Button
        self.start_button = self.add(npyscreen.ButtonPress, name='Start', relx=4, hidden=True)
        self.start_button.whenPressed = self.start_button_pressed

        self.debug = self.add(npyscreen.FixedText, value="Debug", editable=False)

        # Status indicator
        self.statusIndicator = self.add(npyscreen.FixedText, value="STATUS:", editable=False, relx=2, rely=-3, color="DANGER")

        self.status = self.add(npyscreen.FixedText, value="Ready and awaiting orders, General", editable=False, relx=10, rely=-3)

        self.indicator = self.add(npyscreen.FixedText, value="#", editable=False, relx=-5, rely=-3)




    def start_button_pressed(self, *keyCode):
        # npyscreen.notify_wait("HI")
        # self.start_button.name="lul"
        if str(depthMsg["lastUpdateId"]) == "WAITING":
            self.status.value = "Websocket connection not established..."
        else:
            if self.start_button.name == "Start":
                self.start_button.name = "Stop "

                if 0 in self.selectBS.value and 1 in self.selectBS.value:
                    val["tryToBuy"] = True
                    val["tryToSell"] = True
                    self.status.value = "looking to buy and sell.."

                elif 0 in self.selectBS.value:
                    val["tryToBuy"] = True
                    val["tryToSell"] = False
                    self.status.value = "looking to buy.."
                elif 1 in self.selectBS.value:
                    val["tryToSell"] = True
                    val["tryToSBuy"] = False
                    self.status.value = "looking to sell.."




            else:
                self.start_button.name = "Start"
                val["tryToBuy"] = False
                val["tryToSell"] = False
                self.status.value = "just watching the market"

    # @classmethod
    # def on_ok():
    #     # Do stuff when the OK Button is pressed
    #     npyscreen.notify_confirm("OK Button Pressed!")


    def turnSelectorOff(self):
        self.selectBS.value = []

        self.BuyInputHead.hidden = True
        self.BuyInput.hidden = True

        self.BuyQuantHead.hidden = True
        self.BuyQuant.hidden = True

        self.SellInputHead.hidden = True
        self.SellInput.hidden = True

        self.SellQuantHead.hidden = True
        self.SellQuant.hidden = True

        self.start_button.hidden = True
        val["tryT0Buy"] = False
        val["tryT0Sell"] = False
        self.status.value = "Waiting for Websocket..."
        self.statusIndicator.color = "CRITICAL"

    def exit_application(self):
        # curses.beep()
        # npyscreen.notify_wait("Shutting down")

        cleanExit()
        self.editing = False
        self.parentApp.switchForm(None)


class orderSizeInput(npyscreen.Textfield):

    """Input field class for defining the order size.

    Input is evaluated and colorized
    """

    def when_value_edited(self):
        """Fire when value is edited."""
        # TODO: refactor
        self.value = self.value
        sizeValidation = validateOrderSize(self.value, val["symbol"], val["priceList"], "0.021")
        if sizeValidation == "PERFECT":
            self.color = "STANDOUT"
        elif sizeValidation == "GOOD":
            self.color = "GOOD"
        elif sizeValidation == "OK":
            self.color = "WARNING"
        else:
            self.color = "DANGER"

        minTrade = float(val["coins"][symbol]["minTrade"])
        roundTo = len(str(minTrade))

        # Doesn't work like this
        # Must be something like so:
        # get self.value until ., count from . limit length to length before point + point + roundto - 2
        if len(self.value) > roundTo:
            self.value = self.value[:-(len(self.value)-roundTo)]


class buyInput(npyscreen.Textfield):

    """Input field class for defining the order price.

    Input is evaluated and colorized
    """

    def when_value_edited(self):
        """Fire when value is edited."""
        try:
            buyValidation = validateOrderPrice(self.value, depthMsg["bids"][0][0], depthMsg["asks"][0][0], "BUY")
            if buyValidation == "PERFECT":
                self.color = "STANDOUT"
            elif buyValidation == "GOOD":
                self.color = "GOOD"
            elif buyValidation == "OK":
                self.color = "WARNING"
            else:
                self.color = "DANGER"
        except KeyError:
            pass



class sellInput(npyscreen.Textfield):

    """Input field intended for sell order price."""

    def when_value_edited(self):
        """Fire when value is edited."""
        try:
            buyValidation = validateOrderPrice(self.value, depthMsg["bids"][0][0], depthMsg["asks"][0][0], "SELL")
            if buyValidation == "PERFECT":
                self.color = "STANDOUT"
            elif buyValidation == "GOOD":
                self.color = "GOOD"
            elif buyValidation == "OK":
                self.color = "WARNING"
            else:
                self.color = "DANGER"
        except KeyError:
            pass

# Buy/Sell Selector Class
class buySellSelector(npyscreen.MultiSelect):

    """Create a buy / sell selector that triggers several input fields."""

    def when_value_edited(self):

        # Hide/Show Buy/Sell input based on selector switches
        if 0 in self.value:
            self.parent.BuyInputHead.hidden = False
            self.parent.BuyInput.hidden = False

            self.parent.BuyQuantHead.hidden = False
            self.parent.BuyQuant.hidden = False

            try:
                self.parent.BuyInput.value = str(depthMsg["bids"][0][0])
                self.parent.BuyQuant.value = str(calculateMinOrderSize(val["symbol"], val["priceList"]))
            except KeyError:
                pass
        else:
            self.parent.BuyInputHead.hidden = True
            self.parent.BuyInput.hidden = True

            self.parent.BuyQuantHead.hidden = True
            self.parent.BuyQuant.hidden = True

        if 1 in self.value:
            self.parent.SellInputHead.hidden = False
            self.parent.SellInput.hidden = False

            self.parent.SellQuantHead.hidden = False
            self.parent.SellQuant.hidden = False

            # TODO: Fix
            try:
                self.parent.SellInput.value = str(depthMsg["asks"][0][0])  # float(val["coins"][val["symbol"]]["ticksize"]))
            except KeyError:
                pass
        else:
            self.parent.SellInputHead.hidden = True
            self.parent.SellInput.hidden = True

            self.parent.SellQuantHead.hidden = True
            self.parent.SellQuant.hidden = True

        # Show/ Hide start button
        if self.value != []:
            self.parent.start_button.hidden = False
        else:
            self.parent.start_button.hidden = True

        self.parent.display()



class coinInput(npyscreen.Textfield):

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
        # npyscreen.notify_wait("EDITED")

        # TODO Compare with accepted pairs/val["coins"]
        # self.value="VAL"


    def key_pressed(self, inputVal):
        npyscreen.notify_wait(str(inputVal))
        self.parent.parentApp.hardRefresh()
        # self.value = self.value[:-1]

    # CHANGE COIN
    def change_coin(self, inputVal):
        if str(self.value).upper() + str("BTC") in val["coins"] and self.value + str("BTC") != val["symbol"]:
            val["symbol"] = str(self.value).upper() + str("BTC")
            self.color = "DEFAULT"

            self.parent.coinPair.value = str(val["symbol"])

            # unselect buy/sell and hide input fields and start button
            self.parent.turnSelectorOff()
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


            val["cs"] = 0

        elif self.value + str("BTC") != val["symbol"]:
            npyscreen.notify_wait("Was soll " + str(self.value) + " bitte für eine Coin sein?")
        # bm.stop_socket(conn_key)
        else:
            pass

    def when_value_edited(self):
        self.value = self.value
        if str(self.value).upper() + str("BTC") in val["coins"]:
            self.color = "LABEL"
            self.value = str(self.value).upper()
        elif len(str(self.value)) < 6:
            self.color = "WARNING"

        else:
            self.color = "DANGER"


class MainApp(npyscreen.NPSAppManaged):

    """MAIN app class."""

    # update interval too low causes bugs?
    keypress_timeout_default = 5


    # initiate Forms on start
    def onStart(self):
        self.addForm("MAIN", MainForm, name="Juris beeesr Binance Bot", color="STANDOUT")


    # TODO: seperate concerns
    def updateDepth(self):
        # self.getForm("MAIN").statusIndicator.color="VERYGOOD"
        with lock:
            # logging.debug("testzugriff start")
            try:
                self.getForm("MAIN").date_widget.value = str(depthMsg["lastUpdateId"])
                if str(depthMsg["lastUpdateId"]) == "WAITING":
                    # self.getForm("MAIN").date_widget.color = "DANGER"
                    self.getForm("MAIN").statusIndicator.color = "CRITICAL"
                else:
                    # self.getForm("MAIN").date_widget.color = "DEFAULT"
                    self.getForm("MAIN").statusIndicator.color = "VERYGOOD"
                    self.getForm("MAIN").runningSince.value = str(datetime.timedelta(seconds=int(val["s"])))

                # update Orderbook
                for i in range(self.getForm("MAIN").obRange):

                    self.getForm("MAIN").bids[i].value = "[" + str((i+1)).zfill(1) + "]" + str(depthMsg["bids"][i][0]) + " | " + str(float(depthMsg["bids"][i][1])).ljust(6, "0")

                    self.getForm("MAIN").asks[i].value = "[" + str((self.getForm("MAIN").obRange-i)).zfill(1) + "]" + str(depthMsg["asks"][self.getForm("MAIN").obRange-i-1][0]) + " | " + str(float(depthMsg["asks"][self.getForm("MAIN").obRange-i-1][1])).ljust(6, "0")
            except (KeyError, NameError):
                pass
            # update spread
            try:
                self.spreadVal = ((float(depthMsg["asks"][0][0])-float(depthMsg["bids"][0][0]))/float(depthMsg["asks"][0][0]))*100
                self.getForm("MAIN").spread.value = "Spread: " + str(round(self.spreadVal, 2))+"%"
            except (KeyError, ZeroDivisionError):
                pass

            # Update trade history values
            try:
                # logging.debug("DRAWE ORDER HISTORY")

                for i in range(13):
                    if globalList[i]["order"] == "True":
                        # logging.debug("order True")

                        self.getForm("MAIN").oHistory[i].value = str(globalList[i]["price"])
                        self.getForm("MAIN").oHistory[i].color = "DANGER"
                    elif globalList[i]["order"] == "False":
                        # logging.debug("order False")
                        self.getForm("MAIN").oHistory[i].value = str(globalList[i]["price"])
                        self.getForm("MAIN").oHistory[i].color = "GOOD"
                    else:
                        # overwriting empty values
                        self.getForm("MAIN").oHistory[i].value = "          "

            except Exception as err:
                logging.debug("UPDATE_ERROR: " + str(err))

            try:
                self.getForm("MAIN").display()
            except KeyError:
                pass



    def setStatus(self, statusStr, statusTitle):
        with lock:
            self.getForm("MAIN").statusBar.name = str(statusTitle)
            self.getForm("MAIN").statusBar.value = " " + str(statusTitle)

            # try:
            #     self.getForm("MAIN").display()
            # except:
            #     pass


    # TODO: check for refactor
    def periodicUpdate(self):
        # logging.debug("periodic update")
        # self.getForm("MAIN").coinPair.value = str(tickerMsg["s"])
        self.getForm("MAIN").runningSince.value = str(datetime.timedelta(seconds=int(val["s"])))

        try:
            self.getForm("MAIN").tpm.value = int(float(len(globalList))/(float(int(val["cs"])/60)))
        except (KeyError, ZeroDivisionError):
            pass
        self.getForm("MAIN").display()



    def hardRefresh(self):
        self.getForm("MAIN").DISPLAY()

    def refreshDisplay(self):
        self.getForm("MAIN").display()

app = MainApp()
