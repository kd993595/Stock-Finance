#Uses Money Flow Index to determine when to buy and sell stock
import numpy as np
import pandas as pd
#import warnings
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
#warnings.filterwarnings('ignore')

df = pd.read_csv('StockTickers/JPM.csv',nrows=200)
df.set_index(pd.DatetimeIndex(df['Date'].values),inplace=True)



typical_price = (df['Close'] + df['High'] + df['Low'])/3
period = 14
money_flow = typical_price * df['Volume']

positive_flow = list()
negative_flow = list()


for i in range(1,len(typical_price)):
	if(typical_price)[i] > typical_price[i-1]:
		positive_flow.append(money_flow[i-1])
		negative_flow.append(0)
	elif typical_price[i] < typical_price[i-1]:
		positive_flow.append(0)
		negative_flow.append(money_flow[i-1])
	else:
		positive_flow.append(0)
		negative_flow.append(0)

positive_mf = list()
negative_mf = list()

for i in range(period-1,len(positive_flow)):
	positive_mf.append(sum(positive_flow[i+1-period:i+1]))

for i in range(period-1,len(negative_flow)):
	negative_mf.append(sum(negative_flow[i+1-period:i+1]))

mfi = 100*(np.array(positive_mf)/(np.array(positive_mf)+np.array(negative_mf)))


new_df = pd.DataFrame()
new_df = df[period:]
new_df['MFI'] = mfi

def get_signal(data,high,low):
	buy_signal = list()
	sell_signal = list()
	flag = -1

	for i in range(len(data['MFI'])):
		if data['MFI'][i] > high:
			buy_signal.append(np.NaN)
			if flag!=-1:
				sell_signal.append(data['Close'][i])
				flag = -1
			else:
				sell_signal.append(np.NaN)
		elif data['MFI'][i] < low:
			if flag!=1:
				buy_signal.append(data['Close'][i])
				flag = 1
			else:
				buy_signal.append(np.NaN)
			sell_signal.append(np.NaN)
		else:
			buy_signal.append(np.NaN)
			sell_signal.append(np.NaN)
	return (buy_signal,sell_signal)

new_df['Buy'] = get_signal(new_df,80,20)[0]
new_df['Sell'] = get_signal(new_df,80,20)[1]

#plotting
plt.figure(figsize=(12.2,6.4))
plt.plot(df['Close'],label="Close Price",alpha=0.5)
plt.scatter(new_df.index,new_df['Buy'],color='green',marker='^',label='Buy Signal',alpha=1)
plt.scatter(new_df.index,new_df['Sell'],color='red',marker='v',label='Sell Signal',alpha=1)
plt.title('Apple Close Price')
plt.xlabel('Date')
plt.ylabel('Close Price USD($)')
plt.legend(loc='upper left')
plt.show()

#shows MFI value plot
plt.figure(figsize=(12.2,6.4))
plt.plot(new_df['MFI'],label="MFI")
plt.axhline(10,linestyle='--',color = 'orange')
plt.axhline(20,linestyle='--',color = 'blue')
plt.axhline(80,linestyle='--',color = 'blue')
plt.axhline(90,linestyle='--',color = 'orange')
plt.title('MFI')
plt.ylabel('MFI Values')
plt.show()