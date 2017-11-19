#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# by Jurek Baumann

from botLogic import *
import datetime
import pandas as pd

def klinesToCsv(klines, filename):

    """Make a .csv file named COINPAIR+Interval.csv.

    This file contains historical trading data in the proper format to be interpreted by stockstats
    """

    # create 7 empty lists the cool way
    date, amount, closeP, high, low, openP, volume = ([] for i in range(7))

    for index in enumerate(klines):
        i = index[0]

        date.append(datetime.datetime.fromtimestamp(int(str(klines[i][6])[:-3])))
        amount.append(klines[i][7])
        closeP.append(klines[i][4])
        high.append(klines[i][2])
        low.append(klines[i][3])
        openP.append(klines[i][1])
        volume.append(klines[i][5])

    # Make a dict from lists containing the data
    dataTable = { 'date':date, 'amount':amount, 'close':closeP, 'high':high, 'low':low, 'open':openP, 'volume':volume }

    # Build a DataFrame 'coinDataFrame' from dict dataTable
    coinDataFrame = pd.DataFrame(dataTable, columns=['date', 'amount', 'close', 'high', 'low', 'open', 'volume'])

    # Build the filename
    file_name = str(symbol) + str(filename) + ".csv"

    # Export DataFrame to csv
    coinDataFrame.to_csv(file_name, index=False, encoding='utf-8')


def createCSV():

    """Make a kline API call for every time interval.

    Then pass the received data to klinesToCsv.
    """

    timeFrames = []

    tfIntervals = ["1m", "5m", "15m", "30m", "1h", "2h", "1d"]

    for index in enumerate(tfIntervals):

        timeFrames.append([])

        i = index[0]

        timeFrames[i] = client.get_klines(symbol=val["symbol"], interval=tfIntervals[i])

        klinesToCsv(timeFrames[i], tfIntervals[i])


createCSV()
