#! /usr/bin/env python3

import websockets
import json
import asyncio
import ssl

local_ip = "127.0.0.1:5000"
ssl_context = ssl._create_unverified_context()

async def sendMessages():

    async with websockets.connect("wss://" + local_ip + "/v1/api/ws", ssl=ssl_context, extra_headers={'set-cookie': None}) as websocket:
        while True:
            rst = await websocket.recv()
            jsonData = json.loads(rst.decode())
            print(jsonData)

asyncio.get_event_loop().run_until_complete(sendMessages())
