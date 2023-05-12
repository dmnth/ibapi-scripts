#! /usr/bin/env python3

import ibapi
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.contract import (Contract, ContractDetails)

class TestApp(EWrapper, EClient):

    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, self)
        self.dataframe = {}
        self.contract = None

    # WRAPPERS HERE
    def nextValidId(self, orderId):
        super().nextValidId(orderId)
        #logging.debug(f"Next valid ID is set to {orderId}")
        self.nextValidOrderId = orderId
        # As soon as next valid id is received it is safe to send requests
        self.start()

    def historicalNews(self, requestId:int, time:str, providerCode:str, articleId:str, headline:str):
        symbol = self.contract.symbol
        print(requestId, time, providerCode, articleId, headline)

    def contractDetails(self, reqId: int, contractDetails: ContractDetails):
        super().contractDetails(reqId, contractDetails)
        self.contract = contractDetails.contract # store contract in the TestApp instance
        symbol = contractDetails.contract.symbol
        self.reqHistoricalNews(reqId, contractDetails.contract.conId , "BRFG", "", "", 300, [])

    def historicalTicksBidAsk(self, reqId: int, ticks,
                              done: bool):
        for tick in ticks:
            self.convert_unix_timestamp(tick.time)
            print("HistoricalTickBidAsk. ReqId:", reqId, tick)

    def historicalTicksLast(self, reqId: int, ticks,
                            done: bool):
        for tick in ticks:
            self.convert_unix_timestamp(tick.time)
            print("HistoricalTickLast. ReqId:", reqId, tick)

    def historicalDataEnd(self, reqId, start, end):
        super().historicalDataEnd(reqId, start, end)
        print("Historical data end for: ", self.clientId)

    # Place requests here
    def start(self):

        contract = Contract()
        contract.symbol = 'AAPL'
        contract.exchange = 'SMART'
        contract.currency = 'USD'
        contract.secType = "STK"
        
        startDate = "20230308 10:30:00 US/Eastern"
        self.reqHistoricalTicks(self.nextValidOrderId, contract, startDate, "",
                10, "TRADES", 1, True, [])

    def stop(self):
        self.done = True
        self.disconnect()

def main():
    try:
        app = TestApp()
        app.connect('192.168.43.222', 7496, clientId=0)
        app.run()
    except Exception as err:
        print(err)

if __name__ == '__main__':
    main()
