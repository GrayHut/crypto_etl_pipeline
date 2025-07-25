#function to get realtime crypto prices
#identify top 10 crypto and send mails and save data as csv

import requests
from datetime import datetime
import pandas as pd

url='https://api.coingecko.com/api/v3/coins/markets'

parameters={
    'vs_currency':'usd',
    'order':'market_cap_desc',
    'per_page':250,
    'page':1
}
response=requests.get(url, params=parameters)

if response.status_code==200:
    print("SUCCESSFULL CONNECTION!!!.... Fetching data....")

    data=response.json()
    df=pd.DataFrame(data)
    
    #selecting specific columns
    df=df[[
        'id','symbol','name','current_price','market_cap','high_24h','low_24h'
    ]]

    #adding columns
    date_today=datetime.now().strftime('%d-%m-%Y')
    #df['time_stamp']=date_today

    #saving the data as .csv
    df.to_csv(f'media/crypto-data-for-{date_today}.csv', index=False)
    print('Crypto CSV saved successfully')
else:
    print("ERROR ENCOUNTERED DURING CONNECTION")