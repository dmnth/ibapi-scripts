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

        consumer_task = asyncio.create_task(consumer_handler(websocket))
        producer_task = asyncio.create_task(producer_handler(websocket))

        await asyncio.gather(consumer_task, producer_task)


async def consumer(message):
    print("Consumer hadler: ", message)

async def consumer_handler(websocket):
    async for message in websocket:
        await consumer(message)

async def producer_handler(websocket):
    while True:
        print("Triggered")
        msg = await produce_message()
        if len(msg) > 0:
            msg = msg.pop(0)
        await websocket.send(msg)
        await asyncio.sleep(1)
messages = [subscribeMarketData("265598", "31,83")]
async def produce_message():
    if len(messages) != 0:
        message = messages.pop(0)
        return message

def main():
    msgList = []  
#    timePassed()
#    asyncio.get_event_loop().run_until_complete(sendMessages(""))
    asyncio.run(sendMessages(msgList))

if __name__ == "__main__":
    main()
