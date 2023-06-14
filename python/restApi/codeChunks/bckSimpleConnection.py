#! /usr/bin/env python3

import asyncio
import ssl
import json
import requests
import websockets
import time 
import datetime

ssl_context = ssl._create_unverified_context()

local_ip = "127.0.0.1:5000"
base_url = f"https://{local_ip}/v1/api"

def timePassed():
    current_time = datetime.datetime.now()
    target_time = current_time + datetime.timedelta(minutes=5)
    while True:
        new_time = datetime.datetime.now()
        if new_time >= target_time:
            print("5mins passed")
            current_time = datetime.datetime.now()
            break
        else:
            print("5mins have not yet passed")

def subscribeMarketData(conId: str, fields: str):
    fields = fields.split(',')
#    msg = "smd+" + conId + '+' + '{"fields":["31","83"]}'
    msg = "smd+" + conId + '+' + json.dumps({"fields": fields})
    return msg

async def sendMessages(msgList):

    messages = msgList 

    async with websockets.connect("wss://" + local_ip + "/v1/api/ws", ssl=ssl_context) as websocket:
        await consumer_handler(websocket)

        consumer_task = asyncio.create_task(consumer_handler(websocket))
        producer_task = asyncio.create_task(producer_handler(websocket))

        await asyncio.gather(consumer_task, producer_task)

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

async def consumer(message):
    print("Consumer hadler: ", message)

async def consumer_handler(websocket):
    async for message in websocket:
        await consumer(message)

async def producer_handler(websocket):
    while True:
        markeDataMsg = subscribeMarketData("265598", "31,83")
        await websocket.send(markeDataMsg)
        await asyncio.sleep(1)

def main():
    msgList = []  
#    timePassed()
    asyncio.get_event_loop().run_until_complete(sendMessages(""))

if __name__ == "__main__":
    main()
