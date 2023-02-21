#! /usr/bin/env python3

import logging
import datetime
from threading import Timer
import ibapi
import time
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.order import Order
from ibapi.contract import Contract
from ibapi.utils import decimalMaxString, floatMaxString, intMaxString, Decimal
from accumulate_distribute import pair
from my_contracts import CustomContracts

contracts = CustomContracts()

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

    def updateMktDepth(self, reqId, position: int, operation: int,
                       side: int, price: float, size: Decimal):
        super().updateMktDepth(reqId, position, operation, side, price, size)
        print("UpdateMarketDepth. ReqId:", reqId, "Position:", position, "Operation:",
              operation, "Side:", side, "Price:", floatMaxString(price), "Size:", decimalMaxString(size))
        
    def updateMktDepthL2(self, reqId, position: int, marketMaker: str,
                         operation: int, side: int, price: float, size: Decimal, isSmartDepth: bool):
        super().updateMktDepthL2(reqId, position, marketMaker, operation, side,
                                 price, size, isSmartDepth)
        print("UpdateMarketDepthL2. ReqId:", reqId, "Position:", position, "MarketMaker:", marketMaker, "Operation:",
              operation, "Side:", side, "Price:", floatMaxString(price), "Size:", decimalMaxString(size), "isSmartDepth:", isSmartDepth)


    def start(self):
        contract.symbol = symbol
        self.reqMktDepth(self.nextValidOrderId, contract, 10, True, [])
#        self.reqAllOpenOrders()

    def stop(self):
        self.done = True
        self.disconnect()


app = TestApp()

contract = Contract()
contract.exchange = "SMART"
contract.currency = "USD"
contract.secType = "STK"

symbol = "AAPL"

app.connect('192.168.1.167', 7496, clientId=0)
print(f'{app.serverVersion()} --- {app.twsConnectionTime().decode()}')
print(f'ibapi version: ', ibapi.__version__)
#        Timer(15, app.stop).start()
app.run()

