import yfinance as yf
from datetime import datetime, timedelta, date

def scrape_data(stock_name,end_date,period=365,download=False):
	start_date = end_date - timedelta(period)
	data = yf.download(stock_name,start_date,end_date)
	if download:
		data.to_csv(f"{stock_name}.csv")
	return data


