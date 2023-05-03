#! /usr/bin/env python3


import asyncio
import ssl
import json
import requests
import websockets

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

# Streaming data request
def create_SMD_req(conId, args):
#    msg = "smd+" + conId + '+' + '{"fields":["31","83"]}'
    msg = "smd+" + conId + '+' + json.dumps({"fields":args})
    return msg

def processHistoricaReq(serverID):
    # Escape curly braces with f string by adding more curly braces
    msg = "umh+" + f"{{{serverID}}}"
    return msg

async def market_data_requests(mdd_request):
    async with websockets.connect("wss://" + local_ip + "/v1/api/ws", ssl=ssl_context) as websocket:
        while True:
            await asyncio.sleep(1)
            await websocket.send(mdd_request)
            rst = await websocket.recv()
            result_dict = json.loads(rst.decode())
            # Since only 5 concurrent historical requests are allowed - unsubscibe
            if "serverId" in result_dict.keys():
                serverId = result_dict['serverId']
                msg = processHistoricaReq(serverId)
                await websocket.send(msg)
                res = await websocket.recv()
                print(res)
                break
            print(result_dict)


def main():
    smd_req = create_SMD_req('265598', ['31', '83', '84', '85', '86'])
    smh_req = create_SMH_req("265598", "1d", "1hour", "trades", "%o/%c/%h/%l") 
    asyncio.get_event_loop().run_until_complete(market_data_requests(smd_req))

if __name__ == "__main__":
    main()
