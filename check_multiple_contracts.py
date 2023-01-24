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

print(ibapi.__version__)
class TestApp(EWrapper, EClient):

    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, self)
        self.id = {}

    # WRAPPERS HERE

    def error(self, reqId: int, errorCode: int, errorString: str,
            advansedOrderreject=""):
        error_message = f'Error id: {reqId}, Error code: {errorCode}, ' \
                        + f'Msg: {errorString}'
        print(error_message)                        

    # Provides next valid identifier needed to place an order
    # Indicates that the connection has been established and other messages can be sent from
    # API to TWS
    def nextValidId(self, orderId):
        #super().nextValidId(orderId)
        logging.debug(f"Next valid ID is set to {orderId}")
        self.nextValidOrderId = orderId
        self.start()
        print(f"Next valid order ID: {orderId}")

    def tickString(self, reqId, tickType, size):
        super().tickString(reqId, tickType, size)
        print(reqId, tickType, size)

    def contractDetails(self, reqId, contractDetails):
        super().contractDetails(reqId, contractDetails)
        print(contractDetails)

    def historicalData(self, reqId, bar):
        if reqId not in self.id.keys():
            self.id[reqId] = "Present"
        print(self.id)

    def make_multiple_queries(self, list_of_contracts):
        id = self.nextValidOrderId
        for c in list_of_contracts:
            print(c)
            print(id)
            self.reqHistoricalData(id, c, 
                    '', '1 M', '1 hour', "TRADES", 0, 1, False, [])
            id += 1


    def start(self):
        print(self.serverVersion())
        contract = TestContracts.create_futures_contracts() 

        nymex_symbols = ["CL", "NG", "HO"]
        cbot_symbols = ["ZC", "ZW", "ZS", "YM", "ZF"]

        nymex_contracts = TestContracts.create_contract_list(nymex_symbols,
                exchange="NYMEX")
        cbot_contracts = TestContracts.create_contract_list(cbot_symbols,
                exchange="CBOT")

        self.make_multiple_queries(cbot_contracts)

    def stop(self):
        self.done = True
        self.disconnect()

def main():
    try:
        app = TestApp()
        app.connect('192.168.1.127', 7496, clientId=0)
        print(f'{app.serverVersion()} --- {app.twsConnectionTime().decode()}')
        print(f'ibapi version: ', ibapi.__version__)
        print(app.id)
        Timer(15, app.stop).start()
        app.run()
    except Exception as err:
        print(err)

if __name__ == '__main__':
    main()
