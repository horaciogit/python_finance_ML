#commit

import yfinance as yf
import pandas as pd
import numpy as np
import talib as ta
from scipy.signal import argrelextrema
from datetime import datetime

BA_GRAL= ['MOLI.BA','LONG.BA', 'AGRO.BA', 'METR.BA', 'BOLT.BA', 'AUSO.BA', 'DGCU2.BA',
             'FERR.BA', 'GCLA.BA']


BA = ['ALUA.BA', 'BMA.BA', 'BYMA.BA','CEPU.BA', 'COME.BA', 'CRES.BA', 'CVH.BA',
      'EDN.BA', 'GGAL.BA', 'LOMA.BA', 'MIRG.BA', 'PAMP.BA', 'SUPV.BA','TGNO4.BA',
      'TGSU2.BA', 'TRAN.BA', 'VALO.BA', 'YPFD.BA' ]



tabla= pd.DataFrame()
tabla_gral= pd.DataFrame()



def macd_calc(mk):
#    mk['macd'], mk['macd_signal'],mk['macd_hist'] = ta.MACD(mk['Close'], fastperiod=12, slowperiod=26, signalperiod=9)

    ## Calculate the Short Term Exponential Moving Average
    ShortEMA = mk.Close.ewm(span=12, adjust=False).mean()
    # Calculate the Long Term Exponential Moving Average
    LongEMA = mk.Close.ewm(span=26, adjust=False).mean()
    # Calculate the Moving Average Convergence/Divergence (MACD)
    MACD = ShortEMA - LongEMA
   #Calcualte the signal line
    signal = MACD.ewm(span=9, adjust=False).mean()
    macd_his = MACD - signal
    
#----obtener lista de maximos macd---------------
    x = macd_his.to_numpy()   
    macd_max = []
    for e in range(1, x.size - 1):
       if x[e] > x[e-1] and x[e] > x[e+1]:
         macd_max.append(e)
#-------------------------------------------------    
    
    
    last_max_date = mk.index[macd_max][-1]
    print(last_max_date)
    dif_max =((datetime.now() - last_max_date)).days
    print (f' diferencia maximo : {dif_max}')
      
#----obtener lista de minimos macd---------------    
    macd_min = [] 
    for e in range(1, x.size - 1):
       if x[e] < x[e-1] and x[e] < x[e+1]:
         macd_min.append(e)
#-------------------------------------------------    
    
    
    
    
    
    
    
    last_min_date = mk.index[macd_min][-1]
    print(last_min_date)
    dif_min =((datetime.now() - last_min_date)).days
    print (f' diferencia minimo : {dif_min}')
    
    orden = ""
    if dif_max <= 4 and  dif_max < dif_min:
        orden = 'venda'
        
    if dif_min <= 4 and dif_min < dif_max:
        orden =  'compre'   
    print(orden)
    
    return last_max_date, dif_max, last_min_date, dif_min, orden
    
    


for i in BA:
    mk = yf.download(i, period='6mo')
    resultado = macd_calc(mk)
    tabla = tabla.append({'stock':i, 'ultimo max':resultado[0], 'max pasados': resultado[1],
                          'ultimo min':resultado[2], 'min pasados':resultado[3], 'orden': resultado[4] },  ignore_index=True)

tabla.to_csv('tabla.csv')


for i in BA_GRAL:
    mk = yf.download(i, period='6mo')
    resultado = macd_calc(mk)
    tabla_gral = tabla_gral.append({'stock':i, 'ultimo max':resultado[0], 'max pasados': resultado[1],
                          'ultimo min':resultado[2], 'min pasados':resultado[3], 'orden': resultado[4] },  ignore_index=True)

tabla_gral.to_csv('tabla_gral.csv')


