#description: program uses dual moving average crossover to determine when to buy and sell stock
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

AAPL = pd.read_csv('StockTickers/SUNW.csv',nrows=200)


SMA30 = pd.DataFrame()
SMA30['Adj Close Price'] = AAPL['Adj Close'].rolling(window=30).mean()

#create a simple moving 100 day average
SMA100 = pd.DataFrame()
SMA100['Adj Close Price'] = AAPL['Adj Close'].rolling(window=100).mean()



data = pd.DataFrame()
data['AAPL'] = AAPL['Adj Close']
data['SMA30'] = SMA30['Adj Close Price']
data['SMA100'] = SMA100['Adj Close Price']

#create function to signal when to buy and sell asset/stock
def buy_sell(data):
	sigPriceBuy = []
	sigPriceSell = []
	flag = -1

	for i in range(len(data)):
		if data['SMA30'][i]>data['SMA100'][i]:
			if flag != 1:
				sigPriceBuy.append(data['AAPL'][i])
				sigPriceSell.append(np.nan)
				flag=1
			else:
				sigPriceBuy.append(np.nan)
				sigPriceSell.append(np.nan)
		elif data['SMA30'][i] < data['SMA100'][i]:
			if flag != 0:
				sigPriceBuy.append(np.nan)
				sigPriceSell.append(data['AAPL'][i])
				flag=0
			else:
				sigPriceBuy.append(np.nan)
				sigPriceSell.append(np.nan)
		else:
			sigPriceBuy.append(np.nan)
			sigPriceSell.append(np.nan)

	return (sigPriceBuy,sigPriceSell)

#store buy and sell data into variable
buy_sell = buy_sell(data)
data['Buy_Signal_Price'] = buy_sell[0]
data['Sell_Signal_Price'] = buy_sell[1]

#vizualizing
plt.figure(figsize=(12.4,6.4))
plt.plot(AAPL['Adj Close'],label = 'AAPL', alpha=0.35)
plt.plot(SMA30['Adj Close Price'],label = 'SMA30', alpha=0.35)
plt.plot(SMA100['Adj Close Price'],label = 'SMA100', alpha=0.35)
plt.scatter(data.index,data['Buy_Signal_Price'],label='Buy',marker="^",color='green')
plt.scatter(data.index,data['Sell_Signal_Price'],label='Sell',marker="v",color='red')
plt.title('Apple Adj. Close Price History Buy & Sell Signals')
plt.xlabel('Oct, 02, 2010 - Dec. 30, 2014')
plt.ylabel('Adj. Close Price USD($)')
plt.legend(loc='upper left')
plt.show()