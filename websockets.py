#! /usr/bin/env python3


import websockets
import asyncio
import ssl
import json
import requests

ssl_context = ssl._create_unverified_context()

session = json.dumps({"session": "0e7b15af81d6bc0345d79bcc8212bd26"})

"smh+265598+{'exchange': 'ISLAND', 'period': '2h', 'bar': '5 min'"

resp = requests.get("https://localhost:5000/v1/api/tickle", verify=False)
if resp:
    resp_content = resp.content.decode()
    res = json.loads(resp_content)
    print(res['session'])
    session_id = resp_content.split(':')[1].split(',')[0].strip('"')
    print(session)

    session = json.dumps({'session': res['session']})
    data = "smd+265598+" + json.dumps({'fields':['31', '83']})
    message_dict = {
        'trades': 'str+{}',
        'example': data
    }
# acctId = get_account_id()
# subscribe_mkt_dpth = f"sbd+{acctid}+{conId}+{exchange}"

def authorize():
    resp = requests.get("https://localhost:5000/v1/api/iserver/auth/status", verify=False)
    print(resp.text)

def get_snapshot_data():
    params = {'conids': ['170547560'], 'since': 0, 'fields': ['31', '70', '71', ]}
    print(params)
    resp = requests.get("https://localhost:5000/v1/api/iserver/marketdata/snapshot", verify=False,
                        params=params)
    print(resp.url)

    print(resp.text)

def place_simple_order():
    url = 'https://localhost:5000'
    endpoint = '/v1/api/iserver/account/DU6036902/orders'
    params = { 'orders': [
        {
        'acctId': 'DU6036902',
        'conid': 265598,
        'secType': 'secType = 265598:STK',
        'orderType': 'LMT',
        'listingExchange': 'SMART',
        'outsideRTH': True,
        'price': 1,
        'auxPrice': 0,
        'side': 'BUY',
        'ticker': 'AAPL',
        'tif': 'DAY',
        'quantity': 12
        }
        ]
    }
    str_params = "{ 'orders': [{'acctId': 'DU6036902', 'conid': 265598, 'secType': 'secType = 265598:STK', " \
             "'orderType': 'LMT', 'listingExchange': 'SMART', 'outsideRTH': True, 'price': 1, " \
             "'auxPrice': 0, 'side': 'BUY', 'ticker': 'AAPL', 'tif': 'DAY', 'quantity': 12}]}"
    json_params = json.dumps(str_params)
    print(json_params)
    payload = {"accountId": "DU6036902", "body": params}
    resp = requests.post(url + endpoint, verify=False, data=json_params)
    print(resp.text)

def get_accounts_id():
    rsp = requests.get('https://localhost:5000/v1/api/portfolio/accounts', verify=False)
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
    return [msg]

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

async def hello(mdd_requests):
    async with websockets.connect("wss://localhost:5000/v1/api/ws", ssl=ssl_context) as websocket:
        res = await websocket.recv()
        if res:
            print("result: ", res)
        while True:
            asyncio.sleep(2)
            for message in mdd_requests:
                print(message)
                await websocket.send(message)
            res = await websocket.recv()
            result_dict = json.loads(res.decode())
            if len(res) != 0 and 'data' in result_dict.keys():
                for el in result_dict['data']:
                    print(el)
                    if 'ask' in el.keys() or 'bid' in el.keys():
                        print(el)
                        return




if __name__ == "__main__":
    mdd_requests = create_MDD_req(265598, "ARCA")
  # smd_req = create_SMD_req('265598', ['31', '83', '84', '85', '86'])
#  sbd_req = create_SBD_req(70248730, 'EBS')
#    asyncio.get_event_loop().run_until_complete(hello(mdd_requests))
    place_simple_order()