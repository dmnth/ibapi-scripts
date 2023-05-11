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
async def historicalDataRequest(msg):
    serverIds = [] 
    async with websockets.connect("wss://" + local_ip + "/v1/api/ws", ssl=ssl_context) as websocket:
        while True:
            await asyncio.sleep(1)
            await websocket.send(msg)

            rst = await websocket.recv()
            result_dict = json.loads(rst.decode())
            print(result_dict)

            # Note the serverId since it will be required to unsubscribe from historica data
            if "serverId" in result_dict.keys():
                currentID = result_dict['serverId']
                msg = unsubscibeHistoricalData(currentID)
                await websocket.send(msg)
                break

            # Since only 5 concurrent historical requests are allowed - unsubscibe
            if 'error' in result_dict.keys():
                if result_dict['error'] == CpError.tooManyCharts: 
                    print("Following error occured: ", result_dict['error']) 
                    # Unsubsribe from historical data, get serverID. Should be present in response.
                else:
                    print(result_dict['error'])

def simpleConnection(msg):
    with websockets.connect("wss://" + local_ip + "/v1/api/ws") as socket:
        socket.send(msg)
        resp = socket.recv()
        print(resp)

def main():
    smd_req = create_SMD_req('265598', "31, 84, 86")
    smh_req = create_SMH_req("265598", "1d", "1hour", "trades", "%o/%c/%h/%l") 
    sor_req = create_SOR_req()
#    asyncio.get_event_loop().run_until_complete(historicalDataRequest(smh_req))
    simpleConnection(smd_req)

if __name__ == "__main__":
    main()
