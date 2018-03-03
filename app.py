import json
from collections import OrderedDict
from flask import Flask
from flask import request
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
    #coin = coin.split(",")
    auth_key = request.args.get('auth_key')
    db = get_db()
    if auth_key != "fdsrtw435s6af8dsd9sa":
        return "{ACCESS DENIED:Authentication Failed}"
    ret_data = OrderedDict()
    ret_data = []
    if coin: 
        coin = coin.split(",")
        
        for each in coin:
            lst = []
            if len(each)>0:
                data = db.cryptodata.find({'name':each})
                for hist_data in data:
                    for dts in hist_data['data']:
                        lst.append(dts)
                #ret_data[each] = lst
                ret_data.append(lst)
    return json.dumps({'data':ret_data})
    #else:
    #    data = db.cryptodata.find({})
    #ret_data = []
    #for hist_data in data:
    #    for dts in hist_data['data']:
    #        ret_data.append(dts)
    return json.dumps(OrderedDict(reversed(list(ret_data.items()))))

@app.route('/get_coin_list')
def get_coin_list():
    db = get_db()
    data = db.cryptodata.find({})
    coins = {}
    for each in data:
        for cn in each['data']:
            #return json.dumps(cn['org_name'])
            try:
                coin_name = cn['org_name']
                coins[coin_name] = cn['ticker']
            except:
                pass
    return json.dumps(coins)

if __name__ == '__main__':
    app.run(host="0.0.0.0",  debug=True)
