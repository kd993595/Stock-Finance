#buys when close price below previous 7day low and market above 200MA and sell when above previous 7day High
#it's an unadjusted cost
#very effective
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

stock = pd.read_csv('AAPl.csv')
stock.set_index(pd.DatetimeIndex(stock['Date'].values),inplace=True)

long_ema = stock['Close'].rolling(window=200).mean()
stock['Long'] = long_ema

lows = stock['Low'].rolling(window=7).min()
highs = stock['High'].rolling(window=7).max()

def buy_sell(data):
	buy_list=[]
	sell_list=[]
	flag = 25

	for i in range(len(data)):
		if data['Close'][i] > data['Long'][i] and data['Close'][i] <= lows[i]:
			if flag != 1:				
				buy_list.append(data['Close'][i])
				sell_list.append(np.NaN)
				flag = 1
			else:
				buy_list.append(np.NaN)
				sell_list.append(np.NaN)
		elif data['Close'][i] >= highs[i]:
			if flag != -1:
				buy_list.append(np.NaN)
				sell_list.append(data['Close'][i])
				flag = -1
			else:
				buy_list.append(np.NaN)
				sell_list.append(np.NaN)
		else:
			buy_list.append(np.NaN)
			sell_list.append(np.NaN)
	return (buy_list,sell_list)

a=buy_sell(stock)
stock['Buy Signal'] = a[0]
stock['Sell Signal'] = a[1]


plt.figure(figsize=(12.2,6.4))
plt.title('200 Moving AVerage With Price',fontsize=18)
plt.plot(stock['Close'],label='Close Price',color='blue',alpha=.5)
plt.plot(stock['Long'],label='Long/Slow EMA',color='green',alpha=0.5)
plt.scatter(stock.index,stock['Buy Signal'],label='Buy',marker="^",color='green')
plt.scatter(stock.index,stock['Sell Signal'],label='Sell',marker="v",color='red')
plt.plot(lows,label='Lowest Price Window',color='brown',alpha=0.5)
plt.plot(highs,label="Highest Price Window",color='gold',alpha=0.5)
plt.xlabel('Date',fontsize=18)
plt.ylabel('Close Price',fontsize=18)
plt.legend(loc='upper left')
plt.show()