#! /usr/bin/env python3

import requests
import ssl
import queue
import urllib3
import websocket
import json
import time

localIP = "127.0.0.1"
BASE_URL = f"{localIP}:5000/v1/api"


class WebsocketClient(websocket.WebSocket):
    def __init__(self, websocket_url: str):
        self.websocket_url = websocket_url
        self.subscriptions = []

    def connect(self, session_id: str, ssl_options: dict = None):
        self.ws = websocket.create_connection(self.websocket_url, sslopt=ssl_options)
#        self.ws.send(f'{{"session": "{session_id}"}}')
        return self
    
    def recv(self):
        return self.ws.recv()

    def send(self, message: str):
        return self.ws.send(message)


def request_session_id() -> str:
    request_endpoint = "/tickle"
    request_url = f"https://{BASE_URL}{request_endpoint}"
    print(request_url)
    response = requests.post(request_url, verify=False)
    print(response.text)
    if not response.ok:
        raise RuntimeError("Failed to request session ID")
    session_id = response.json()["session"]
    return session_id

def getAccountId():
    resp = requests.get("https://" + BASE_URL + "/iserver/accounts", verify=False) 
    jsonData = json.loads(resp.text)
    accounts = jsonData['accounts']
    if len(accounts) > 0:
        return accounts

def getContractDetails(conId):
    endpoint = f"/iserver/contract/{conId}/info"
    data = {"conid": conId}
    resp = requests.get("https://" + BASE_URL + endpoint, verify=False, params=data)
    jsonData = json.loads(resp.text)
    if resp.status_code == 200:
        return jsonData
    else:
        raise RuntimeError(f"No contracts found for {conId}")

def get_websocket_client(session_id: str) -> WebsocketClient:
    websocket_endpoint = "/ws"
    websocket_url = f"wss://{BASE_URL}{websocket_endpoint}"
    websocket = WebsocketClient(websocket_url).connect(
        session_id, {"cert_reqs": ssl.CERT_NONE}
    )
    return websocket

def marketDataReq(conId, args: str):
    args = args.split(',')
#    msg = "smd+" + conId + '+' + '{"fields":["31","83"]}'
    msg = "smd+" + conId + '+' + json.dumps({"fields":args})
    return msg

def historicalDataRequest(conID, period, barSize, dataType, dateFormat):
    msg = f"smh+{conID}+" + json.dumps({
        "period": period,
        "bar": barSize,
        "source": dataType,
        "format": dateFormat 
        }) 
    return msg

def unsubscibeHistoricalData(serverID):
    msg = "umh+" + serverID 
    return msg

def marketDepthRequest(conID, acctID=None, exchange=None):

    if acctID is None:
        acctIDs = getAccountId()
        acctID = acctIDs[0]

    if exchange is None:
        details = getContractDetails(conID)
        exchange = details['exchange']

    msg = f"sbd+{acctID}+{conID}+{exchange}"
    unsubMsg = f"ubd+{acctID}"

    msgPair = {
            "subscribe": msg,
            "unsubscribe": unsubMsg
            }

    return msgPair 

def processMsg(websocket, msg, mktDpthResponse=None):

    if "topic" not in msg.keys():
        print(msg)

    # Unsubscibe from historical data in order not to plot charts
    if msg['topic'].startswith('smh+'):
        serverID = msg['serverId']
        unsubMsg = unsubscibeHistoricalData(serverID)
        websocket.send(unsubMsg)
        res = websocket.recv()
        print("Unsubscribed from historical data")
    
    # Unsubscibe from market depth
    if msg['topic'] == 'sbd':
        print(msg)
        websocket.send(mktDpthResponse)
        res = websocket.recv()
        print("Unsubscribed from market depth")

# One request at a time can be processed because websockets are meant to be async
def main():
    session_id = request_session_id()
    session_id = 0
    websocket = get_websocket_client(session_id)
    histReq = historicalDataRequest("265598", "1d", "1hour", "trades", "%o/%c/%h/%l") 
    mktDpthMsg = marketDepthRequest("265598")
    messages = [
            mktDpthMsg['subscribe'],
            histReq,
    ]
    messages = []
    message_queue = queue.Queue()
    for message in messages:
        message_queue.put(message)
    try:
        while True:
            if not message_queue.empty():
                message = message_queue.get()

                if message.startswith("smd+"):
                    print("Sending market data request")

                if message.startswith("smh+"):
                    print("Sending historical data request")

                if message.startswith("sor"):
                    print("Subscribed to open orders")

                if message.startswith("sbd+"):
                    print("Sending market depth requests")

                websocket.send(message)
            websocket_message = websocket.recv()
            msg = json.loads(websocket_message.decode())
            # Implement message handling here, for example add unsubscribe logic
            time.sleep(2)
            processMsg(websocket, msg, mktDpthMsg['unsubscribe'])
            prettyMsg = json.dumps(msg, indent=4)
#            print(prettyMsg)

    except KeyboardInterrupt:
        raise SystemExit


if __name__ == "__main__":
    urllib3.disable_warnings()
    main()

