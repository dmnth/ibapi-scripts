#! /usr/bin/env python3

import ibapi
import random
import time
from threading import Timer
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.contract import (Contract, ContractDetails)
from ibapi.utils import floatMaxString, decimalMaxString

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

    def tickPrice(self, reqId, tickType, price: float,
                  attrib):
        super().tickPrice(reqId, tickType, price, attrib)
        print("TickPrice. TickerId:", reqId, "tickType:", tickType,
              "Price:", floatMaxString(price), "CanAutoExecute:", attrib.canAutoExecute,
              attrib.preOpen)

    def tickSize(self, reqId, tickType, size):
        super().tickSize(reqId, tickType, size)
        print("TickSize. TickerId:", reqId, "TickType:", tickType, "Size: ", decimalMaxString(size))

    def tickGeneric(self, reqId, tickType, value: float):
        super().tickGeneric(reqId, tickType, value)
        print("TickGeneric. TickerId:", reqId, "TickType:", tickType, "Value:", floatMaxString(value))

    def tickString(self, reqId, tickType, value: str):
        super().tickString(reqId, tickType, value)
        print("TickString. TickerId:", reqId, "Type:", tickType, "Value:", value)

    def start(self):

        contract = Contract()
        contract.symbol = 'AMZN'
        contract.exchange = 'SMART'
        contract.currency = 'USD'
        contract.secType = "STK"

        self.reqMktData(self.nextValidOrderId, contract, '', False, False, [])
        
    def stop(self):
        self.done = True
#        self.cancelMktData(12343)
        print(f"Disconnecting client id {self.clientId}")
        self.disconnect()

def main():
    cid =12345 
    try:
        app = TestApp()
        app.connect('192.168.43.222', 7497, clientId=cid)
        Timer(5, app.stop).start()
        app.run()
    except Exception as err:
        print(err)

if __name__ == '__main__':
    main()
