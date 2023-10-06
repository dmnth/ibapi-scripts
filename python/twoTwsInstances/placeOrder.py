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
from threading import Timer


def aaplContractPearl():

    contract = Contract()

    contract.symbol = "AAPL"
    contract.exchange = "SMART"
    contract.currency = "USD" 
    contract.secType = "STK"

    return contract


def bmwContract():

    
    contract = Contract()
    contract.symbol = "BMW"
    contract.secType = "STK"
    contract.currency = "EUR"
    contract.exchange = "SMART"
    contract.primaryExchange = "IBIS"

    return contract

def conidContract():

    contract = Contract()

    contract.conId = 549590944 
    contract.exchange = "COMEX"
    contract.currency = "USD"
    contract.secType = "FOP"
    contract.symbol = "GC"

    return contract

def qqqContract():

    contract = Contract()
    contract.symbol = "QQQ"
    contract.exchange = "SMART"
    contract.primaryExchange = "NASDAQ"
    contract.currency = "USD"
    contract.tradingClass = "NMS"
    contract.localSymbol = "QQQ"
    contract.secType = "STK"

    return contract

def goodAfterTimeOrder():

    order = Order()
    order.action = "BUY" 
    order.orderType = "MKT"
    order.totalQuantity = 1 
    order.goodAfterTime = "20230501 14:00:00 Europe/Moscow"

    return order

def sellLimitOrder():

    order = Order()
    order.action = "SELL"
    order.orderType = "LMT"
    order.lmtPrice = "105.5"
    order.tif = "DAY"
    order.totalQuantity = 1
    order.transmit = True 

    return order

def aaplContract():

    contract = Contract()
    contract.symbol = "AAPL"
    contract.exchange = "SMART"
    contract.currency = "USD"
    contract.secType = "STK"

    return contract

def alkemContract():

    contract = Contract()

    contract.conId = 628565593
    contract.symbol = "ALKEM"
    contract.lastTradeDateOrContractMonth = "20230727"
    contract.multiplier = '1'
    contract.exchange = "NSE"
    contract.currency = "INR"
    contract.localSymbol = "ALKEM23JULFUT"

    return contract


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

    def orderStatus(self, orderId, status: str, filled: Decimal,
                    remaining: Decimal, avgFillPrice: float, permId: int,
                    parentId: int, lastFillPrice: float, clientId: int,
                    whyHeld: str, mktCapPrice: float):
        super().orderStatus(orderId, status, filled, remaining,
                            avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice)
        print(status)
        if status == "Filled":
            print(orderId, filled)

        if status == "Cancelled":
            print(orderId, remaining, filled)

    def openOrderEnd(self):
        super().openOrderEnd()
        print("OpenOrderEnd")

    def start(self):
        contracts = CustomContracts()
        contract = contracts.aaplOptions()

        contract = aaplContract()

        order = Order()

        order.transmit = True 
        order.action = "BUY"
        order.orderType = "MKT"
        order.auxPrice = 120
        order.totalQuantity = 1
        order.outsideRth = False 

        orderId = self.nextValidOrderId
        self.reqOpenOrders()
        for i in range(10):
            self.placeOrder(orderId, contract, order)
            orderId += 1

    def stop(self):
        self.done = True
        self.disconnect()

def main():
    try:
        app = TestApp()
        app1 = TestApp()
        app.connect('192.168.43.222', 7496, clientId=0)
        app1.connect('192.168.43.222', 7490, clientId=1)
        print(f'{app.serverVersion()} --- {app.twsConnectionTime().decode()}')
        print(f'ibapi version: ', ibapi.__version__)
        Timer(5, app.stop).start()
        Timer(10, app1.stop).start()
        app.run()
        app1.run()
    except Exception as err:
        print(err)

if __name__ == '__main__':
    main()
