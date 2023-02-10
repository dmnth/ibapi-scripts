#! /usr/bin/env python3

import logging
import datetime
from threading import Timer
import ibapi
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.order import Order
from ibapi.contract import Contract
from custom_contracts import contracts
from datetime import datetime

class TestApp(EWrapper, EClient):

    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, self)
        self.birla_lines = 0
        self.abcap_lines = 0

    # WRAPPERS HERE

    def error(self, reqId: int, errorCode: int, errorString: str,
            advansedOrderreject):
        super().error(reqId, errorCode, errorString, advansedOrderreject)
        error_message = f'Error id: {reqId}, Error code: {errorCode}, ' \
                        + f'Msg: {errorString}'

    # Provides next valid identifier needed to place an order
    # Indicates that the connection has been established and other messages can be sent from
    # API to TWS
    def nextValidId(self, orderId):
        #super().nextValidId(orderId)
        logging.debug(f"Next valid ID is set to {orderId}")
        self.nextValidOrderId = orderId
        self.start()
        print(f"Next valid order ID: {orderId}")

    def historicalData(self, reqId: int, bar):
        super().historicalData(reqId, bar)
        print("Historical data for: ", reqId, bar)
        if reqId == 1:
            self.birla_lines += 1
        if reqId == 2:
            self.abcap_lines += 1
    
    def historicalDataUpdate(self, reqId, bar):
        super().historicalDataUpdate(reqId, bar)
        print("Historical data for: ", reqId, bar)

    def historicalDataEnd(self, reqId, start, end):
        super().historicalDataEnd(reqId, start, end)
        print("Historical data end for ", reqId, f"from {start} to {end}")
        print("lines returned: ")
        if reqId == 1:
            print(self.birla_lines)
        if reqId == 2:
            print(self.abcap_lines)

    def start(self):
        print(self.serverVersion())
        now = datetime.now().strftime("") 
        birla_contract = contracts[0]
        abc_contract = contracts[1]
        query_time = "20201204 15:00:00"
        order_id = self.nextValidOrderId
        self.reqMarketDataType(4)
        self.reqHistoricalData(1, birla_contract, query_time, '3 M',
                '30 mins', "TRADES", useRTH=1, formatDate=1, keepUpToDate=False, 
                chartOptions=[])
        self.reqHistoricalData(2, abc_contract, query_time, '3 M',
                '30 mins', "TRADES", useRTH=1, formatDate=1, keepUpToDate=False, 
                chartOptions=[])

    def stop(self):
        self.done = True
        self.disconnect()

def main():
    try:
        app = TestApp()
        app.connect('192.168.1.167', 7496, clientId=0)
        print(f'{app.serverVersion()} --- {app.twsConnectionTime().decode()}')
        print(f'ibapi version: ', ibapi.__version__)
        app.run()
    except Exception as err:
        print(err)

if __name__ == '__main__':
    main()
