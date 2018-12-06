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
            buy_open = buy_input[i,3]
        if(i==len(buy_input)-1):
            buy_close = buy_input[i,12]
            temp1.append([buy_time,buy_ticker,buy_open,buy_close])
            break
        if(float(buy_input[i,0])//1000 < float(buy_input[i+1,0])//1000):
            buy_close = buy_input[i,12]
            temp1.append([buy_time,buy_ticker,buy_open,buy_close])

    buy_output = np.array(temp1)

    for i in range(len(sell_input)):
        if(float(sell_input[i,0])//1000 > float(sell_input[i-1,0])//1000 or i==0):
            sell_time = float(sell_input[i,0])//1000
            sell_ticker = sell_input[i,1]
            sell_open = sell_input[i,3]
        if(i==len(sell_input)-1):
            sell_close = sell_input[i,12]
            temp2.append([sell_time,sell_ticker,sell_open,sell_close])
            break
        if(float(sell_input[i,0])//1000 < float(sell_input[i+1,0])//1000):
            sell_close = sell_input[i,12]
            temp2.append([sell_time,sell_ticker,sell_open,sell_close])
    sell_output = np.array(temp2)
    print(buy_output, sell_output)
toSeconds("Workbook1.csv")