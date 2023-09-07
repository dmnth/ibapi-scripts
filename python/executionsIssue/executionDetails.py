#! /usr/bin/env python3

import logging
import datetime
from threading import Timer
import ibapiTest
import time
import datetime
from ibapiTest.wrapper import EWrapper
from ibapiTest.client import EClient
from ibapiTest.order import Order
from ibapiTest.contract import Contract
from ibapiTest.utils import decimalMaxString, floatMaxString, intMaxString
from ibapiTest.execution import ExecutionFilter, Execution

class ExecutionsDetails(EWrapper, EClient):

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

    def openOrderEnd(self):
        super().openOrderEnd()
        print("OpenOrderEnd")

    def execDetails(self, reqId: int, contract: Contract, execution: Execution):
        super().execDetails(reqId, contract, execution)
        print("ExecDetails. ReqId:", reqId, "Symbol:", contract.symbol, "SecType:", contract.secType, "Currency:", contract.currency, execution)

    def execDetailsEnd(self, reqId: int):
        super().execDetailsEnd(reqId)
        print("ExecDetailsEnd. ReqId:", reqId)

    def tickPrice(self, reqId, tickType, price: float,
                  attrib):
        super().tickPrice(reqId, tickType, price, attrib)
        print("TickPrice. TickerId:", reqId, "tickType:", tickType)

    def nextValidId(self, orderId):
        #super().nextValidId(orderId)
        logging.debug(f"Next valid ID is set to {orderId}")
        self.nextValidOrderId = orderId
        self.start()
        print(f"Next valid order ID: {orderId}")

    def start(self):
        order = Order()
        order.action = "BUY" 
        order.orderType = "MKT"
        order.totalQuantity = 11 


        contract = Contract()
        contract.symbol = "AAPL"
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "SMART"

#        self.placeOrder(self.nextValidOrderId, contract, order)
#        time.sleep(1#)
        execFilter = ExecutionFilter()
#        execFilter.secType = "BAG"
        execFilter.time = "20230701-02:30:00" 
        execFilter.secType = "FUT"
##        self.placeOrder(self.nextValidOrderId+1, contract, order)
        self.reqExecutions(self.nextValidOrderId, execFilter)
#        self.reqMktData(self.nextValidOrderId, contract, "", False, False, []) 

    def stop(self):
        self.done = True
        self.disconnect()

def main():
    try:
        app = ExecutionsDetails()
        app.connect('192.168.43.222', 7497, clientId=0)
        print(f'{app.serverVersion()} --- {app.twsConnectionTime().decode()}')
        print(f'ibapi version: ', ibapiTest.__version__)
#        Timer(5, app.stop).start()
        app.run()
    except Exception as err:
        print(err)

if __name__ == '__main__':
    main()