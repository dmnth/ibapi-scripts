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


def futuresContractPerSymbol(symbol: str):
    endpoint = "/trsrv/futures"
    data = {"symbols": symbol}
    resp = requests.get(base_url + endpoint, verify=False, params=data)
    if resp.status_code == 200:
        jsonData = json.loads(resp.text)
        if len(jsonData.keys()) != 0:
            validContracts = jsonData[data['symbols']]
            return validContracts

def getSpecificContractDetails(conId):
    endpoint = f"/iserver/contract/{conId}/info"
    data = {"conid": conId}
    resp = requests.get(base_url + endpoint, verify=False, params=data)
    if resp.status_code == 200:
        jsonData = json.loads(resp.text)
        return jsonData

def getOrderIds():
    resp = requests.get(base_url + "/iserver/account/orders", verify=False, 
            headers=headers)
    jsonData = json.loads(resp.text)
    ids = []
    for order in jsonData['orders']:
        prettyJson = json.dumps(order, indent=4)
        if "orderId" in order.keys():
            if order['orderId'] not in ids:
                ids.append(order['orderId'])
    return ids

def getAccounts():
    resp = requests.get(base_url + "/iserver/accounts", verify=False, 
            headers=headers)
    jsonData = json.loads(resp.text)
    accounts = jsonData['accounts']
    if len(accounts) > 0:
        return accounts
    else:
        print("Go open an account, will ya.")

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

def cancelOrder(accountID, orderID):
    endpoint = f'/iserver/account/{accountID}/order/{orderID}'
    resp = requests.delete(base_url + endpoint, verify=False, headers=headers)
    print(resp.text)

def main():
    # Place an order, reply, monitor websockets for updates of sor+{} requests
    checkAuthStatus()
    contracts = futuresContractPerSymbol("MES")
    contract = getSpecificContractDetails(contracts[0]['conid'])
    print(contract)
#    accountTrades()
#    placeOrder()
#    orderIDs = getOrderIds()
#    accounts = getAccounts()
#    acc = accounts[0]
#    oid = orderIDs[0]
#    cancelOrder(acc, oid)

if __name__ == "__main__":
    if args.address == None:
        print("Please provide all required arguments")
        parser.print_help()
    else:
        print(args)
        main()
