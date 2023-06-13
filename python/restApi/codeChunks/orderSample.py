#! /usr/bin/env python3

import asyncio
import ssl
import json
import requests
import websockets

ssl_context = ssl._create_unverified_context()

local_ip = "127.0.0.1:5000"
base_url = f"https://{local_ip}/v1/api"

def getAccounts():
    resp = requests.get(base_url + "/iserver/accounts", verify=False) 
    jsonData = json.loads(resp.text)
    accounts = jsonData['accounts']
    return accounts[0]

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

def orderReply(replyID):
    endpoint = base_url + f"/iserver/reply/{replyID}"
    data = {'confirmed': True}
    response = requests.post(endpoint, verify=False, json=data)
    print(f"REPLY to {replyID}: ", response.text)
    jsonData = json.loads(response.text)
    for e in jsonData:
        if type(e) is dict:
            if 'id' in e.keys():
                orderReply(e['id'])
            else:
                print("JSON: ", jsonData, e)
                return jsonData

def placeOrder(accId: str, orderDict: dict):
    endpoint = f'/iserver/account/{accId}/orders'
    data = { "orders": [
        orderDict 
        ]
        
    }
    print(data)
    resp = requests.post(base_url + endpoint, verify=False, json=data)
    print(resp.text)
    jsonData = json.loads(resp.text)

    for el in jsonData:
        if "id" in el.keys():
            jsonData = orderReply(el['id'])

    return jsonData 

def subscribeLiveOrderUpdates():
    msg = "sor+{}"
    return msg

def unsubscribeLiveOrderUpdates():
    msg = "uor+{}"
    return msg

async def sendMessages(msgList):

    messages = msgList 
    ordersSent = False 
    orderUpdates = 0

    async with websockets.connect("wss://" + local_ip + "/v1/api/ws", ssl=ssl_context) as websocket:

        while True:
            if len(messages) != 0:
                currentMsg = messages.pop(0)
                await asyncio.sleep(1)
                await websocket.send(currentMsg)
           
           # Orders will only be picked up by websocket stream
           # only `if they were placed after we have subscribed to 
           # updates.

            if ordersSent == False:
                accId = getAccounts()
                mktOrder = createMarketOrderPayload(accId=accId, 
                        conId=265598, 
                        exchange="SMART",
                        orth=False,
                        action="BUY",
                        symbol="AAPL",
                        quantity=1,
                        tif="DAY")
                placeOrder(accId, mktOrder)
                ordersSent = True

            rst = await websocket.recv()
            jsonData = json.loads(rst.decode())

            if 'topic' in jsonData.keys():

                if jsonData['topic'] == "sts":
                    print(f"Session info: \n{jsonData['args']}")

                if jsonData['topic'] == "act":
                    print(f"User data: \n{jsonData['args']}")

                if jsonData['topic'] == "system": 
                    # Keep session alive 
                    messages.append('tic')

                if jsonData['topic'] == "sor":
                    print(f"Order update ----> {jsonData}")
                    orderUpdates += 1
                    if orderUpdates > 2:
                        print("Unsubscribing from live order updates")
                        msg = unsubscribeLiveOrderUpdates()
                        await websocket.send(msg)

            if 'error' in jsonData.keys():
                print(jsonData['error'])
            

            
def main():
    msgList = [subscribeLiveOrderUpdates()]  
    asyncio.get_event_loop().run_until_complete(sendMessages(msgList))

if __name__ == "__main__":
    main()
