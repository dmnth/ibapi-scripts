#! /usr/bin/env python3

import logging
import datetime
import threading
from threading import Timer
import ibapi
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.order import Order
from ibapi.contract import Contract
import json
# from parse_json import contract
from bracket_order import bracket_order

class TestApp(EWrapper, EClient):


    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, self)
        self.dataframe = {}

    # WRAPPERS HERE

    def error(self, reqId: int, errorCode: int, errorString: str,
              advansedOrderreject=""):
        super().error(reqId, errorCode, errorString, advansedOrderreject)
        error_message = f'Error id: {reqId}, Error code: {errorCode}, ' \
                        + f'Msg: {errorString}'
        print(error_message)
    #
    # Provides next valid identifier needed to place an order
    # Indicates that the connection has been established and other messages can be sent from
    # API to TWS
    def nextValidId(self, orderId):
        super().nextValidId(orderId)
        logging.debug(f"Next valid ID is set to {orderId}")
        self.nextValidOrderId = orderId # Snippet 1
        self.start()

    def contractDetails(self, reqId: int, contractDetails):
        super().contractDetails(reqId, contractDetails)
        print(contractDetails)

    def historicalData(self, reqId:int, bar):
        print("HistoricalData. ReqId:", reqId, "BarData.", bar)

    def start(self):
        print('@###################################')
        contrac2 = Contract()
        contrac2.symbol = "SPX"
        contrac2.exchange = "SMART"
        contrac2.currency = "USD"
        contrac2.secType = "IDX"

        self.reqContractDetails(self.nextValidOrderId, contrac2)
#        self.reqHistoricalData(self.nextValidOrderId, contrac2, "20230101-23:59:59", "1 D", "1 min", "MIDPOINT", 1, 1, False, [])

    def stop(self):
        self.done = True
        self.disconnect()


def main():
    try:
        app = TestApp()
        app.connect('127.0.0.1', 7496, clientId=0)
        print(f'{app.serverVersion()} --- {app.twsConnectionTime().decode()}')
        print(f'ibapi version: ', ibapi.__version__)
        Timer(5, app.stop).start()
        app.run()
    except Exception as err:
        print(err)

if __name__ == '__main__':
    main()
