import numpy as np
import pandas as pd
from pandas.api.types import is_numeric_dtype
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

'''df = pd.read_csv('StockTickers/CRSR.csv', index_col = 'Date',nrows=130)
#data = data.drop(columns='Unnamed: 0') In case need to drop empty column
df = df.iloc[::-1]'''


def SMA(data,period=15,column='Close'):
	return data[column].rolling(window=period).mean()

def EMA(data,period=20,column='Close'):
	return data[column].ewm(span=period,adjust=False).mean()

def DEMA(data,period=20,column='Close'):
	temp_ema = EMA(data,period,column)
	temp_dema = 2*temp_ema - temp_ema.ewm(span=period,adjust=False).mean()
	return temp_dema

def MACD(data,period_long=26,period_short=12,period_signal=9,column='Close'):
	ShortEMA = EMA(data,period_short,column=column)
	LongEMA = EMA(data,period_long,column=column)
	MACD = ShortEMA - LongEMA
	temp_df = pd.DataFrame(MACD.values,columns=['MACD'])
	SignalLine = EMA(temp_df,period_signal,column='MACD')
	temp_df['Signal'] = SignalLine.values
	return temp_df

def RSI(data,period=14,column='Close'):
	if not is_numeric_dtype(data[column]):
		data[column] = pd.to_numeric(data[column], downcast="float")
	delta = data[column].diff(1)
	delta = delta[1:]
	up = delta.copy()
	down = delta.copy()
	up[up<0] = 0
	down[down>0] = 0
	temp_df = data.copy()
	temp_df.drop(['Open','High','Low','Adj Close','Volume'],axis=1,inplace=True)
	temp_df['up'] = up
	temp_df['down'] = down
	AVG_Gain = SMA(temp_df,period,column='up')
	AVG_Loss = abs(SMA(temp_df,period,column='down'))
	RS = AVG_Gain/AVG_Loss
	RSI = 100.0 - (100.0/(1.0+RS))
	temp_df['RSI'] = RSI
	
	return temp_df


'''df['SMA-15'] = SMA(df)
df['EMA-20'] = EMA(df)
temp = MACD(df)
df['MACD'] = temp['MACD'].values
df['Signal'] = temp['Signal'].values
df['RSI'] = RSI(df)['RSI']
df['DEMA'] = DEMA(df)


indexes_to_drop = [i for i in range(15)]
indexes_to_keep = set(range(df.shape[0])) - set(indexes_to_drop)
df = df.take(list(indexes_to_keep))

column_list = ['RSI']
df[column_list].plot(figsize=(12.2,6.4))
plt.title('RSI')
plt.ylabel('USD Price')
plt.xlabel('Date')
plt.show()'''