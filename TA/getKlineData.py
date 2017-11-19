import pandas as pd

from binance.client import Client
from binance.websockets import BinanceSocketManager
from binance.enums import *

from config import *

import datetime

client = Client(api_key, api_secret)

bm = BinanceSocketManager(client)

symbol = 'BNBBTC'
print ("Creating csv files for " + symbol)


klines1 = client.get_klines(symbol=symbol, interval="1m")
klines5 = client.get_klines(symbol=symbol, interval="5m")
klines15 = client.get_klines(symbol=symbol, interval="15m")
klines30 = client.get_klines(symbol=symbol, interval="30m")
klines1h = client.get_klines(symbol=symbol, interval="1h")
klines2h = client.get_klines(symbol=symbol, interval="2h")
klines1d = client.get_klines(symbol=symbol, interval="1d")


timeFrames = [klines1, klines5, klines15, klines30, klines1h, klines2h, klines1d]

tfIntervals = ["1m", "5m", "15m", "30m", "1h", "2h", "1d"]


def klinesToCsv(klines, filename):

    date= list()
    amount= list()
    closeP= list()
    high= list()
    low= list()
    openP= list()
    volume = list()

    for index in enumerate(klines):
        date.append(datetime.datetime.fromtimestamp(int(str(klines[index[0]][6])[:-3])))
        amount.append(klines[index[0]][7])
        closeP.append(klines[index[0]][4])
        high.append(klines[index[0]][2])
        low.append(klines[index[0]][3])
        openP.append(klines[index[0]][1])
        volume.append(klines[index[0]][5])

    dataTable = { 'date':date, 'amount':amount, 'close':closeP, 'high':high, 'low':low, 'open':openP, 'volume':volume }

    # Build a DataFrame coinDataFrame from dict dataTable
    coinDataFrame = pd.DataFrame(dataTable, columns=['date', 'amount', 'close', 'high', 'low', 'open', 'volume'])

    file_name = str(symbol) + str(filename) + ".csv"

    coinDataFrame.to_csv(file_name, index=False, encoding='utf-8')

iterator=0

for tf in timeFrames:

    klinesToCsv(tf, tfIntervals[iterator])
    iterator+=1
