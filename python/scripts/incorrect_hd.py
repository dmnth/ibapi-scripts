#! /usr/bin/env python3

import logging
import datetime
from threading import Timer
import ibapi
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.order import Order
from ibapi.contract import Contract
from custom_contracts import TestContracts

class TestApp(EWrapper, EClient):

    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, self)

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

    def historicalData(self, reqId, bar):
        if bar.date == "20230112 13:00:00 US/Central":
            print(bar.date, bar.close)
        if bar.date == "20230112 13:00:00 MET":
            print(bar.date, bar.close)
        if bar.date == "20230112 13:00:00 US/Eastern":
            print(bar.date, bar.close)

    def headTimestamp(self, reqId, headTimeStamp):
        print("HeadTimeStamp: ", headTimeStamp)


    def compareDates(self, dateString1, dateString2):
        return


    def start(self):
        print(self.serverVersion())
        contract = TestContracts.create_futures_contracts() 
#        contract = TestContracts.porsche_contract()
#        contract = TestContracts.create_single_US_contract("AAPL")
#        self.reqHeadTimeStamp(self.nextValidOrderId, contract, "TRADES", 0, 1)
        end_date = "20230113 13:00:00 US/Eastern"
        self.reqMarketDataType(1)
        self.reqHistoricalData(self.nextValidOrderId, contract[0], end_date, "1 M",
                "1 hour", "MIDPOINT", 1, 1, False, [])
#        self.nextValidOrderId += 1
#         self.reqHistoricalData(self.nextValidOrderId, contract, "", "1 W",
#                "1 hour", "TRADES", 1, 1, False, [])

    def stop(self):
        self.done = True
        self.disconnect()

def main():
    try:
        app = TestApp()
        app.connect('192.168.1.127', 7496, clientId=0)
        print(f'{app.serverVersion()} --- {app.twsConnectionTime().decode()}')
        print(f'ibapi version: ', ibapi.__version__)
        Timer(15, app.stop).start()
        app.run()
    except Exception as err:
        print(err)

if __name__ == '__main__':
    main()
