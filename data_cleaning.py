import pandas as pd
import numpy as np
from numpy import genfromtxt

def toSeconds(file):
    df = pd.read_csv(file, header=None, sep=',', low_memory=False)
    readin = df.values
    temp1, temp2 = [], []
    for i in range(1,len(readin)):
        if readin[i,2]=="BUY":
            temp1.append(readin[i])
        else:
            temp2.append(readin[i])
    buy_input = np.array(temp1)
    sell_input = np.array(temp2)

    temp1, temp2 = [], []

    for i in range(len(buy_input)):

        if(float(buy_input[i,0])//1000 > float(buy_input[i-1,0])//1000 or i==0):
            buy_time = float(buy_input[i,0])//1000
            buy_ticker = buy_input[i,1]
            buy_open = buy_input[i,3][:7]
            buy_low = min(float(buy_input[i,3+j][:8]) for j in range(10))
            buy_high = max(float(buy_input[i,3+j][:8]) for j in range(10))
            buy_vol = sum(float(buy_input[i,3+j].split('x')[1].split('(')[0])*
                        float(buy_input[i,3+j].split('(')[1].split(')')[0]) 
                        for j in range(10))
            buy_sum = sum(float(buy_input[i,3+j][:8])*
                        float(buy_input[i,3+j].split('x')[1].split('(')[0])*
                        float(buy_input[i,3+j].split('(')[1].split(')')[0]) 
                        for j in range(10))

        else:
            row_low = min(float(buy_input[i,3+j][:8]) for j in range(10))
            row_high = max(float(buy_input[i,3+j][:8]) for j in range(10))
            buy_vol += sum(float(buy_input[i,3+j].split('x')[1].split('(')[0])*
                        float(buy_input[i,3+j].split('(')[1].split(')')[0]) 
                        for j in range(10))
            buy_sum += sum(float(buy_input[i,3+j][:8])*
                        float(buy_input[i,3+j].split('x')[1].split('(')[0])*
                        float(buy_input[i,3+j].split('(')[1].split(')')[0]) 
                        for j in range(10))
            if(row_low < buy_low):
                buy_low = row_low
            if(row_high > buy_high):
                buy_high = row_high

        if(i==len(buy_input)-1):
            buy_close = buy_input[i,12][:7]
            buy_weighted_avg = buy_sum / buy_vol
            temp1.append([buy_time,buy_ticker,buy_open,buy_close,buy_low,buy_high,buy_vol,buy_weighted_avg])
            break

        if(float(buy_input[i,0])//1000 < float(buy_input[i+1,0])//1000):
            buy_close = buy_input[i,12][:7]
            buy_weighted_avg = buy_sum / buy_vol
            temp1.append([buy_time,buy_ticker,buy_open,buy_close,buy_low,buy_high,buy_vol,buy_weighted_avg])

    buy_output = np.array(temp1)
    columns = ['time','ticker','open','close','low','high','volume','weighted_avg']
    df = pd.DataFrame(buy_output,columns=columns)
    df.to_csv("ticker1_buy.csv")# change file name if you would like

    for i in range(len(sell_input)):

        if(float(sell_input[i,0])//1000 > float(sell_input[i-1,0])//1000 or i==0):
            sell_time = float(sell_input[i,0])//1000
            sell_ticker = sell_input[i,1]
            sell_open = sell_input[i,3][:7]
            sell_low = min(float(sell_input[i,3+j][:8]) for j in range(10))
            sell_high = max(float(sell_input[i,3+j][:8]) for j in range(10))
            sell_vol = sum(float(sell_input[i,3+j].split('x')[1].split('(')[0])*
                        float(sell_input[i,3+j].split('(')[1].split(')')[0]) 
                        for j in range(10))
            sell_sum = sum(float(sell_input[i,3+j][:8])*
                        float(sell_input[i,3+j].split('x')[1].split('(')[0])*
                        float(sell_input[i,3+j].split('(')[1].split(')')[0]) 
                        for j in range(10))

        else:
            row_low = min(float(sell_input[i,3+j][:8]) for j in range(10))
            row_high = max(float(sell_input[i,3+j][:8]) for j in range(10))
            sell_vol += sum(float(sell_input[i,3+j].split('x')[1].split('(')[0])*
                        float(sell_input[i,3+j].split('(')[1].split(')')[0]) 
                        for j in range(10))
            sell_sum += sum(float(sell_input[i,3+j][:8])*
                        float(sell_input[i,3+j].split('x')[1].split('(')[0])*
                        float(sell_input[i,3+j].split('(')[1].split(')')[0]) 
                        for j in range(10))
            if(row_low < sell_low):
                sell_low = row_low
            if(row_high > sell_high):
                sell_high = row_high

        if(i==len(sell_input)-1):
            sell_close = sell_input[i,12][:7]
            sell_weighted_avg = sell_sum / sell_vol
            temp2.append([sell_time,sell_ticker,sell_open,sell_close,sell_low,sell_high,sell_vol,sell_weighted_avg])
            break

        if(float(sell_input[i,0])//1000 < float(sell_input[i+1,0])//1000):
            sell_close = sell_input[i,12][:7]
            sell_weighted_avg = sell_sum / sell_vol
            temp2.append([sell_time,sell_ticker,sell_open,sell_close,sell_low,sell_high,sell_vol,sell_weighted_avg])

    sell_output = np.array(temp2)
    columns = ['time','ticker','open','close','low','high','volume','weighted_avg']
    df = pd.DataFrame(sell_output,columns=columns)
    df.to_csv("ticker1_sell.csv") # change file name if you would like


### Change file path here ###
toSeconds("Ticker1.csv")

