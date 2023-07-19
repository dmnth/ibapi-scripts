#! /usr/bin/env python3

import asyncio
import ssl
import json
import requests
import websockets

ssl_context = ssl._create_unverified_context()

local_ip = "127.0.0.1:5000"
base_url = f"https://{local_ip}/v1/api"

#Historical data payload:
def create_SMH_req(conID, period, barSize, dataType, dateFormat):
    msg = f"smh+{conID}+" + json.dumps({
        "period": period,
        "bar": barSize,
        "source": dataType,
        "format": dateFormat 
        }) 
    return msg

def authStatus():
    resp = requests.post(base_url + "/iserver/auth/status", verify=False) 
    if resp.status_code == 200:
        print(resp.text)
    else:
        raise RuntimeError(f"Received http status code: {resp.status_code}")


def getAccountId():
    resp = requests.get(base_url + "/iserver/accounts", verify=False) 
    if resp.status_code == 200:
        jsonData = json.loads(resp.text)
        accounts = jsonData['accounts']
        return accounts
    else:
        print(resp.status_code, resp.text)
        raise RuntimeError("!???")

def searchBySymbol(symbol: str, sectype: str):
    data = {
            "symbol": symbol,
            "name": True,
            "secType": sectype,
            }
    resp = requests.post(base_url + "/iserver/secdef/search", json=data, verify=False)
    if resp.status_code == 200:
        jsonData = json.loads(resp.text)
        print(jsonData)
        conid = jsonData[0]['conid']
        return conid
    else:
        raise RuntimeError(f"Nothing found for symbol {symbol} because of response status code: {resp.status_code}")

def getContractDetails(conId):
    endpoint = f"/iserver/contract/{conId}/info"
    data = {"conid": conId}
    resp = requests.get(base_url + endpoint, verify=False, params=data)
    if resp.status_code == 200:
        jsonData = json.loads(resp.text)
        return jsonData
    else:
        raise RuntimeError(f"No contracts found for {conId}")

# Streaming data request, accepts comma-separated values
def create_SMD_req(conId, args: str):
    args = args.split(',')
    msg = "smd+" + conId + '+' + '{"fields":["31","83"]}'
    msg = "smd+" + conId + '+' + json.dumps({"fields":args})
    return msg

def marketDepthRequest(conID, acctID=None, exchange=None):

    if acctID is None:
        acctIDs = getAccountId()
        acctID = acctIDs[0]

    if exchange is None:
        details = getContractDetails(conID)
        exchange = details['exchange']

    msg = f"sbd+{acctID}+{conID}+{exchange}"

    return msg 


# Live order updates request
def create_SOR_req():
    msg = "sor+{}"
    return msg

def create_STR_req():
    msg = 'str+{"realtimeUpdatesOnly": true}'
    return

def unsubscibeHistoricalData(serverID):
    msg = "umh+" + serverID 
    return msg

def createRequests(conId):
    smd_req = create_SMD_req(conId, "31, 84, 86")
    smh_req = create_SMH_req(conId, "1d", "1hour", "trades", "%o/%c/%h/%l") 
    sor_req = create_SOR_req()
    str_req = create_STR_req()
    mktDpthReq = marketDepthRequest(conId) 
    msgList = [smd_req, sor_req, smh_req, mktDpthReq]

    return msgList


async def sendMessages(msgList):

    messages = msgList 
    mktDepthUnsubscribed = False
    historicalDataUnsubscribed = False

    async with websockets.connect("wss://" + local_ip + "/v1/api/ws", ssl=ssl_context) as websocket:
        while True:
            if len(messages) != 0:
                # *Imitates queue* 
                currentMsg = messages.pop(0)
                await asyncio.sleep(1)
                await websocket.send(currentMsg)

            rst = await websocket.recv()
            jsonData = json.loads(rst.decode())

            if 'topic' in jsonData.keys():

                if jsonData['topic'].startswith("smh+") and historicalDataUnsubscribed == False:
                    serverID = jsonData['serverId']
                    msg = unsubscibeHistoricalData(serverID)
                    messages.append(msg)
                    historicalDataUnsubscribed = True
                    print("historical data should be unsubscribed now")

                if jsonData['topic'] == "sbd" and mktDepthUnsubscribed == False:
                    acctID = getAccountId()
                    msg = f"ubd+{acctID}"
                    messages.append(msg)
                    mktDepthUnsubscribed = True
                    print("Market depth data was unsubscribed")

                if jsonData['topic'] == "system": 
                    # Keep session alive 
                    messages.append('tic')

            if 'error' in jsonData.keys():
                print(jsonData['error'])

            
            print(jsonData)

def main():
    conId = searchBySymbol("TSLA", "STK")
    msgList = createRequests(conId)
    asyncio.get_event_loop().run_until_complete(sendMessages(msgList))

if __name__ == "__main__":
    main()
