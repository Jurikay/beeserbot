import stockstats
import pandas as pd


pd.options.mode.chained_assignment = None  # default='warn'


stock = stockstats.StockDataFrame.retype(pd.read_csv('coins.csv'))
# volume delta against previous day
stock['volume_delta']
# open delta against next 2 day
stock['open_2_d']

# open price change (in percent) between today and the day before yesterday
# 'r' stands for rate.
stock['open_-2_r']

# CR indicator, including 5, 10, 20 days moving average
stock['cr']
stock['cr-ma1']
stock['cr-ma2']
stock['cr-ma3']

# volume max of three days ago, yesterday and two days later
stock['volume_-3,2,-1_max']

# volume min between 3 days ago and tomorrow
stock['volume_-3~1_min']

# # KDJ, default to 9 days
# stock['kdjk']
# stock['kdjd']
# stock['kdjj']
#
# # three days KDJK cross up 3 days KDJD
# stock['kdj_3_xu_kdjd_3']

# 2 days simple moving average on open price
stock['open_2_sma']

# MACD
mymacd = stock['macd']
# MACD signal line
stock['macds']
# MACD histogram
stock['macdh']

# bolling, including upper band and lower band
myboll = stock['boll']
myuboll = stock['boll_ub']
mylboll = stock['boll_lb']

# close price less than 10.0 in 5 days count
stock['close_10.0_le_5_c']

# CR MA2 cross up CR MA1 in 20 days count
stock['cr-ma2_xu_cr-ma1_20_c']

# 6 days RSI
myrsi = stock['rsi_6']
# 12 days RSI
myrsi12 = stock['rsi_12']

# 10 days WR
stock['wr_10']
# 6 days WR
stock['wr_6']

# CCI, default to 14 days
stock['cci']
# 20 days CCI
stock['cci_20']

# TR (true range)
stock['tr']
# ATR (Average True Range)
stock['atr']

# DMA, difference of 10 and 50 moving average
stock['dma']

# DMI
# +DI, default to 14 days
stock['pdi']

# DX, default to 14 days of +DI and -DI
stock['dx']

# ADXR, 6 days SMA of ADX, same as stock['adx_6_ema']
stock['adxr']

# TRIX, default to 12 days
stock['trix']
# MATRIX is the simple moving average of TRIX
stock['trix_9_sma']

# VR, default to 26 days
stock['vr']
# MAVR is the simple moving average of VR
stock['vr_6_sma']

print("%.8f" % mymacd.iloc[-1])
print(myrsi.iloc[-1])
print(myboll.iloc[-1])
print("")
print("#####################")
print("")
print("Coin: " + str("BNB"))
print("Bollinger Bands: (upper, middle, lower)")
print(round(float(myuboll.iloc[-1]),8))
print(round(myboll.iloc[-1],8))
print(round(mylboll.iloc[-1],8))
print("")
print("RSI: 6, 12")
print(round(myrsi.iloc[-1],1))
print(round(myrsi12.iloc[-1],1))

tfIntervals = ["1m", "5m", "15m", "30m", "1h", "2h", "1d"]

print("##################   ")

for tf in tfIntervals:
    stock = stockstats.StockDataFrame.retype(pd.read_csv('BNBBTC' + tf + '.csv'))

    myrsi = stock['rsi_6']
    myrsi12 = stock['rsi_12']

    myboll = stock['boll']
    myuboll = stock['boll_ub']
    mylboll = stock['boll_lb']

    print("Interval: " + tf + ":")
    print("RSI: " + "6d: " + str(round(myrsi.iloc[-1],1)) + " 12d: " + str(round(myrsi12.iloc[-1],1)))
    print("BOLL: " + "low: " + str(round(mylboll.iloc[-1],8)) + " med: " + str(round(myboll.iloc[-1],8)) + " high: " + str(round(myuboll.iloc[-1],8)))
