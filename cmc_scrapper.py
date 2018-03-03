from bs4 import BeautifulSoup
import pandas as pd
import json
import requests

def process_response(url):
    #soup = BeautifulSoup(resp, 'lxml')
    #table = soup.findall('table')
    #print table
    #df = pd.read_html(str(table))
    df = pd.read_html(url)
    #js = (df[0].to_json(orient='records'))
    #js_data = json.loads(js)
    with open('data.txt', 'w') as f:
        for each in df:
            f.write(str(each))

def get_coins():
    url = "https://api.coinmarketcap.com/v1/ticker/?limit=500"
    resp = requests.get(url)
    data = json.loads(resp.text)
    coin_list = []
    for each in data:
        coin_list.append(each['id'])

    return coin_list


def main():
    url = "https://coinmarketcap.com/all/views/all/"
    resp = requests.get(url)
    process_response(resp.text)

if __name__ == "__main__":
    main()
