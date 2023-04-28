#! /usr/bin/env python3

import json
import requests
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-a', '--address', help = "provide server ip address")
args = parser.parse_args()

local_ip = "192.168.43.222:5000"
base_url = f"https://{local_ip}/v1/api"
headers = {
        "User-Agent": "python-requests/2.28.1",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "*/*",
        "Connection": "keep-alive",
        "Content-type": "application/json"
        }


def checkAuthStatus():
    resp = requests.get(base_url + "/iserver/auth/status", verify=False)
    jsonData = json.loads(resp.text)
    print(jsonData)

def accountTrades():
    resp = requests.get(base_url + "/iserver/account/trades", verify=False,
            headers=headers)
    jsonData = json.loads(resp.text)
    print(resp.headers)
    print(resp.content.decode())

def checkTypes(jsonData):
    for element in jsonData:
        for k,v in element.items():
            if type(k) == bytes or type(v) == bytes:
                print(f"some exception occured - {type(k)}: {type(v)}")
    print("Done comparing")
    
def placeOrder():
    endpoint = '/iserver/account/DU6036902/orders'
    params = { "orders": [
        {
        "acctId": "DU6036902",
        "conid": 265598,
        "secType": "secType = 265598:STK",
        "orderType": "LMT",
        "listingExchange": "SMART",
        "outsideRTH": True,
        "price": 1,
        "auxPrice": 0,
        "side": "BUY",
        "ticker": "AAPL",
        "tif": "DAY",
        "quantity": 12
        }
        ]
    }
    json_params = json.dumps(params)
    resp = requests.post(base_url + endpoint, verify=False, data=json_params,
            headers=headers)

def main():
    checkAuthStatus()
    accountTrades()

if __name__ == "__main__":
    if args.address == None:
        print("Please provide all required arguments")
        parser.print_help()
    else:
        print(args)
        main()
