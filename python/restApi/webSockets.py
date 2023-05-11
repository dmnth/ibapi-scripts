#! /usr/bin/env python3


import asyncio
import ssl
import json
import requests
import websockets
from errors import CpError

ssl_context = ssl._create_unverified_context()

local_ip = "192.168.43.222:5000"
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

# Streaming data request, accepts comma-separated values
def create_SMD_req(conId, args: str):
    args = args.split(',')
#    msg = "smd+" + conId + '+' + '{"fields":["31","83"]}'
    msg = "smd+" + conId + '+' + json.dumps({"fields":args})
    return msg

# Live order updates request
def create_SOR_req():
    msg = "sor+{}"
    return msg

def unsubscibeHistoricalData(serverID):
    # Escape curly braces with f string by adding more curly braces
    msg = "umh+" + serverID 
    return msg

async def market_data_requests(mdd_request):
    async with websockets.connect("wss://" + local_ip + "/v1/api/ws", ssl=ssl_context) as websocket:
        while True:
            await asyncio.sleep(1)
            await websocket.send(mdd_request)
            rst = await websocket.recv()
            result_dict = json.loads(rst.decode())
            # Since only 5 concurrent historical requests are allowed - unsubscibe
            print(result_dict)

# Allows 5 concurrent requests, serverID is required to unsubscribe.
async def sendMessages(msgLst):
    async with websockets.connect("wss://" + local_ip + "/v1/api/ws", ssl=ssl_context) as websocket:
        while True:
            # Create a queue of messages
            if len(msgLst) != 0:
                currentMsg = msgLst.pop(0)
                await asyncio.sleep(1)
                await websocket.send(currentMsg)

            # Process the responses
            rst = await websocket.recv()
            result_dict = json.loads(rst.decode())

            if 'topic' in result_dict.keys():

                if result_dict['topic'].startswith("smh+"):
                    serverID = result_dict['serverId']
                    msg = unsubscibeHistoricalData(serverID)
                    await websocket.send(msg)
                    print("historical data should be unsubscribed now")

            if 'error' in result_dict.keys():
                print(result_dict['error'])
            
            print(result_dict)

def main():
    smd_req = create_SMD_req('265598', "31, 84, 86")
    smh_req = create_SMH_req("265598", "1d", "1hour", "trades", "%o/%c/%h/%l") 
    sor_req = create_SOR_req()
    msgList = [smd_req, sor_req, smh_req]
    asyncio.get_event_loop().run_until_complete(sendMessages(msgList))
    simpleConnection(smd_req)

if __name__ == "__main__":
    main()
