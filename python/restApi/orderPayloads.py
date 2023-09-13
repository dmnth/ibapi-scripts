#! /usr/bin/env python3

class Samples():

    def __init__(self):
        self.property = None

    def samplePayloadUno(acctId):

        payload = {
                "acctId": acctId,
                "conid": 477963416,
                "orderType": "TRAIL",
                "listingExchange": "SEHK",
                "side": "SELL",
                "price": 110.3,
                "trailingAmt": 0.5,
                "trailingType": "%",
                "ticker": "9626",
                "tif": "DAY",
                "quantity": 200,
                "outsideRTH": True 
                }

        return payload

    def mktOrderPayload(acctId):

        payload = {
                "acctId": acctId,
                "conid": 477963416,
                "orderType": "MKT",
                "listingExchange": "SMART",
                "side": "BUY",
                "ticker": "9626",
                "tif": "GTC",
                "quantity": 200,
                "outsideRTH": True 
                }

        return payload

    def applMktOrder(acctId):

        payload = {
                "acctId": acctId,
                "conid": 265598,
                "orderType": "LMT",
                "price": 110,
                "listingExchange": "SMART",
                "side": "BUY",
                "ticker": "AAPL",
                "tif": "GTC",
                "quantity": 200,
                "outsideRTH": True 
                }

        return payload

