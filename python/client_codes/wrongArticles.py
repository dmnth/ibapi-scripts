#! /usr/bin/env python3


import ibapi
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.contract import (Contract, ContractDetails)
import re

class TestApp(EWrapper, EClient):

    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, self)
        self.dataframe = {}
        self.symbols = []
        self.conids = []

    # WRAPPERS HERE
    def nextValidId(self, orderId):
        super().nextValidId(orderId)
        #logging.debug(f"Next valid ID is set to {orderId}")
        self.nextValidOrderId = orderId
        # As soon as next valid id is received it is safe to send requests
        self.start()

    def historicalNews(self, requestId:int, time:str, providerCode:str, articleId:str, headline:str):
        # Matches if preceeded by }
        pattern = re.compile("(?<=})[A-Za-z0-9]+")
        iline = headline
        result = pattern.findall(iline)
        name = result[0]
        print(f"Historical news for {name}")
#        print(requestId, time, providerCode, articleId, headline)

    def contractDetails(self, reqId: int, contractDetails: ContractDetails):
        super().contractDetails(reqId, contractDetails)
        self.contract = contractDetails.contract # store contract in the TestApp instance
        conid = contractDetails.contract.conId
        print("Appending conid")
        self.conids.append(conid)
        self.reqHistoricalNews(reqId, contractDetails.contract.conId , "BRFG", "", "", 300, [])

    # Place requests here
    def start(self):
        self.reqCurrentTime()
        symbol_list = ["NKE", "ACN", "LULU"]
        self.symbols = symbol_list
        news_articles = []
        # Request Historical News
        print("STATE<EMT")
        for symbol in symbol_list:
            contract = Contract()
            contract.symbol = symbol
            contract.secType = "STK"
            contract.exchange = "SMART"
            contract.currency = "USD"
            # Score News Articles
            self.reqContractDetails(self.nextValidOrderId, contract)
        print("STATE<EMT 2")
        print(self.conids)
        contract = Contract()
        contract.symbol = "AAPL" 
        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.currency = "USD"
        # Score News Articles
        self.reqContractDetails(self.nextValidOrderId, contract)

    def stop(self):
        self.done = True
        self.disconnect()

def main():
    try:
        app = TestApp()
        app.connect('192.168.1.167', 7496, clientId=0)
        app.run()
    except Exception as err:
        print(err)

if __name__ == '__main__':
    main()
