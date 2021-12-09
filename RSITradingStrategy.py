#Uses RSI to determine if stock overbought or oversold
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

stock = pd.read_csv('AAPL.csv')
stock.set_index(pd.DatetimeIndex(stock['Date']),inplace=True)



delta = stock['Adj Close'].diff(1)
delta.dropna()

up = delta.copy()
down = delta.copy()

up[up<0] = 0
down[down>0] = 0

period=14
AVG_Gain = up.rolling(window=period).mean()
AVG_Loss = abs(down.rolling(window=period).mean())

RS = AVG_Gain/AVG_Loss
RSI = 100.0 - (100.0/(1.0+RS))


new_df = pd.DataFrame()
new_df['Adj Close'] = stock['Adj Close']
new_df['RSI'] = RSI

#visualizing
plt.figure(figsize=(12.2,5.8))
plt.plot(new_df.index,new_df['Adj Close'],)
plt.title('Adj. Close Price History')
plt.xlabel('Date',fontsize=18)
plt.ylabel('Adj. Close Price USD($)',fontsize=18)
plt.legend(new_df.columns.values,loc='upper left')
plt.show()

plt.figure(figsize=(12.2,5.8))
plt.title('RSI Plot')
plt.plot(new_df.index,new_df['RSI'])
plt.axhline(0,linestyle='--',alpha=0.5,color='gray')
plt.axhline(10,linestyle='--',alpha=0.5,color='orange')
plt.axhline(20,linestyle='--',alpha=0.5,color='green')
plt.axhline(30,linestyle='--',alpha=0.5,color='red')
plt.axhline(70,linestyle='--',alpha=0.5,color='red')
plt.axhline(80,linestyle='--',alpha=0.5,color='green')
plt.axhline(90,linestyle='--',alpha=0.5,color='orange')
plt.axhline(100,linestyle='--',alpha=0.5,color='gray')
plt.show()