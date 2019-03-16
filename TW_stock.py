import requests
import json
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta
import time

data = {
    'response': 'json',
    'date': '20190312'
}
#res = requests.get('http://www.tse.com.tw/exchangeReport/MI_INDEX', params=data)
res = requests.get('http://www.tse.com.tw/exchangeReport/MI_INDEX?response=json&date=20190312')
#print(res.text)
#loads data to json.text
jres = json.loads(res.text)
jres['stat']
jres
jres['data1']
#print(jres['data1'])
#create a data frame
df_temp = pd.DataFrame(jres['data1'],columns=jres['fields1'])
#print(df_temp)

#build time index
timedelta(days=1)
datetime(2019,3,12) + timedelta(1)
datetime.strftime(datetime(2019,1,30), '%Y%m%d')#datetime formate
#create a empty data frame
column_list = list(df_temp['指數'])

column_list.append('date')
df = pd.DataFrame(columns=column_list)
print(df)

#crawling
crawl_date = datetime(2019,3,12) # start_date

for i in range(365):
    crawl_date -= timedelta(1)
    crawl_date_str = datetime.strftime(crawl_date, '%Y%m%d')
    res = requests.get('http://www.tse.com.tw/exchangeReport/MI_INDEX?response=json&date=' + crawl_date_str)
    jres = json.loads(res.text)

    # 證交所回覆有資料
    if(jres['stat']=='OK'):
        print(crawl_date_str, ': crawling data...')
        # 將讀取回的json轉成的DataFrame(df_temp)
        df_temp = pd.DataFrame(jres['data1'],columns=jres['fields1'])

        # load'漲跌百分比(%)' from df.temp  to df
        row_data = list(df_temp['漲跌百分比(%)'])
        row_data.append(crawl_date_str)
        df.loc[len(df)] = row_data
    else:
        print(crawl_date_str, ': no data')

    # sleep 3 sec avoid blocked
    time.sleep(3)
