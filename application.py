import json
import requests
from flask import Flask
from flask import request
from bs4 import BeautifulSoup
import pandas as pd
import pymongo
from pymongo import MongoClient
app = Flask(__name__)


@app.route('/')
def btc():
    return json.dumps({"#":"1", "name":"BTC Bitcoin", "price":"$11260.20", "Volume (24h)":"$7,689,590,000", "Market Cap":"$190,012,350,557", "Symbol": "BTC"})

def get_db():
    client = MongoClient('localhost:27017')
    db = client.cmcdata
    return db

@app.route('/get_data')
def get_data():
    coin = request.args.get('coin_name')
    #coin_List = coin.split(",")
    auth_key = request.args.get('auth_key')
    db = get_db()
    if auth_key != "fdsrtw435s6af8dsd9sa":
        return "{ACCESS DENIED:Authentication Failed}"
    if coin: 
        coin = coin.split(",")
        data = db.cryptodata.find({'name':coin[0]})
    else:
        data = db.cryptodata.find({})
    ret_data = []
    for hist_data in data:
        for dts in hist_data['data']:
            ret_data.append(dts)
    return json.dumps(ret_data)

@app.route('/get_coin_list') 
def get_coin_list(): 
    db = get_db() 
    data = db.cryptodata.find({}) 
    coins = {}
    a = []
    for each in data: 
        for cn in each['data']: 
            #print cn
            #return json.dumps(cn['org_name']) 
            try: 
                #coin_name = cn['org_name'] 
                a.append({cn['org_name']: cn['ticker']})
            except Exception as e: 
                #print e
                #return e
                pass 
    
    coins["data"] = a
    
    return json.dumps(coins)

@app.route('/get_coins')
def get_coins():
    url = "https://coinmarketcap.com/all/views/all/" 
    html = requests.get(url).text 
    soup = BeautifulSoup(html, 'lxml') # pass the html to lxml parser 
    table = soup.find_all('table')[0] # find table from html 
    df = pd.read_html(str(table)) 
    k = (df[0].to_json(orient='records')) # 
    data = json.loads(k) 
    coin_list = []
    for rec in data: 
        coin_list.append({"coin":rec['Name'], "ticker":rec['Symbol']})

    return json.dumps({"coins":coin_list})


if __name__ == '__main__':
    app.run(host="0.0.0.0",  debug=True)
