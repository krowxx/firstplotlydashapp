import datetime
import requests
import pandas as pd
import schedule
import time

def time_2_hours_ago():
    time_ago = datetime.datetime.now() - datetime.timedelta(hours=2)
    time_ago = str(int(time_ago.timestamp()))
    return time_ago

print(time_2_hours_ago())

def download_bybit_data(symbol, interval, start_time):
    #define the url
    url = 'https://api.bybit.com/v2/public/kline/list'
    #define the parameters
    params = {'symbol': symbol, 'interval': interval, 'from': start_time}
    #get the response
    response = requests.get(url, params=params)
    #convert the response to json
    data = response.json()
    print(data['result'])
    #convert the json to dataframe
    df = pd.DataFrame(data['result'])
    #rename the columns
    df.columns = ['symbol','interval','open_time', 'open', 'high', 'low', 'close', 'volume', 'turnover']
    #convert the open_time and close_time to datetime
    df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
    #set the index to open_time
    df.set_index('open_time', inplace=True)
    #return the dataframe
    return df


def download_bybit_data_to_csv(symbol, interval, start_time, filename):
    #download the data
    df = download_bybit_data(symbol, interval, start_time)
    #write the data to csv
    df.to_csv(filename)

download_bybit_data_to_csv('BTCUSD','1',time_2_hours_ago(),'bitcoin1minute.csv')

#schedule the function to run every 15 minutes

schedule.every(1).second.do(download_bybit_data_to_csv,'BTCUSD','1',time_2_hours_ago(),'bitcoin1minute.csv')

while True:
    schedule.run_pending()
    time.sleep(1)
    print('1second passed')
