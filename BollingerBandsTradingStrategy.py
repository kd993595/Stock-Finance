#uses bollinger bands to buy and sell stocks
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

df = pd.read_csv('AAPL.csv')
df.set_index(pd.DatetimeIndex(df['Date'].values),inplace=True)

#calculate moving average, standard deviation, upper band, lower band
period=20
df['SMA'] = df['Close'].rolling(window=period).mean()
df['STD'] = df['Close'].rolling(window=period).std()
df['Upper'] = df['SMA'] + (df['STD'] * 2)
df['Lower'] = df['SMA'] - (df['STD'] * 2)

column_list = ['Close','SMA','Upper','Lower']


new_df = df[period-1:]

def get_signal(data):
	buy_signal=[]
	sell_signal=[]
	flag = -1

	for i in range(len(data['Close'])):
		if data['Close'][i] > data['Upper'][i] and flag != -1:
			buy_signal.append(np.NaN)
			sell_signal.append(data['Close'][i])
			flag = -1
		elif data['Close'][i] < data['Lower'][i] and flag != 1:
			buy_signal.append(data['Close'][i])
			sell_signal.append(np.NaN)
			flag = 1
		else:
			buy_signal.append(np.NaN)
			sell_signal.append(np.NaN)
	return (buy_signal,sell_signal)

new_df['Buy'] = get_signal(new_df)[0]
new_df['Sell'] = get_signal(new_df)[1]


fig = plt.figure(figsize=(12.2,5.8))
ax = fig.add_subplot(1,1,1)
x_axis = new_df.index
ax.fill_between(x_axis, new_df['Upper'],new_df['Lower'],color='grey')
ax.plot(x_axis, new_df['Close'],color='blue',lw=3,label='Close Price',alpha=0.5)
ax.plot(x_axis, new_df['SMA'],color='purple',lw=2,label='Simple Moving Average',alpha=0.5)
ax.scatter(x_axis,new_df['Buy'],color='green',label='Buy',marker='^',alpha=1)
ax.scatter(x_axis,new_df['Sell'],color='red',label='Sell',marker='v',alpha=1)
ax.set_title('Bollinger Band for Apple')
ax.set_xlabel('Date')
ax.set_ylabel('USD Price($)')
ax.legend(loc='upper left')
plt.show()