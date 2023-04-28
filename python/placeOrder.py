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

    def nextValidId(self, orderId):
        #super().nextValidId(orderId)
        logging.debug(f"Next valid ID is set to {orderId}")
        self.nextValidOrderId = orderId
        self.start()
        print(f"Next valid order ID: {orderId}")
    def openOrder(self, orderId, contract, order: Order,
                  orderState):
        super().openOrder(orderId, contract, order, orderState)
        print("OpenOrder. PermId:", intMaxString(order.permId), "ClientId:", intMaxString(order.clientId), " OrderId:", intMaxString(orderId), 
              "Account:", order.account, "Symbol:", contract.symbol, "SecType:", contract.secType,
              "Exchange:", contract.exchange, "Action:", order.action, "OrderType:", order.orderType,
              "TotalQty:", decimalMaxString(order.totalQuantity), "CashQty:", floatMaxString(order.cashQty), 
              "LmtPrice:", floatMaxString(order.lmtPrice), "AuxPrice:", floatMaxString(order.auxPrice), "Status:", orderState.status,
              "MinTradeQty:", intMaxString(order.minTradeQty), "MinCompeteSize:", intMaxString(order.minCompeteSize),
              "competeAgainstBestOffset:", floatMaxString(order.competeAgainstBestOffset),
              "MidOffsetAtWhole:", floatMaxString(order.midOffsetAtWhole),"MidOffsetAtHalf:" ,floatMaxString(order.midOffsetAtHalf))

    def orderStatus(self, orderId, status: str, filled: Decimal,
                    remaining: Decimal, avgFillPrice: float, permId: int,
                    parentId: int, lastFillPrice: float, clientId: int,
                    whyHeld: str, mktCapPrice: float):
        super().orderStatus(orderId, status, filled, remaining,
                            avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice)
        print("OrderStatus. Id:", orderId, "Status:", status, "Filled:", decimalMaxString(filled),
              "Remaining:", decimalMaxString(remaining), "AvgFillPrice:", floatMaxString(avgFillPrice),
              "PermId:", intMaxString(permId), "ParentId:", intMaxString(parentId), "LastFillPrice:",
              floatMaxString(lastFillPrice), "ClientId:", intMaxString(clientId), "WhyHeld:",
              whyHeld, "MktCapPrice:", floatMaxString(mktCapPrice))

    def openOrderEnd(self):
        super().openOrderEnd()
        print("OpenOrderEnd")

    def start(self):

        
        self.reqAllOpenOrders()

        contract = bmwContract()
        order = sellLimitOrder()

        self.reqContractDetails(self.nextValidOrderId, contract)

        order.transmit = False
        self.placeOrder(self.nextValidOrderId, contract, order)

        time.sleep(4)

        order.transmit = True
        self.placeOrder(self.nextValidOrderId + 1, contract, order)


    def stop(self):
        self.done = True
        self.disconnect()

def main():
    try:
        app = TestApp()
        app.connect('192.168.1.167', 7496, clientId=0)
        print(f'{app.serverVersion()} --- {app.twsConnectionTime().decode()}')
        print(f'ibapi version: ', ibapi.__version__)
#        Timer(15, app.stop).start()
        app.run()
    except Exception as err:
        print(err)

if __name__ == '__main__':
    main()
