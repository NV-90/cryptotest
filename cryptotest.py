import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import datetime

#Strategy will look to buy when exp weighted moving average in short term goes above long term
# strategy gets out of the trade when short term EWM moves below long term

from datetime import datetime
crypto_data = pd.read_csv("C:/Users/***/Downloads/BITBAY_BTCUSD, 1D (1).csv") #open high low close MA Volume Voluma MA RSI Histogram MACD Signal
crypto_data["time"] = [datetime.fromtimestamp(x).strftime("%d-%m-%Y") for x in crypto_data["time"]]
crypto_data.set_index('time')


crypto = crypto_data[["close"]]
#print(crypto)
# exponentially weighted moving averages to use in strategy
EMA=[3, 5, 10, 12, 15, 30, 40, 45, 50, 60]
pos = 0
num=0
percentchange=[]

for x in EMA:
    crypto["ema_"+str(x)] = round(crypto["close"].ewm(span=x, adjust = False).mean(),2)

for y in range(0,len(crypto.index)):
    cmin1=min(crypto.iloc[y,[1,2,3,4,5]])
    cmax1= max(crypto.iloc[y, [6, 7, 8, 9, 10]])
    close=crypto["close"][y]

#if the minimum out of the shorter EMAs used is greater than the maximum of the longer EMAs used then enter into a buy position (bp)
    if (cmin1>cmax1):
        if(pos==0):
            bp=close
            pos=1
            #print("Buying now at "+str(bp))

    elif(cmin1<cmax1):
        if(pos==1):
            sp=close
            pos=0
            #print("Selling now at "+str(sp))
            pc=(sp/bp-1)*100
            percentchange.append(pc)
#if we have an open position at the end of the dataset, then close the position out.
    if (y==len(crypto.index)-1 and pos==1):
        sp = close
        pos = 0
        #print("Selling now at " + str(sp))
        pc = (sp / bp - 1) * 100
        percentchange.append(pc)

#print(percentchange)


gains=0
netgains=0
losses=0
netlosses=0
Return=1

#calculating summary of strategy.
for i in percentchange:
    if(i>0):
        gains+=i
        netgains+=1
    else:
        losses+=i
        netlosses+=1
    Return = Return *((i/100)+1)
Return=round((Return-1)*100,2)



print("EMAs used: "+str(EMA))
print("Total return over "+str(netgains+netlosses)+ " trades: "+ str(Return)+"%" )

print()

