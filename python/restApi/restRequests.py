#! /usr/bin/env python3

import json
import requests
import argparse
import time
import urllib
from time import sleep

parser = argparse.ArgumentParser()
parser.add_argument('-a', '--address', help = "provide server ip address")
args = parser.parse_args()

requests.packages.urllib3.disable_warnings()

local_ip = "127.0.0.1:5000"
base_url = f"https://{local_ip}/v1/api"
headers = {
        "User-Agent": "python-requests/2.28.1",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "*/*",
        "Connection": "keep-alive",
        "Content-type": "application/json"
        }

# /iserver/accounts should be queried
# A

def stocksBySymbol(symbol):
    endpoint = base_url + f"/trsrv/stocks"
    data = {
            "symbols": symbol
            }
    response = requests.get(endpoint, params=data, verify=False, headers=headers)
    jsonData = json.loads(response.text)
    return jsonData

def snapShotDataSubscribe(conIds: str, fields: str):
    endpoint = base_url + "/iserver/marketdata/snapshot"
    conIds = conIds.split(',')
#    fields = fields.split(',')
    data = {
            "conids": conIds,
            "fields": fields
            }
    response = requests.get(endpoint, verify=False, params=data, headers=headers)
    print(response.text)
    return

def snapShotDataUnsubscribe(conid):
    endpoint = base_url + f"/iserver/marketdata/{conid}/unsubscribe"
    data = {"conid": conid}
    response = requests.get(endpoint, params=data, verify=False, headers=headers)
    if response.status_code == 200:
        print(response.text)
    else:
        print(response.status_code, ", shit")

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

def callPortfolioAccounts():
    resp = requests.get(base_url + "/portfolio/accounts", verify=False)
    print(resp.text)

def checkAuthStatus():
    resp = requests.get(base_url + "/iserver/auth/status", verify=False)
    jsonData = json.loads(resp.text)
    return jsonData

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
    print(jsonData)

    for el in jsonData:
        if "id" in el.keys():
            jsonData = orderReply(el['id'])

    return jsonData 


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

def createLimitOrderPayload(accId: str, conId: int, exchange: str,
        orth, price: int, action, symbol, quantity, tif):
    data = { 
            "acctId": accId,
            "conid": conId,
            "secType": f"secType = {conId}:STK",
            "orderType": "LMT",
            "listingExchange": exchange,
            "outsideRTH": orth,
            "price": price,
            "side": action,
            "ticker": symbol,
            "quantity": quantity,
            "tif": tif
            }

    return data

def createMarketOrderPayload(accId: str, conId: int, exchange: str,
        orth, action, symbol, quantity, tif):
    data = { 
            "acctId": accId,
            "conid": conId,
            "secType": f"secType = {conId}:STK",
            "orderType": "MKT",
            "listingExchange": exchange,
            "outsideRTH": orth,
            "side": action,
            "ticker": symbol,
            "quantity": quantity,
            "tif": tif
            }

    return data

def createMutliplePayloads(accId, conDefList):
    payloads = []
    for con in conDefList:
        payload = createLimitOrderPayload(
                accId=accId,
                conId=con['conid'],
                exchange=con['listingExchange'],
                orth=False,
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
    print(f"REPLY to {replyID}: ", response.text)
    jsonData = json.loads(response.text)
    for e in jsonData:
        if type(e) is dict:
            if 'id' in e.keys():
                orderReply(e['id'])
            else:
                print("JSON: ", jsonData, e)
                return jsonData

def getOrderStatus(orderId):
    endpoint = base_url + f"/iserver/account/order/status/{orderId}"
    data = {'orderId': orderId}
    response = requests.get(endpoint, verify=False, params=data, headers=headers)
    jsonData = json.loads(response.text)
    print(jsonData)

def invalidatePositions(accId):
    endpoint = base_url + f"/portfolio/{accId}/positions/ivalidate"
    data = {"accountId": accId}
    response = requests.post(endpoint, json=data, verify=False, headers=headers)
    print(response.text)

def getPortfolioPositionsByPage(accId, pageId):
    data = {
            "accountId": accId,
            "pageId": pageId,
            "model": "",
            "sort": "",
            "direction": "",
            "period": ""
            }
    endpoint = base_url + f"/portfolio/{accId}/positions"
    response = requests.get(endpoint, params=data, verify=False, headers=headers)

    if response.status_code == 200:
        jsonData = json.loads(response.text)
        print("Positions --> ", jsonData)

    else:
        raise RuntimeError("")

def getPortfolioPositions(accId):
    data = {
            "accountId": accId,
            "model": "",
            "sort": "",
            "direction": "",
            "period": ""
            }
    endpoint = base_url + f"/portfolio/{accId}/positions"
    response = requests.get(endpoint, params=data, verify=False, headers=headers)

    if response.status_code == 200:
        jsonData = json.loads(response.text)
        print(jsonData)

    else:
        raise RuntimeError("")


def placeSingleOrder(symbol, exchange, action, orderType, tif, orth, quantity, price=None):
    contract = searchBySymbol(symbol, "STK")
    print(contract)
    accId = getAccounts()[0]
    if orderType == "LMT":
        orderPayload = createLimitOrderPayload(
                accId = accId,
                conId=int(contract['conid']),
                exchange=exchange,
                orth=orth,
                price=price if price is not None else 0,
                action=action,
                symbol=contract['symbol'],
                quantity=quantity,
                tif=tif
                )
    if orderType == "MKT":
        orderPayload = createMarketOrderPayload(
                accId = accId,
                conId=int(contract['conid']),
                exchange=exchange,
                orth=orth,
                action=action,
                symbol=contract['symbol'],
                quantity=quantity,
                tif=tif
                )
    message = placeOrder(accId, orderPayload)
    if "id" in message.keys():
        replyId = message['id']
        # orderReply function implements recursive call so
        # all queries have relevant reply.
        orderData = orderReply(replyId)



def placesFutOrders(symbol):
    contracts = futuresContractPerSymbol(symbol)
    contract = getSpecificContractDetails(contracts[0]['conid'])
    conIdList = [con['conid'] for con in contracts]
    conDefList = getSecDefPerConId(conIdList)
    # Take one contract from a list and place order for it
    curCon = conDefList[0]
    accountId = getAccounts()[0]
    print("Current accountID: ", accountId)
    print("Current contract: ", curCon) 
    singlePayload = createLimitOrderPayload(
            accId=accountId,
            conId=curCon['conid'],
            exchange=curCon['listingExchange'],
            orth=False,
            price=4430,
            action="SELL",
            symbol=curCon['ticker'],
            quantity=5,
            tif="DAY"
             )
    print("Current payload:", singlePayload)
    payloads = createMutliplePayloads(accountId, conDefList)
    for p in payloads:
        messages = placeOrder(accountId, p)
        print(messages)



def getLiveOrders():
    endpoint = base_url + "/iserver/account/orders"
    response = requests.get(endpoint, verify=False, headers=headers)
    jsonData = json.loads(response.text)
    orderIds = []
    for order in jsonData['orders']:
        orderIds.append(order['orderId'])

    return orderIds

def searchBySymbol(symbol: str, sectype: str):
    data = {
            "symbol": symbol,
            "name": True,
            "secType": sectype,
            }
    resp = requests.post(base_url + "/iserver/secdef/search", json=data, verify=False)
    if resp.status_code == 200:
        jsonData = json.loads(resp.text)
        contract = jsonData[0]
        return contract 
    else:
        raise RuntimeError(f"Nothing found for symbol {symbol}")

def cancelOrder(accountID, orderID):
    endpoint = f'/iserver/account/{accountID}/order/{orderID}'
    print(orderID)
    if type(orderID) == list:
        orderID = ','.join(str(i) for i in orderID)
        orderID = f'[{orderID}]'
        print("ORDER LIST TO CANCEL: ", orderID)
    data = {"accountId": accountID, "orderId": orderID}
    resp = requests.delete(base_url + endpoint, params=data, verify=False, headers=headers)
    print("Cancel order response: ", resp.text)

def cancelAllOrders():
    # to cancel all orders send -1 as ID value
    orderIds = getLiveOrders()
    accId = getAccounts()[0]
    cancelOrder(accId, orderIds)

#    while len(orderIds) != 0:
#        toCancelId = orderIds.pop(0)
#        cancelOrder(accId, toCancelId)

def main():
    checkAuthStatus()
    placesFutOrders("BMW")
#    print(getLiveOrders())
    cancelAllOrders()
    while True:
        print(getLiveOrders())
        sleep(1)
#    response = placeOrder(accountID, payload)
    # need to implement order reply logic into placeOrder function
#    print(response)
    # Make it return 500 or 503 on order confirmation
#    placeSingleOrder(symbol="BMW", exchange="SMART", orderType="MKT", action="BUY", tif="DAY", orth=False, quantity=700)

if __name__ == "__main__":
    if args.address == None:
        print("Please provide all required arguments")
        parser.print_help()
    else:
        print(args)
        main()
