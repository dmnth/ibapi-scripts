#! /usr/bin/env python3


import asyncio
import ssl
import json
import requests
import websockets

#ssl_context = ssl._create_unverified_context()
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)

"smh+265598+{'exchange': 'ISLAND', 'period': '2h', 'bar': '5 min'"

local_ip = "127.0.0.1:5000"
base_url = f"https://{local_ip}/v1/api"

def authorize():
    resp = requests.get(base_url + "/iserver/auth/status", verify=False)
    print(resp.text)


def get_accounts_id():
    rsp = requests.get(base_url + '/portfolio/accounts', verify=False)
    content = json.loads(rsp.content)
    id_list = []
    for id in range(len(content)):
        account_id = content[id]['id']
        id_list.append(account_id)
    return id_list

def create_SMD_req(conId, args):
    msg = "smd+" + conId + '+' + json.dumps({'fields': args})
    return [msg]

def create_SBD_req(conId, exchange):
    account_list = get_accounts_id()
    msg = f"sbd+{account_list[0]}+{conId}+{exchange}"
    return msg

def create_MDD_req(conID, exchange):
    accID_list = get_accounts_id()
    req_list = []
    for accID in accID_list:
        req = f'sbd+{accID}+{conID}+{exchange}'
        req_list.append(req)
    return req_list

async def market_data_requests(mdd_requests):
    async with websockets.connect("wss://" + local_ip + "/v1/api/ws", ssl=ssl_context) as websocket:
        res = await websocket.recv()
        print(res)
        while True:
            for el in mdd_requests:
                await asyncio.sleep(1)
                await websocket.send(mdd_requests)
                res = await websocket.recv()
                result_dict = json.loads(res.decode())

def streaming_data_operations():
   # mdd_requests = create_MDD_req(265598, "ARCA")
   # payload = json.dumps({'sssion': 'fa75c071746dbfbda1e9fbdca7f03fab'})
    smd_req = create_SMD_req('265598', ['31', '83', '84', '85', '86'])
    sbd_req1 = create_SBD_req("265598", "SMART")
    sbd_req2 = create_SBD_req("3691937", "SMART")
#    smd_req = 'smd+265598+{"fields":["31"]}'
#  sbd_req = create_SBD_req(70248730, 'EBS')
    asyncio.get_event_loop().run_until_complete(market_data_requests([sbd_req1, sbd_req2]))
#    asyncio.get_event_loop().run_until_complete(non_async_function([sbd_req1, sbd_req2]))


if __name__ == "__main__":
    authorize()
    streaming_data_operations()

