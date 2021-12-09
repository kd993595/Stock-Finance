#use Double Exponential Moving Average to determine when to buy and sell stocks
#reduced lag but subjective to market fluctuations
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

df = pd.read_csv("StockTickers/CRSR.csv",nrows=365)
df.set_index(pd.DatetimeIndex(df['Date'].values),inplace=True)


def DEMA(data,time_period,column):
	#calculate exponential moving average for some time period
	EMA = data[column].ewm(span=time_period,adjust=False).mean()
	DEMA = 2*EMA - EMA.ewm(span=time_period,adjust=False).mean()
	return DEMA

#storing short(20day) terrm and long(50day) term DEMA into data set
df['DEMA_short'] = DEMA(df,20,'Close')
df['DEMA_long'] = DEMA(df,50,'Close')



def DEMA_strategy(data):
	buy_list=[]
	sell_list=[]
	flag = 1

	for i in range(0,len(data)):
		if data['DEMA_short'][i] > data['DEMA_long'][i] and flag != -1:
			buy_list.append(data['Close'][i])
			flag = -1
			sell_list.append(np.NaN)
			
		elif data['DEMA_short'][i] < data['DEMA_long'][i] and flag != 1:
			sell_list.append(data['Close'][i])
			buy_list.append(np.NaN)
			flag = 1
		else:
			buy_list.append(np.NaN)
			sell_list.append(np.NaN)
	return (buy_list,sell_list)

df['Buy'] = DEMA_strategy(df)[0]
df['Sell'] = DEMA_strategy(df)[1]

#show data on plot
plt.figure(figsize=(12.2,6.4))
plt.scatter(df.index, df['Buy'],color='green',label='Buy Signal',marker='^',alpha=1)
plt.scatter(df.index, df['Sell'],color='red',label='Sell Signal',marker='v',alpha=1)
plt.plot(df['Close'],label='Close Price',alpha=0.35)
plt.plot(df['DEMA_short'],label='DEMA_short',alpha=0.35)
plt.plot(df['DEMA_long'],label='DEMA_long',alpha=0.35)
plt.title('Close Price Buy and Sell Signals using DEMA')
plt.ylabel('USD Price ($)',fontsize=18)
plt.xlabel('Date',fontsize=18)
plt.legend(loc='upper left')
plt.show()