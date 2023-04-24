#! /usr/bin/env python3


import asyncio
import ssl
import json
import requests
import websockets

ssl_context = ssl._create_unverified_context()

local_ip = "127.0.0.1:5000"
base_url = f"https://{local_ip}/v1/api"

# Streaming data request
def create_SMD_req(conId, args):
#    msg = "smd+" + conId + '+' + '{"fields":["31","83"]}'
    msg = "smd+" + conId + '+' + json.dumps({"fields":args})
    return msg

async def market_data_requests(mdd_requests):
    async with websockets.connect("wss://" + local_ip + "/v1/api/ws", ssl=ssl_context) as websocket:
        while True:
            await asyncio.sleep(1)
            for req in mdd_requests:
                await websocket.send(req)
            rst = await websocket.recv()
            result_dict = json.loads(rst.decode())
            print("Response: ", result_dict)


def main():
    smd_req = create_SMD_req('265598', ['31', '83', '84', '85', '86'])
    smd_req1 = create_SMD_req('474641211', ['31', '83', '84', '85', '86'])
    smd_req2 = create_SMD_req('431039863', ['31', '83', '84', '85', '86'])
    req_list = [smd_req2, smd_req1, smd_req]
    asyncio.get_event_loop().run_until_complete(market_data_requests(req_list))

if __name__ == "__main__":
    main()
