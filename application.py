import json
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

if __name__ == '__main__':
    app.run(host="0.0.0.0",  debug=True)
