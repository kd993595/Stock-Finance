#Uses Moving Average Convergence Divergence crossover to buy/sell stock
#used in shorter time frames day or hours or even minutes
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

df = pd.read_csv('AAPL.csv')
df.set_index(pd.DatetimeIndex(df['Date']),inplace=True)

#calculate MACF and signla line indicators
#calculate short term expoenntial moving average(EMA)
ShortEMA = df.Close.ewm(span=12,adjust=False).mean()
#calculate long term exponential moving average
LongEMA = df.Close.ewm(span=26,adjust=False).mean()

MACD = ShortEMA - LongEMA
signal = MACD.ewm(span=9,adjust=False).mean()


df['MACD'] = MACD
df['Signal Line'] = signal


def buy_sell(signal):
	buy_list = list()
	sell_list = list()
	flag = -1

	for i in range(0,len(signal)):
		if signal['MACD'][i] > signal['Signal Line'][i]:
			sell_list.append(np.NaN)
			if flag !=1:
				buy_list.append(signal['Close'][i])
				flag = 1
			else:
				buy_list.append(np.NaN)
		elif signal['MACD'][i] < signal['Signal Line'][i]:
			buy_list.append(np.NaN)
			if flag != 0:
				sell_list.append(signal['Close'][i])
				flag = 0
			else:
				sell_list.append(np.NaN)
		else:
			buy_list.append(np.NaN)
			sell_list.append(np.NaN)
	return (buy_list,sell_list)

a = buy_sell(df)
df['Buy Signal Price'] = a[0]
df['Sell Signal Price'] = a[1]

#visualizing
plt.figure(figsize=(12.2,5.8))
#plt.scatter(df.index,df['Buy Signal Price'],color='green',label='Buy',marker='^',alpha=1)
#plt.scatter(df.index,df['Sell Signal Price'],color='red',label='Sell',marker='v',alpha=1)
#plt.plot(df['Close'],label='Close Price',alpha=0.35)
plt.plot(df['MACD'],label='MACD',alpha=0.35,color='blue')
plt.plot(df['Signal Line'],label='Signal Line',alpha=0.35,color='gold')
plt.axhline(0,linestyle='--',alpha=0.5,color='gray')
plt.legend(loc='upper left',)
plt.title('Close Price Buy and Sell')
plt.xlabel('Date')
plt.ylabel('Close Price USD ($)')
plt.show()
