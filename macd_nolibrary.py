import pandas as pd
import numpy as np
import yfinance as yf
#import pandas_datareader as pdr
import datetime as dt
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema
from datetime import datetime

ticker = 'EDN.BA'
 
df = yf.download(ticker, period='6mo')


# Calculate the MACD and Signal Line indicators
## Calculate the Short Term Exponential Moving Average
ShortEMA = df.Close.ewm(span=12, adjust=False).mean()

# Calculate the Long Term Exponential Moving Average
LongEMA = df.Close.ewm(span=26, adjust=False).mean()






# Calculate the Moving Average Convergence/Divergence (MACD)
MACD = ShortEMA - LongEMA
print(MACD)



# Calcualte the signal line
signal = MACD.ewm(span=9, adjust=False).mean()

macd_his=MACD-signal
print(macd_his)
x =macd_his.to_numpy()


macd_max = argrelextrema(x, np.greater)
last_max_date = df.index[macd_max][-1]
print(last_max_date)
dif_max =((datetime.now() - last_max_date)).days
print (f' diferencia maximo : {dif_max}')


macd_min = argrelextrema(x, np.less)
last_min_date = df.index[macd_min][-1]
print(last_min_date)
dif_min =((datetime.now() - last_min_date)).days
print (f' diferencia minimo : {dif_min}')








