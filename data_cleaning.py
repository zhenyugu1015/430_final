import pandas as pd
import numpy as np

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
    buy_vol, buy_sum, buy_contr = 0, 0, 0
    sell_vol, sell_sum, sell_contr = 0, 0, 0
    
    for i in range(len(buy_input)):

        buy_vol += sum(float(buy_input[i,3+j].split('x')[1].split('(')[0])*
                        float(buy_input[i,3+j].split('(')[1].split(')')[0]) 
                        for j in range(10))
        buy_sum += sum(float(buy_input[i,3+j][:8])*
                        float(buy_input[i,3+j].split('x')[1].split('(')[0])
                        for j in range(10))
        buy_contr += sum(float(buy_input[i,3+j].split('x')[1].split('(')[0])
                        for j in range(10))

        if(float(buy_input[i,0])//1000 > float(buy_input[i-1,0])//1000 or i==0):
            buy_time = float(buy_input[i,0])//1000
            buy_open = buy_input[i,3][:7]
            buy_low = min(float(buy_input[i,3+j][:8]) for j in range(10))
            buy_high = max(float(buy_input[i,3+j][:8]) for j in range(10))

        else:
            row_low = min(float(buy_input[i,3+j][:8]) for j in range(10))
            row_high = max(float(buy_input[i,3+j][:8]) for j in range(10))
            if(row_low < buy_low):
                buy_low = row_low
            if(row_high > buy_high):
                buy_high = row_high

        if(i==len(buy_input)-1):
            buy_close = buy_input[i,12][:7]
            buy_weighted_avg = buy_sum / buy_contr
            temp1.append([buy_time,buy_open,buy_close,buy_low,buy_high,buy_vol,buy_weighted_avg])
            buy_vol, buy_sum, buy_contr = 0, 0, 0
            break

        if(float(buy_input[i,0])//1000 < float(buy_input[i+1,0])//1000):
            buy_close = buy_input[i,12][:7]
            buy_weighted_avg = buy_sum / buy_contr
            temp1.append([buy_time,buy_open,buy_close,buy_low,buy_high,buy_vol,buy_weighted_avg])
            buy_vol, buy_sum, buy_contr = 0, 0, 0

    buy_output = np.array(temp1)
    buy_columns = ['time','buy_open','buy_close','buy_low','buy_high','buy_volume','buy_weighted_avg']
    buy_df = pd.DataFrame(buy_output,columns=buy_columns)
    #df.to_csv(".csv")# change file name if you would like

    for i in range(len(sell_input)):

        sell_vol += sum(float(sell_input[i,3+j].split('x')[1].split('(')[0]) *
                        float(sell_input[i,3+j].split('(')[1].split(')')[0]) 
                        for j in range(10))
        sell_sum += sum(float(sell_input[i,3+j][:8]) *
                        float(sell_input[i,3+j].split('x')[1].split('(')[0])
                        for j in range(10))
        sell_contr += sum(float(sell_input[i,3+j].split('x')[1].split('(')[0])
                        for j in range(10))

        if(float(sell_input[i,0])//1000 > float(sell_input[i-1,0])//1000 or i==0):
            sell_time = float(sell_input[i,0])//1000
            sell_open = sell_input[i,3][:7]
            sell_low = min(float(sell_input[i,3+j][:8]) for j in range(10))
            sell_high = max(float(sell_input[i,3+j][:8]) for j in range(10))

        else:
            row_low = min(float(sell_input[i,3+j][:8]) for j in range(10))
            row_high = max(float(sell_input[i,3+j][:8]) for j in range(10))
            if(row_low < sell_low):
                sell_low = row_low
            if(row_high > sell_high):
                sell_high = row_high

        if(i==len(sell_input)-1):
            sell_close = sell_input[i,12][:7]
            sell_weighted_avg = sell_sum / sell_contr
            temp2.append([sell_time,sell_open,sell_close,sell_low,sell_high,sell_vol,sell_weighted_avg])
            sell_vol, sell_sum, sell_contr = 0, 0, 0
            break

        if(float(sell_input[i,0])//1000 < float(sell_input[i+1,0])//1000):
            sell_close = sell_input[i,12][:7]
            sell_weighted_avg = sell_sum / sell_contr
            temp2.append([sell_time,sell_open,sell_close,sell_low,sell_high,sell_vol,sell_weighted_avg])
            sell_vol, sell_sum, sell_contr = 0, 0, 0

    sell_output = np.array(temp2)
    sell_columns = ['time','sell_open','sell_close','sell_low','sell_high','sell_volume','sell_weighted_avg']
    sell_df = pd.DataFrame(sell_output,columns=sell_columns)

    result = pd.merge(buy_df, sell_df,how='outer',on='time')
    result.sort_values('time')
    result.to_csv("concat.csv",index=False) # change file name if you would like


### Change file path here ###
toSeconds("Workbook1.csv")