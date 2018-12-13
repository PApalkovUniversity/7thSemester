import requests
import json


def parse_prices(prices):
    for key, value in prices.items():
        prices[key] = value["RUB"]

    return prices


def get_info():
    data = requests.get('https://min-api.cryptocompare.com/data/pricemulti?fsyms=BTC,ETH,USD,&tsyms=RUB')
    return parse_prices(data.json())



if __name__ == '__main__':
    print(get_info())
