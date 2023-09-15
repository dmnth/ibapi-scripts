#! /usr/bin/env python3

import logging
import datetime
from threading import Timer
import ibapiTest
import time
from ibapiTest.wrapper import EWrapper
from ibapiTest.client import EClient
from ibapiTest.order import Order
from ibapiTest.contract import Contract
from ibapiTest.utils import decimalMaxString, floatMaxString, intMaxString, Decimal
from ibapiTest.tag_value import TagValue
from contracts import CustomContracts 
from ibapiTest.execution import ExecutionFilter
from ibapi.contract import ComboLeg

def silverSpread():

    contract = Contract()

    contract.symbol = "SI"
    contract.secType = "BAG"
    contract.currency = "USD"
    contract.exchange = "COMEX"

    leg1 = ComboLeg()
    leg1.conId = 645364413 
    leg1.ratio = 1
    leg1.action = "BUY"
    leg1.exchange = "COMEX"

    leg2 = ComboLeg()
    leg2.conId = 651096968 
    leg2.ratio = 1
    leg2.action = "BUY"
    leg2.exchange = "COMEX"

    contract.comboLegs = []
    contract.comboLegs.append(leg1)
    contract.comboLegs.append(leg2)

    return contract


class PlaceBagOrders(EWrapper, EClient):

    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, self)
        self.executions = []

    # WRAPPERS HERE

    def error(self, reqId: int, errorCode: int, errorString: str,
            advansedOrderreject=""):
        super().error(reqId, errorCode, errorString, advansedOrderreject)
        error_message = f'Error id: {reqId}, Error code: {errorCode}, ' \
                        + f'Msg: {errorString}'

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
        if orderId == None:
            print("OpenOrder. PermId:", intMaxString(order.permId), "ClientId:", intMaxString(order.clientId), " OrderId:", intMaxString(orderId), "Account:", order.account, "Symbol:", contract.symbol, "SecType:", contract.secType,
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
        if orderId == None:
            print("OrderStatus. Id:", orderId, "Status:", status, "Filled:", decimalMaxString(filled),
                  "Remaining:", decimalMaxString(remaining), "AvgFillPrice:", floatMaxString(avgFillPrice),
                  "PermId:", intMaxString(permId), "ParentId:", intMaxString(parentId), "LastFillPrice:",
                  floatMaxString(lastFillPrice), "ClientId:", intMaxString(clientId), "WhyHeld:",
                  whyHeld, "MktCapPrice:", floatMaxString(mktCapPrice))

    def execDetails(self, reqId: int, contract: Contract, execution):
        super().execDetails(reqId, contract, execution)
        print("ExecDetails. ReqId:", reqId, "Symbol:", contract.symbol, "SecType:", contract.secType, "Currency:", contract.currency, execution)

    def execDetailsEnd(self, reqId: int):
        super().execDetailsEnd(reqId)
        print("ExecDetailsEnd. ReqId:", reqId)

    def openOrderEnd(self):
        super().openOrderEnd()
        print("OpenOrderEnd")


    def placeSpread(self):

        silverSpreadContract = silverSpread() 

        order = Order()
        order.orderType = "MKT"
        order.action = 'BUY'
        order.totalQuantity = 1 

        orderId = self.nextValidOrderId 

        self.placeOrder(orderId, silverSpreadContract, order)

    def start(self):

        self.placeSpread()

        time.sleep(5)

        execFilter = ExecutionFilter()
        execFilter.secType = "BAG"
        # Adjust the time if required or comment it out
        execFilter.time = "20230915 11:25:00"
        self.reqExecutions(self.nextValidOrderId, execFilter) 

        

    def stop(self):
        self.done = True
        self.disconnect()

def main():
    try:
        app = PlaceBagOrders()
        app.connect('127.0.0.1', 7496, clientId=0)
        print(f'{app.serverVersion()} --- {app.twsConnectionTime().decode()}')
        print(f'ibapi version: ', ibapiTest.__version__)
#        Timer(15, app.stop).start()
        app.run()
    except Exception as err:
        print(err)

if __name__ == '__main__':
    main()
