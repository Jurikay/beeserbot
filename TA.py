#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# by Jurek Baumann

"""Convert Binance Kline data to stockstats/ pandas DataFrames and retrieve indicator data."""


# import datetime
import pandas as pd
import stockstats
from botLogic import *

# pandas – Disable chained assignment warnings. Default='warn'
pd.options.mode.chained_assignment = None


# entrypoint
def getTA():
    """Make a kline API call for every time interval.
    Then pass the received data to createFrame.
    """

    # Limit time intervals to the most interesting only
    timeIntervals = ["1m", "5m", "15m", "30m", "1h"]

    # Create a list to store API answers in
    timeFrames = []

    # create a list to store dataframes in
    allDataFrames = []

    # iterate through all time intervals
    for index in enumerate(timeIntervals):

        i = index[0]

        # add an empty lists to timeFrames and allDataFrames
        timeFrames.append([])
        allDataFrames.append([])

        # API CALL: Get kline data for each time interval
        timeFrames[i] = client.get_klines(symbol=val["symbol"], interval=timeIntervals[i])

        # store DataFrames returned from createFrame in allDataFrames
        allDataFrames[i] = createFrame(timeFrames[i], timeIntervals[i])

    # Once DataFrames for all time intervals are available, call interpreteData
    indicatorData = interpreteData(timeIntervals, allDataFrames)

    # Finally return indicator data
    return indicatorData


def createFrame(klines, filename):

    """Create a pandas.DataFrame.

    This object contains historical trading data in the proper format to be interpreted by stockstats.
    """

    # create 7 named empty lists the cool way
    date, amount, closeP, high, low, openP, volume = ([] for i in range(7))

    # iterate through API kline data
    for index in enumerate(klines):

        i = index[0]

        # assign relevant data to lists
        date.append(int(klines[i][6]))
        amount.append(float(klines[i][7]))
        closeP.append(float(klines[i][4]))
        high.append(float(klines[i][2]))
        low.append(float(klines[i][3]))
        openP.append(float(klines[i][1]))
        volume.append(float(klines[i][5]))

    # Create a dict from lists containing the data
    dataTable = {'date': date, 'amount': amount, 'close': closeP, 'high': high, 'low': low, 'open': openP, 'volume': volume}

    # Build a DataFrame 'coinDataFrame' from the dict dataTable
    coinDataFrame = pd.DataFrame(dataTable, columns=['date', 'amount', 'close', 'high', 'low', 'open', 'volume'])

    # return the DataFrame
    return coinDataFrame


def interpreteData(intervals, dataFrames):

    """Use stockstats to get relevant indicator data."""

    # Determine number of decimal places of the considered coin
    tickSize = str(val["coins"][val["symbol"]]["tickSize"])
    roundTo = len(str(tickSize))-2

    indicatorData = dict()

    # iterate through time intervals
    for value in enumerate(intervals):

        i = value[0]

        # Create a StockDataFrame from the respective time interval data
        stock = stockstats.StockDataFrame.retype(dataFrames[i])

        # Calculate chosen indicatorData
        # RSI
        rsi6hData = stock['rsi_6']
        rsi12hData = stock['rsi_12']

        # MACD
        macdData = stock['macd']

        # BOLLINGER BANDS
        medBollData = stock['boll']
        upperBollData = stock['boll_ub']
        lowerBollData = stock['boll_lb']

        # TODO ADD MORE RELEVANT
        volumeDeltaData = stock['volume_delta']

        # get last respective entries from DataFrame
        rsi6h = round(rsi6hData.iloc[-1], 2)
        rsi12h = round(rsi12hData.iloc[-1], 2)

        macd = "{:.8f}".format(macdData.iloc[-1])

        medBoll = round(medBollData.iloc[-1], roundTo)
        upperBoll = round(upperBollData.iloc[-1], roundTo)
        lowerBoll = round(lowerBollData.iloc[-1], roundTo)


        volumeDelta = volumeDeltaData.iloc[-1]

        # For every time interval, add the last value of the
        # chosen indicator to a dictionary as a 'key': value pair
        indicatorData[value[1]] = {"rsi6h": rsi6h, "rsi12h": rsi12h, "medBoll": medBoll, "upperBoll": upperBoll, "lowerBoll": lowerBoll, "volumeDelta": volumeDelta, "macd": macd}

    # return indicator data sorted by timeframe.
    return indicatorData
