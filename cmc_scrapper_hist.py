__author__ = "samrohn77@gmail.com"

from bs4 import BeautifulSoup
import pandas as pd
from pymongo import MongoClient
import requests
import json
import datetime
import pytz


dates = ['20130428', '20130505','20130512', '20130519','20130526', '20130602', '20130609','20130616', '20130623','20130630','20130707','20130714','20130721','20130728',
        '20130804','20130811','20130818','20130825','20130901','20130908','20130915','20130922','20130929'] # 2013

dates = ['20140406', '20140413', '20140420','20140427','20140504','20140511','20140518','20140525','20140601', '20140608', '20140615','20140622', '20140629'] # 2014
def get_db():
    client = MongoClient('localhost:27017')
    db = client.cmcdata
    return db

def update_db(data):
    pass

def get_cmc_data(url):
    html  = requests.get(url).text

    soup = BeautifulSoup(html, 'lxml') # pass the html to lxml parser
    table = soup.find_all('table')[0]  # find table from html
    df = pd.read_html(str(table))      
    k = (df[0].to_json(orient='records')) # 
    data = json.loads(k)
    return data

def insert_data(db, data, his_date):
    for each in data:
        print each
    
    now = datetime.datetime.now()
    #date_tod = his_date.strftime("%Y-%m-%d")
    his_date = datetime.datetime.strptime(his_date, "%Y%m%d").strftime("%Y-%m-%d")
    for rec in data:
        print rec
        res = db.cryptodata.find({"name" : rec['Symbol']})
        if res.count() > 0:
            up_data = {}
            up_data['date'] = his_date
            up_data['rank'] = rec['#']
            up_data['name'] = rec['Name']
            up_data['price'] = rec['Price']
            up_data['% 7d'] = rec['% 7d']
            up_data['Volume (24h)'] = rec['Volume (24h)']
            up_data['% 24h'] = rec['% 24h']
            up_data['market_cap'] = rec['Market Cap']
            print 'coin already exists.Updating'
            db.cryptodata.update({"name" : rec['Symbol']},{'$push':{'data': up_data}})
            
        else:
            print 'inserting coin, ', rec['Symbol']
            record = {}
            db.cryptodata
            record['name'] = rec['Symbol']
            record['data'] = []
            details = {}
            
            cet_tz = pytz.timezone('CET')
            #date_tod = now.strftime("%Y-%m-%d")
            #date_tod = cet_tz.localize(now)
            #date_tod = str(now.strftime("%Y-%m-%d"))
            #print date_tod
            details['date'] = his_date
            details['rank'] = rec['#']
            details['name'] = rec['Name']
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
    #data = get_cmc_data()
    db = get_db()
    for each in dates:
        url = "https://coinmarketcap.com/historical/" + each
        data = get_cmc_data(url)
        insert_data(db, data, each)
    #print db.cmcdata.collection
    #clc = db.cryptodata
    #res =  db.cryptodata.find({})
    #for each in res:
    #    print each
    #insert_data(db, data,)
