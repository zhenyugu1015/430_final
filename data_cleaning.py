import pandas as pd
import numpy as np
from numpy import genfromtxt

def toSeconds(file):
    df = pd.read_csv(file, header=None, sep=',')
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
            buy_vol = sum(float(buy_input[i,3+j][-3:-2]) for j in range(10))

        else:
            row_low = min(float(buy_input[i,3+j][:8]) for j in range(10))
            row_high = max(float(buy_input[i,3+j][:8]) for j in range(10))
            buy_vol += sum(float(buy_input[i,3+j][-3:-2]) for j in range(10))
            if(row_low < buy_low):
                buy_low = row_low
            if(row_high > buy_high):
                buy_high = row_high

        if(i==len(buy_input)-1):
            buy_close = buy_input[i,12][:7]
            temp1.append([buy_time,buy_ticker,buy_open,buy_close,buy_low,buy_high,buy_vol])
            break

        if(float(buy_input[i,0])//1000 < float(buy_input[i+1,0])//1000):
            buy_close = buy_input[i,12][:7]
            temp1.append([buy_time,buy_ticker,buy_open,buy_close,buy_low,buy_high,buy_vol])

    buy_output = np.array(temp1)
    columns = ['time','ticker','open','close','low','high','volume']
    df = pd.DataFrame(buy_output,columns=columns)
    df.to_csv("ticker1_buy.csv")



toSeconds("Workbook1.csv")