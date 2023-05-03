#! /usr/bin/env python3

import json
import requests
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-a', '--address', help = "provide server ip address")
args = parser.parse_args()

local_ip = "192.168.1.167:5000"
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
    #
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
    
def placeOrder(accId: str, orderDict: dict):
    endpoint = f'/iserver/account/{accId}/orders'
    data = { "orders": [
        orderDict 
        ]
        
    }
    resp = requests.post(base_url + endpoint, verify=False, json=data,
            headers=headers)
    jsonData = json.loads(resp.text)
    messages = {}
    print(type(jsonData))
    if type(jsonData) == dict and "error" in jsonData.keys():
        print("ERROR: ", jsonData['error'])
        messages['error'] = jsonData['error']

    else:
        for el in jsonData:
            if "id" in el.keys():
                if el['id'] not in messages.keys():
                    messages['id'] = el['id']
                    messages['message'] = el['message']
    return messages                

def cancelOrder(accountID, orderID):
    endpoint = f'/iserver/account/{accountID}/order/{orderID}'
    resp = requests.delete(base_url + endpoint, verify=False, headers=headers)
    print(resp.text)

def getContractRules(conID):
    print("is called")
    endpoint = '/iserver/contract/rules'
    data = {'conid': conID, "isBuy": True}
    response = requests.post(base_url + endpoint, json=data, verify=False,
            headers=headers)
    print(response.text)

# Available assetClass values: STK, OPT, FUT, CFD, WAR, SWP, FND, BND, ICS
def getTradingSchedule(assetClass, symbol, exchange=None, exchangeFilter=None):
    endpoint = base_url + "/trsrv/secdef/schedule"
    data = {"assetClass": assetClass, 
            "symbol": symbol,
            "exchange": exchange if exchange is not None else "",
            "exchangeFilter": exchangeFilter if exchangeFilter is not None else ""
            }
    respose = requests.get(endpoint, verify=False, params=data, headers=headers) 
    print(respose.text)

def getSecDefPerConId(conids: list):
    endpoint = base_url + "/trsrv/secdef"
    data={"conids": conids}
    print(data)
    respose = requests.post(endpoint, verify=False, json=data, headers=headers)
    jsonData = json.loads(respose.text)['secdef']
    return jsonData

def createOrderPayload(accId: str, conId: int, orderType: str, exchange: str,
        orth, price: int, action, symbol, quantity, tif):
    data = { 
            "acctId": accId,
            "conid": conId,
            "secType": f"secType = {conId}:FUT",
            "orderType": orderType,
            "listingExchange": exchange,
            "outsideRTH": orth,
            "price": price,
            "side": action,
            "ticker": symbol,
            "quantity": quantity,
            "tif": tif
            }

    return data

def createMutliplePayloads(conDefList):
    payloads = []
    for con in conDefList:
        payload = createOrderPayload(
                accId="0test0",
                conId=con['conid'],
                orderType="LMT",
                exchange=con['listingExchange'],
                orth=True,
                price=1,
                action="BUY",
                symbol=con['ticker'],
                quantity=1,
                tif="DAY"
                 )
        payloads.append(payload)
    return payloads

def orderReply(replyID):
    endpoint = base_url + f"/iserver/reply/{replyID}"
    data = {'confirmed': True}
    response = requests.post(endpoint, verify=False, json=data, headers=headers)
    print("REPLY endpoint: ", response.text)
    jsonData = json.loads(response.text)
    print(jsonData)
    for e in jsonData:
        if type(e) is dict:
            if 'id' in e.keys():
                orderReply(e['id'])
        else:
            print(e)

def main():
    # Place an order, reply, monitor websockets for updates of sor+{} requests
    checkAuthStatus()
    contracts = futuresContractPerSymbol("MES")
    contract = getSpecificContractDetails(contracts[0]['conid'])
#    getContractRules(contracts[0]['conid'])
#    print(contract)
#    getTradingSchedule(contract['instrument_type'], contract['symbol'])
    conIdList = [con['conid'] for con in contracts]
    conDefList = getSecDefPerConId(conIdList)
    # Take one contract from a list and place order for it
    curCon = conDefList[0]
    accountId = getAccounts()[0]
    print("Current accountID: ", accountId)
    print("Current contract: ", curCon)
    payload = createOrderPayload(
            accId=accountId,
            conId=curCon['conid'],
            orderType="LMT",
            exchange=curCon['listingExchange'],
            orth=False,
            price=4445,
            action="BUY",
            symbol=curCon['ticker'],
            quantity=5,
            tif="DAY"
             )
    print("Current payload:", payload)
    messages = placeOrder(accountId, payload)
    if "error" not in messages.keys():
        print(messages)
        replyId = messages['id']
        orderReply(replyId)
    else:
        print(messages['error'])

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
