#! /usr/bin/env python3


import asyncio
import ssl
import websockets
import json

ssl_context = ssl._create_unverified_context()

smd_req = 'smd+265598+{"fields":["31"]}'

async def market_data_requests(mdd_requests):
    async with websockets.connect("wss://192.168.1.127:5000/v1/api/ws", ssl=ssl_context) as websocket:
        print(mdd_requests)
        while True:
            await asyncio.sleep(1)
            await websocket.send(mdd_requests)
            res = await websocket.recv()
            result_dict = json.loads(res.decode())
            print(result_dict)


asyncio.get_event_loop().run_until_complete(market_data_requests(smd_req))
