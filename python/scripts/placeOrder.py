#! /usr/bin/env python3

import ibapi
import logging
import time
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.order import Order
from ibapi.contract import Contract
from ibapi.utils import decimalMaxString, floatMaxString, intMaxString, Decimal
from contracts import CustomContracts




class TestApp(EWrapper, EClient):

    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, self)

    # WRAPPERS HERE

#    def error(self, reqId: int, errorCode: int, errorString: str,
#            advansedOrderreject=""):
#        super().error(reqId, errorCode, errorString, advansedOrderreject)
#        error_message = f'Error id: {reqId}, Error code: {errorCode}, ' \
#                        + f'Msg: {errorString}'

    def nextValidId(self, orderId):
        #super().nextValidId(orderId)
        logging.debug(f"Next valid ID is set to {orderId}")
        self.nextValidOrderId = orderId
        self.start()
        print(f"Next valid order ID: {orderId}")

    def contractDetails(self, reqId, contractDetails):
        super().contractDetails(reqId, contractDetails)
        print("contract details: ", reqId, contractDetails)

    def openOrder(self, orderId, contract, order: Order,
                  orderState):
        super().openOrder(orderId, contract, order, orderState)
        print("openorder OrderId: ", orderId)

    def orderStatus(self, orderId, status: str, filled: Decimal,
                    remaining: Decimal, avgFillPrice: float, permId: int,
                    parentId: int, lastFillPrice: float, clientId: int,
                    whyHeld: str, mktCapPrice: float):
        super().orderStatus(orderId, status, filled, remaining,
                            avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice)
        print(status)
        print("orderstatus OrderId: ", orderId)
        if status == "Filled":
            print(orderId, filled)

        if status == "Cancelled":
            print(orderId, remaining, filled)

    def openOrderEnd(self):
        super().openOrderEnd()
        print("OpenOrderEnd")

    def start(self):
        contracts = CustomContracts()
        contract = contracts.aaplContract()
        
        self.reqContractDetails(self.nextValidOrderId, contract)
        order = Order()

        order.transmit = True 
        order.action = "BUY"
        order.orderType = "MKT"
        order.auxPrice = 120
        order.totalQuantity = 1
        order.outsideRth = False 

        orderId = self.nextValidOrderId
        self.reqOpenOrders()
        self.reqAutoOpenOrders(True)
        for i in range(3):
            self.placeOrder(orderId, contract, order)
            orderId += 1

    def stop(self):
        self.done = True
        self.disconnect()

def main():
    try:
        app = TestApp()
        app.connect('192.168.43.222', 7496, clientId=2)
        print(f'{app.serverVersion()} --- {app.twsConnectionTime().decode()}')
        print(f'ibapi version: ', ibapi.__version__)
#        Timer(15, app.stop).start()
        app.run()
    except Exception as err:
        print(err)

if __name__ == '__main__':
    main()
