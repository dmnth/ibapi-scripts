#! /usr/bin/env python3

from restRequests import *
from restRequests import stocksBySymbol

def testConnection():
    conn = checkAuthStatus()
    assert conn['connected'] == True 

def testAuthenticated():
    conn = checkAuthStatus()
    assert conn['authenticated'] == True

def testOrderPlacement():
    accountID = getAccounts()[0]
    symbol = "BMW"
    contractId = stocksBySymbol(symbol)[symbol][0]['contracts'][0]['conid']
    payload = createMarketOrderPayload(accId=accountID, conId=contractId, exchange="SMART",
            orth=False, action="BUY", symbol=symbol, quantity=1, tif="DAY")
    response = placeOrder(accountID, payload)
    assert 'order_status' in response[0].keys()
