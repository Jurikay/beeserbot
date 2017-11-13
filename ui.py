#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# by Jurek Baumann
import npyscreen
import curses
from colorSyntax import *
from botFunctions import *
from botLogic import *
import logging

logging.basicConfig(filename="test.log", level=logging.DEBUG, format='%(asctime)s %(message)s')



class MainForm(npyscreen.FormBaseNew):


    gridBuy=True
    # set (update) values periodically when no user input is present
    # Form idle loop

    @staticmethod
    def updateOrderbook(self):
        logging.debug("UPDATE ORDERBOOK!!!" + str(self))
        # Update order book values
        for i in range(self.obRange):
            self.bids[i].value ="[" + str((i+1)).zfill(1)+ "]" + str(depthMsg["bids"][i][0]) + " | " + str(float(depthMsg["bids"][i][1])).ljust(6,"0")

            self.asks[i].value ="[" + str((self.obRange-i)).zfill(1)+ "]" + str(depthMsg["asks"][self.obRange-i-1][0]) + " | " + str(float(depthMsg["asks"][self.obRange-i-1][1])).ljust(6,"0")


    #################################################################
    # WHILE WAITING LOOP
    #################################################################
    def while_waiting(self):
    #
    #     # Catch KeyError if websocket update hasn't occured yet
    #     try:
    #         logging.debug("drawe changes")
    #
    #         self.coinPair.value = str(tickerMsg["s"])
    #         # update values from websocket data, stored in "global" dictionary
    #         #npyscreen.notify_wait(str(temp["lastUpdateId"]))
    #
    #         # self.date_widget.value = str(depthMsg["lastUpdateId"])
    #
    #
    #         self.runningSince.value = str(datetime.timedelta(seconds=int(val["s"])))
    #
    #         try:
    #             self.tpm.value =  int(float(len(globalList))/(float(int(val["cs"])/60)))
    #         except:
    #             pass
    #
    #         # Update order book values
    #         # for i in range(self.obRange):
    #         #     self.bids[i].value ="[" + str((i+1)).zfill(1)+ "]" + str(depthMsg["bids"][i][0]) + " | " + str(float(depthMsg["bids"][i][1])).ljust(6,"0")
    #         #
    #         #     self.asks[i].value ="[" + str((self.obRange-i)).zfill(1)+ "]" + str(depthMsg["asks"][self.obRange-i-1][0]) + " | " + str(float(depthMsg["asks"][self.obRange-i-1][1])).ljust(6,"0")
    #
    #
    #         self.clearOb()
    #         # Update trade history values
    #         try:
    #             for i in range(self.obRange*2+3):
    #                 # self.oHistory[i].value = str(globalList[i])
    #                 # with open("myfile2.txt", "w") as f:
    #                 #     f.write(str(globalList))
    #
    #                 if globalList[i]["order"] == "True":
    #                     self.oHistory[i] = self.add(SyntaxHistSell, npyscreen.FixedText, value=str(globalList[i]["price"])+"  "+str(float(globalList[i]["quantity"])).ljust(5,"0"), editable=False, relx=50,rely=i+2)
    #                 else:
    #                     self.oHistory[i] = self.add(SyntaxHistBuy, npyscreen.FixedText, value=str(globalList[i]["price"])+"  "+str(float(globalList[i]["quantity"])).ljust(5,"0"), editable=False, relx=50,rely=i+2)
    #                 self.oHistory[i].syntax_highlighting=True
    #
    #         except:
    #             pass
    #
    #         # Update trades, spread
    #         self.tradesSinceStart.value = str(len(globalList))
    #         try:
    #             self.spreadVal = ((float(depthMsg["asks"][0][0])-float(depthMsg["bids"][0][0]))/float(depthMsg["asks"][0][0]))*100
    #             self.spread.value = "Spread: " + str(round(self.spreadVal,2))+"%"
    #         except:
    #             pass
    #
    #         self.display()
    #     except KeyError:
    #         #print ("error")
    #         pass

        # commit updates and refresh view
        self.display()
    #################################################################
    # CREATE FUNCTION
    #################################################################
    def create(self):
        # EXIT APP on ESC
        self.how_exited_handers[npyscreen.wgwidget.EXITED_ESCAPE]  = self.exit_application

        self.coinPair = self.add(npyscreen.FixedText, value="COINPAIR", editable=False, color="WARNING")
        # initialize values. Later to be replaced by WebSocket data
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


        self.bids = {}
        self.asks = {}
        self.oHistory = {}
        self.obRange = 6

        for i in range(self.obRange):
            self.asks[i] = self.add(SyntaxObAsks,npyscreen.FixedText, value="01 0.00001337 ", editable=False, relx=25,rely=i+2)
            self.asks[i].syntax_highlighting=True


        self.spacer = self.add(npyscreen.FixedText, value="", editable=False)
        self.spread = self.add(npyscreen.FixedText, value="Spread", editable=False, relx=25, rely=self.obRange+3)


        for i in range(self.obRange):
            self.bids[i] = self.add(SyntaxObBids,npyscreen.FixedText, value="01 0.00001337 ", editable=False, relx=25,rely=i+self.obRange+5)
            self.bids[i].syntax_highlighting=True



        # for i in range(self.obRange*2+3):
        #     self.oHistory[i] = self.add(npyscreen.FixedText, value="+*", editable=False, relx=50,rely=i+2)
        #     # self.OBasks+str(i) = self.add(npyscreen.FixedText, value="asks "+str(i  ), editable=False)

        self.editT = self.add(coinInput, value=symbol.strip("BTC"), editable=True, name="Coin",begin_entry_at=7, two_lines=None)

        # self.spacer = self.add(npyscreen.FixedText, value="", editable=False)

        self.selectBS= self.add(npyscreen.MultiSelect, max_height=2, value = [], name="Pick Several", values = ["Buy","Sell",], scroll_exit=True)

        self.spacer = self.add(npyscreen.FixedText, value="", editable=False)


        # self.Debug = self.add(npyscreen.FixedText, value="")


        self.start_button = self.add(npyscreen.ButtonPress, name = 'Start', relx=1)
        self.start_button.whenPressed = self.start_button_pressed

        self.statusBar = self.add(npyscreen.TitleText, name="status:", value="hier ist der status", editable=False, color="VERYGOOD", display_value="asdasddas", rely=-3, relx=3, begin_entry_at=11)

    def clearOb(self):
        for i in range(self.obRange*2+5):
            self.oHistory[i] = self.add(npyscreen.FixedText, value="                    ", editable=False, relx=50,rely=i+2)
        #self.editW = self.add(npyscreen.



    def start_button_pressed(self):
        npyscreen.notify_wait("HI")
        self.start_button.name="lul"


    def on_ok(self):
        # Do stuff when the OK Button is pressed
        npyscreen.notify_confirm("OK Button Pressed!")


    def exit_application(self):
        # curses.beep()

        self.editing = False
        self.parentApp.switchForm(None)
        cleanExit()


class coinInput(npyscreen.Textfield):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_handlers(
            {
                curses.ascii.NL: self.do_something,
                curses.ascii.CR: self.do_something,
                curses.KEY_ENTER:self.do_something,
                '^F':            self.do_something
            }
        )
        # npyscreen.notify_wait("EDITED")

        # TODO Compare with accepted pairs/coins
        # self.value="VAL"


    def do_something(self, input):

        # depthMsg=dict()
        # npyscreen.notify_confirm(str(conn_key))
        if str(self.value).upper() + str("BTC") in coins and self.value + str("BTC") != val["symbol"]:
            val["symbol"] = str(self.value).upper() + str("BTC")
            self.color="DEFAULT"

            restartSocket(str(val["symbol"]))
            # npyscreen.notify_wait("Switche coin... ")

            self.parent.clearOb()
            val["cs"]=0

        else:
            curses.beep()
        # bm.stop_socket(conn_key)


    def when_value_edited(self):
        if str(self.value).upper() + str("BTC") in coins:
            self.color="LABEL"
        else:
            self.color="WARNING"

# npyscreen App Class
class MainApp(npyscreen.NPSAppManaged):

    # update interval
    keypress_timeout_default = 5

    # initiate Forms on start
    def onStart(self):
        self.addForm("MAIN", MainForm, name="BEESER BOT")


    def testZugriff(self):
        with lock:
            logging.debug("testzugriff start")
            self.getForm("MAIN").date_widget.value = str(depthMsg["lastUpdateId"])

            self.getForm("MAIN").runningSince.value = str(datetime.timedelta(seconds=int(val["s"])))

            for i in range(self.getForm("MAIN").obRange):

                self.getForm("MAIN").bids[i].value ="[" + str((i+1)).zfill(1)+ "]" + str(depthMsg["bids"][i][0]) + " | " + str(float(depthMsg["bids"][i][1])).ljust(6,"0")

                self.getForm("MAIN").asks[i].value ="[" + str((self.getForm("MAIN").obRange-i)).zfill(1)+ "]" + str(depthMsg["asks"][self.getForm("MAIN").obRange-i-1][0]) + " | " + str(float(depthMsg["asks"][self.getForm("MAIN").obRange-i-1][1])).ljust(6,"0")
        # self.getForm("MAIN").display()

        logging.debug("testzugriff end")

app = MainApp()
