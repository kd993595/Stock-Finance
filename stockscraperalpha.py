import requests
import os
import json
import pandas as pd

API_KEY = "H3O80WUBMLPNMF0S"
symbol = "MARA"
#change to compact for previos 100
size_ouput = "full"
source_link = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}&datatype=csv"
source_adjusted_info = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={API_KEY}&datatype=csv"

time_interval = "60min"
source_intraday = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={time_interval}&apikey={API_KEY}&datatype=csv"

def download_file(url, filename):
    ''' Downloads file from the url and save it as filename '''
    response = requests.get(url)
    # Check if the response is ok (200)
    if response.status_code == 200:
        # Open file and write the content
        with open(filename, 'wb') as file:
            # A chunk of 128 bytes
            for chunk in response:
                file.write(chunk)

#download_file(source_json,f'{symbol}.json')

def convertJsonToCSV(filename,download=True):
    new_filename = filename.split(".")[0] + ".csv"
    with open(filename,'r') as f:
        data = json.load(f)
    meta_data = data['Meta Data']
    daily_data = data['Time Series (Daily)']
    df = []
    columns = ['Date','Open','High','Low','Close','Adj Close','Volume']
    for key in daily_data.keys():
        df.append([key,daily_data[key]['1. open'],daily_data[key]['2. high'],daily_data[key]['3. low'],daily_data[key]['4. close'],
                        daily_data[key]['5. adjusted close'],daily_data[key]['6. volume']])
    df = pd.DataFrame(df,columns = columns)
    df.set_index(pd.DatetimeIndex(df['Date'].values),inplace=True)
    if download==True:
        df.to_csv(new_filename,index=False)
    return df

#convertJsonToCSV("BB.json")

def getStockInfo(stockname,download=True):
    source_json = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={stockname}&outputsize=full&apikey={API_KEY}"
    download_file(source_json,f"StockTickers/{stockname}.json")
    return convertJsonToCSV(f"StockTickers/{stockname}.json",download)