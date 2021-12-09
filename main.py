import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
plt.style.use('fivethirtyeight')
import warnings
warnings.filterwarnings("ignore")
import os
from stockscraperalpha import getStockInfo
from functions import SMA, EMA,DEMA,MACD,RSI

def show_menu():
	return """[1]change stock
[2]plot
"""

def getInitialInfo(stockname):
	if os.path.isfile(f"StockTickers/{stockname}"):
		return pd.read_csv(f"StockTickers/{stockname}",index_col='Date')
	else:
		return getStockInfo(stockname)

def addDataFrameTI(data_frame):
	data_frame['SMA-13'] = SMA(data_frame,period=13)
	data_frame['SMA-50'] = SMA(data_frame,period=50)
	data_frame['SMA-120'] = SMA(data_frame,period=120)
	data_frame['EMA-12'] = EMA(data_frame,period=12)
	data_frame['EMA-26'] = EMA(data_frame,period=26)
	data_frame['EMA-120'] = EMA(data_frame,period=120)
	temp = MACD(data_frame)
	data_frame['MACD'] = temp['MACD'].values
	data_frame['Signal'] = temp['Signal'].values
	data_frame['RSI'] = RSI(data_frame)['RSI'].values
	data_frame['DEMA-50'] = DEMA(data_frame,period=50)

	data_frame['DEMA-180'] = DEMA(data_frame,period=180)

def cleanDataFrame(data_frame,period=20):
	indexes_to_keep = [i for i in range(period+180)]
	temp_data = data_frame.take(list(indexes_to_keep))
	temp_data = temp_data.iloc[::-1]
	addDataFrameTI(temp_data)
	indexes_to_drop = [i for i in range(180)]
	indexes_to_keep = set(range(temp_data.shape[0])) - set(indexes_to_drop)
	temp_data = temp_data.take(list(indexes_to_keep))
	return temp_data
	

def plotInfo(data):
	plt.figure(figsize=(12.2,6.4))

	if data['Buy'].notnull().values.any():
		plt.scatter(data.index, data['Buy'],color='green',label='Buy Signal',marker='^',alpha=1)
	if data['Sell'].notnull().values.any():
		plt.scatter(data.index, data['Sell'],color='red',label='Sell Signal',marker='v',alpha=1)
	plt.plot(data['SMA-120'],label='SMA_long',alpha=0.35)
	plt.plot(data['EMA-120'],label='EMA_long',alpha=0.35)
	plt.plot(data['Close'],label='Close Price',alpha=0.35)
	plt.title('Close Price Buy and Sell Signals')
	plt.ylabel('USD Price ($)',fontsize=18)
	plt.xlabel('Date',fontsize=18)
	plt.legend(loc='upper left')
	plt.show()



def buy_sell(data):
	buy_list = []
	sell_list = []
	flag = 1
	signal = 0


	for i in range(len(data)):
		if signal == 1:
			buy_list.append(data['Close'][i])
			sell_list.append(None)
			signal = 0
		elif signal == -1:
			sell_list.append(data['Close'][i])
			buy_list.append(None)
			signal = 0
		else:
			buy_list.append(None)
			sell_list.append(None)

		if flag == 1 and data['EMA-12'][i]>data['EMA-26'][i] and data['EMA-120'][i]>data['SMA-120'][i]:
			#buy
			signal = 1
			flag = -1
		elif flag == -1 and data['EMA-12'][i]<data['EMA-26'][i]:
			#sell
			signal = -1
			flag = 1
		else:
			signal = 0
	return buy_list,sell_list


def main():
	stockname = input("Enter stockname: ")
	df = pd.DataFrame()
	df = getInitialInfo(stockname)
	time_period = int(input("How many Days: "))
	df = cleanDataFrame(df,time_period)
	temp_data = buy_sell(df)
	df['Buy'] = temp_data[0]
	df['Sell'] = temp_data[1]	
	while True:
		print(show_menu())
		keyword = input(":")
		if keyword == "quit":
			break
		elif keyword == '1':
			stockname = input("Enter stockname: ")
			df = getInitialInfo(stockname)
			time_period = int(input("How many Days: "))
			df = cleanDataFrame(df,time_period)
			temp_data = buy_sell(df)
			df['Buy'] = temp_data[0]
			df['Sell'] = temp_data[1]
		elif keyword == '2':
			plotInfo(df)
		elif keyword == '3':
			print(df)
		else:
			print('input not recognized')


if __name__ == '__main__':
	main()