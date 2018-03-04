__author__ = "samrohn77@gmail.com"

from bs4 import BeautifulSoup
import pandas as pd
from pymongo import MongoClient
import requests
import json
import datetime
import pytz

def get_db():
    client = MongoClient('localhost:27017')
    db = client.cmcdata
    return db

def update_db(data):
    pass

def get_cmc_data():
    url = "https://coinmarketcap.com/all/views/all/"
    html = requests.get(url).text

    soup = BeautifulSoup(html, 'lxml') # pass the html to lxml parser
    table = soup.find_all('table')[0]  # find table from html
    df = pd.read_html(str(table))      
    k = (df[0].to_json(orient='records')) # 
    data = json.loads(k)
    return data

def insert_data(db, data):
    now = datetime.datetime.now()
    date_tod = now.strftime("%Y-%m-%d")
    for rec in data:
        coin = rec['Name']
        print coin
        #continue
        res = db.cryptodata.find({"name" : coin})
        
        if res.count() > 0:
            up_data = {}
            up_data['date'] = date_tod
            up_data['rank'] = rec['#']
            up_data['ticker'] = rec['Symbol']
            up_data['price'] = rec['Price']
            up_data['% 7d'] = rec['% 7d']
            up_data['Volume (24h)'] = rec['Volume (24h)']
            up_data['% 24h'] = rec['% 24h']
            up_data['market_cap'] = rec['Market Cap']
            up_data['% 1hr'] = rec['% 1h']
            up_data['ciculating_supply'] = rec['Circulating Supply']
            print 'coin already exists.Updating'
            db.cryptodata.update({"name" : coin},{'$push':{'data': up_data}})
            
        else:
            print 'inserting coin, ', coin
            record = {}
            db.cryptodata
            record['name'] = coin
            record['data'] = []
            details = {}
            now = datetime.datetime.now()
            cet_tz = pytz.timezone('CET')
            #date_tod = now.strftime("%Y-%m-%d")
            #date_tod = cet_tz.localize(now)
            date_tod = now.strftime("%Y-%m-%d")
            #print date_tod
            details['date'] = date_tod
            details['rank'] = rec['#']
            details['ticker'] = rec['Symbol']
            details['price'] = rec['Price']
            details['% 7d'] = rec['% 7d']
            details['Volume (24h)'] = rec['Volume (24h)']
            details['% 24h'] = rec['% 24h']
            details['market_cap'] = rec['Market Cap']

            details['% 1h'] = rec['% 1h']
            details['circulating_supply'] = rec['Circulating Supply']

            record['data'].append(details)
            print '-- ', json.dumps(record)
            db.cryptodata.insert(record)

            #print json.dumps(record)
        

if __name__ == '__main__':
    data = get_cmc_data()
    db = get_db()
    #print db.cmcdata.collection
    #clc = db.cryptodata
    #res =  db.cryptodata.find({})
    #for each in data:
    #    print each
    insert_data(db, data)
