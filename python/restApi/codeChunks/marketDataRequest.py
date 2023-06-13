#! /usr/bin/env python3

import asyncio
import ssl
import json
import requests
import websockets

ssl_context = ssl._create_unverified_context()

local_ip = "127.0.0.1:5000"
base_url = f"https://{local_ip}/v1/api"

# Streaming data request, accepts comma-separated values
def subscribeMarketData(conId: str, fields: str):
    fields = fields.split(',')
#    msg = "smd+" + conId + '+' + '{"fields":["31","83"]}'
    msg = "smd+" + conId + '+' + json.dumps({"fields": fields})
    return msg

def unsubscribeMarketData(conId):
    msg = f"umd+{conId}+{{}}" 
    return msg

async def sendMessages(msgList):

    messages = msgList 
    marketDataResponses = 0

    async with websockets.connect("wss://" + local_ip + "/v1/api/ws", ssl=ssl_context) as websocket:

        while True:
            if len(messages) != 0:
                currentMsg = messages.pop(0)
                await asyncio.sleep(1)
                await websocket.send(currentMsg)

            rst = await websocket.recv()
            jsonData = json.loads(rst.decode())

            if 'error' in jsonData.keys():
                print(jsonData['error'])

            if 'topic' in jsonData.keys():

                if jsonData['topic'] == "system": 
                    # Keep session alive 
                    print("Sending {tic} to keep session alive. \n")
                    messages.append('tic')

                if "smd" in jsonData['topic']:
                    print(f"Market data for {jsonData['conid']}---> {jsonData}\n")
                    marketDataResponses += 1
                    if marketDataResponses == 2:
                        # Cancelling does not trigger any response
                        print("Cancelling after two market data responses: ")
                        msg = unsubscribeMarketData(jsonData['conid'])
                        messages.append(msg)

            else:
                print("Exceptions: ", jsonData)
            
#            print(jsonData)

            
def main():
    msgList = []  
    markeDataMsg = subscribeMarketData("265598", "31,83")
    msgList.append(markeDataMsg)
    asyncio.get_event_loop().run_until_complete(sendMessages(msgList))

if __name__ == "__main__":
    main()
