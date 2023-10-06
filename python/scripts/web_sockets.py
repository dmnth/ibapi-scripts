#! /usr/bin/env python3


import asyncio
import ssl
import json
import requests
import websockets

ssl_context = ssl._create_unverified_context()

# session = json.dumps({"session": sid})
# Check if CORS are enabled in http headers

"smh+265598+{'exchange': 'ISLAND', 'period': '2h', 'bar': '5 min'"

local_ip = "127.0.0.1:5000"
base_url = f"https://{local_ip}/v1/api"

def get_sid():
    resp = requests.get(base_url + "/tickle", verify=False)
    if resp:
        resp_content = resp.content.decode()
        res = json.loads(resp_content)
        print(res['session'])
        session_id = resp_content.split(':')[1].split(',')[0].strip('"')

        session = json.dumps({'session': res['session']})
        data = "smd+265598+" + json.dumps({'fields':['31', '83']})
        message_dict = {
            'trades': 'str+{}',
            'example': data
        }
    return session_id
# acctId = get_account_id()
# subscribe_mkt_dpth = f"sbd+{acctid}+{conId}+{exchange}"

def authorize():
    resp = requests.get(base_url + "/iserver/auth/status", verify=False)
    print(resp.text)

def get_snapshot_data():
    params = {'conids': ['170547560'], 'since': 0, 'fields': ['31', '70', '71', ]}
    print(params)
    resp = requests.get("https://localhost:5000/v1/api/iserver/marketdata/snapshot", verify=False,
                        params=params)
    print(resp.url)

    print(resp.text)

def whatif():
    headers = {"Content-Type": "application/json"}
    url = \
    "https://"+ local_ip +"/v1/api/iserver/account/DU6036902/orders/whatif"
    params = { "orders": [
        {
        "acctId": "DU6036902",
        "conid": 265598,
        "secType": "secType = 265598:STK",
        "orderType": "LMT",
        "listingExchange": "SMART",
        "outsideRTH": True,
        "price": 1,
        "auxPrice": 0,
        "side": "BUY",
        "ticker": "AAPL",
        "tif": "DAY",
        "quantity": 12
        }
        ]
    }
    json_params = json.dumps(params)
    print("Json params: ", json_params)
    resp = requests.post(url, verify=False, data=json_params, headers=headers)
    print("Whatif response: ", resp.text)

def place_simple_order():
    headers = {"Content-Type": "application/json"}
    url = 'https://192.168.1.167:4001'
    endpoint = '/v1/api/iserver/account/DU6036902/orders'
    params = { "orders": [
        {
        "acctId": "DU6036902",
        "conid": 265598,
        "secType": "secType = 265598:STK",
        "orderType": "LMT",
        "listingExchange": "SMART",
        "outsideRTH": True,
        "price": 1,
        "auxPrice": 0,
        "side": "BUY",
        "ticker": "AAPL",
        "tif": "DAY",
        "quantity": 12
        }
        ]
    }
    json_params = json.dumps(params)
    print(json_params)
    resp = requests.post(url + endpoint, verify=False, data=json_params,
            headers=headers)
    print("this: ", resp.text)

def get_accounts_id():
    rsp = requests.get(base_url + '/portfolio/accounts', verify=False)
    content = json.loads(rsp.content)
    id_list = []
    for id in range(len(content)):
        account_id = content[id]['id']
        id_list.append(account_id)
    return id_list

def reauthenticate_session():
    rsp = requests.get(base_url + '/iserver/reauthenticate', verify=False)
    if rsp.status_code != 200:
        print(rsp.status_code, "-> Wonder if something is wrong")
    else:
        return rsp.content

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

def get_subAccounts_list():
    # Should be called before any other account operations
    rsp = requests.get('https://localhost:5000/v1/api/portfolio/accounts')

async def non_async_function(mdd_requests):
    async  with websockets.connect("wss://127.0.0.1:5000/v1/api/ws", ssl=ssl_context) as socket:
        await socket.send('{session: "0845803408530485038"}')
        res = await socket.recv()
        print(res)
        while True:
            for message in mdd_requests:
                print(message)
                await asyncio.sleep(1)
                await socket.send(message)
                result_dict = json.loads(res.decode())
                print(result_dict)

async def market_data_requests(mdd_requests):
    async with websockets.connect("wss://" + local_ip + "/v1/api/ws", ssl=ssl_context) as websocket:
        await websocket.send('{session: "0845803408530485038"}')
        res = await websocket.recv()
        print(res)
        while True:
            for el in mdd_requests:
                await asyncio.sleep(1)
                await websocket.send(mdd_requests)
                res = await websocket.recv()
                result_dict = json.loads(res.decode())
                if 'error' in result_dict.keys():

                    if result_dict['error'] == 'not authenticated':
                        print("PLEASE REAUTHENTICATE BLYAT")
                        msg = reauthenticate_session().decode()
                        if len(msg) != 0 and msg['message'] == 'triggered':
                            print("Reauthenticated succesfully")
                        else:
                            print("Reauth did not succeed")
                else:
                    if 'data' in result_dict.keys():
                        print("----> ", result_dict['data'][0])

async def send_session_id(payload):
    async with websockets.connect("wss://" + local_ip + "/v1/api/ws", ssl=ssl_context) as websocket:
        res = await websocket.recv()
        if res:
            print("result: ", res)
        asyncio.sleep(2)
        print(payload)
        await websocket.send(payload)
        res = await websocket.recv()
        print('decoded response: ', res.decode())
        result_dict = json.loads(res.decode())
        print('dict json: ', result_dict)
        if len(res) != 0 and 'data' in result_dict.keys():
            for el in result_dict['data']:
                print(el)
                if 'ask' in el.keys() or 'bid' in el.keys():
                    print(el)
                    return

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
    whatif()
    place_simple_order()
    streaming_data_operations()

