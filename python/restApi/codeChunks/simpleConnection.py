#! /usr/bin/env python3

import asyncio
import ssl
import json
import requests
import websockets

ssl_context = ssl._create_unverified_context()

local_ip = "127.0.0.1:5000"
base_url = f"https://{local_ip}/v1/api"

async def sendMessages(msgList):

    messages = msgList 

    async with websockets.connect("wss://" + local_ip + "/v1/api/ws", ssl=ssl_context) as websocket:

        while True:
            if len(messages) != 0:
                currentMsg = messages.pop(0)
                await asyncio.sleep(1)
                await websocket.send(currentMsg)

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

            if 'error' in jsonData.keys():
                print(jsonData['error'])
            
            print(jsonData)

            
def main():
    msgList = []  
    asyncio.get_event_loop().run_until_complete(sendMessages(msgList))

if __name__ == "__main__":
    main()
