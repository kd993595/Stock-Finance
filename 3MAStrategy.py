import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

df = pd.read_csv('StockTickers/CRSR.csv',nrows=365)
df = df.set_index(pd.DatetimeIndex(df['Date'].values))

#calculating moving averages
short_ema = df.Close.ewm(span=5,adjust=False).mean()
middle_ema = df.Close.ewm(span=21,adjust=False).mean()
long_ema = df.Close.ewm(span=63,adjust = False).mean()



#add exponential moving averaes to dataset
df['Short'] = short_ema
df['Middle'] = middle_ema
df['Long'] = long_ema

def buy_sell_function(data):
	buy_list=[]
	sell_list=[]
	flag_long=False
	flag_short=False

	for i in range(0,len(data)):
		
		if data['Middle'][i] < data['Long'][i] and data['Short'][i]<data['Middle'][i] and flag_long ==False and flag_short==False:
			buy_list.append(data['Close'][i])
			sell_list.append(np.NaN)
			flag_short=True
		elif flag_short and data['Short'][i] > data['Middle'][i]:
			sell_list.append(data['Close'][i])
			buy_list.append(np.NaN)
			flag_short=False
		
		elif data['Middle'][i] > data['Long'][i] and data['Short'][i]>data['Middle'][i] and flag_long ==False and flag_short==False:
			buy_list.append(data['Close'][i])
			sell_list.append(np.NaN)
			flag_long=True
		elif flag_long and data['Short'][i] < data['Middle'][i]:
			sell_list.append(data['Close'][i])
			buy_list.append(np.NaN)
			flag_long=False
		else:
			buy_list.append(np.NaN)
			sell_list.append(np.NaN)
	return (buy_list,sell_list)



#add buy and sell signals to data set
df['Buy'] = buy_sell_function(df)[0]
df['Sell'] = buy_sell_function(df)[1]

plt.figure(figsize=(12.2,6.4))
plt.title('Buy and Sell Plot',fontsize=18)
plt.plot(df['Close'],label='Close Price',color='blue',alpha=.35)
plt.plot(short_ema,label='Short/Fast EMA',color='red',alpha=.35)
plt.plot(middle_ema,label='Middle/Medium EMA',color='orange',alpha=.35)
plt.plot(long_ema,label='Long/Slow EMA',color='green',alpha=.35)
plt.scatter(df.index, df['Buy'],color='green',marker='^',alpha=1)
plt.scatter(df.index, df['Sell'],color='red',marker='v',alpha=1)
plt.xlabel('Date',fontsize=18)
plt.ylabel('Close Price',fontsize=18)
plt.legend(loc='upper left')
plt.show()