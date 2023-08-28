#! /usr/bin/env python3

import logging
import ibapi
import time
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.order import Order
from ibapi.contract import Contract
from ibapi.execution import Execution
from ibapi.utils import decimalMaxString, floatMaxString, intMaxString, Decimal
from bracketOrder import bracketOrder, stopProfit

class TestApp(EWrapper, EClient):


    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, self)
        self.dataframe = {}

    def error(self, reqId: int, errorCode: int, errorString: str,
              advansedOrderreject=""):
        super().error(reqId, errorCode, errorString, advansedOrderreject)
        error_message = f'Error id: {reqId}, Error code: {errorCode}, ' \
                        + f'Msg: {errorString}'
        print(error_message)
       
    def nextValidId(self, orderId):
        super().nextValidId(orderId)
        logging.debug(f"Next valid ID is set to {orderId}")
        self.nextValidOrderId = orderId # Snippet 1
        print(self.nextValidOrderId)
        self.start()

    def openOrder(self, orderId, contract, order: Order,
                  orderState):
        super().openOrder(orderId, contract, order, orderState)
        print(f"openOrder {orderId}\nContract {contract}\n########################")

    def orderStatus(self, orderId, status: str, filled: Decimal,
                    remaining: Decimal, avgFillPrice: float, permId: int,
                    parentId: int, lastFillPrice: float, clientId: int,
                    whyHeld: str, mktCapPrice: float):
        super().orderStatus(orderId, status, filled, remaining,
                            avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice)
        if status == "Filled":
            print(f"orderStatus: {orderId}, {filled}, {status}")

    def openOrderEnd(self):
        super().openOrderEnd()
        print("OpenOrderEnd")

    def execDetails(self, reqId: int, contract: Contract, execution: Execution):
        super().execDetails(reqId, contract, execution)
        print("ExecDetails. ReqId:", reqId, "Symbol:", contract.symbol, "SecType:", contract.secType, "Currency:", contract.currency, execution)
        if execution.orderId == self.nextValidOrderId:
            print(f"Order status: {execution}")
            self.modifyBracketOrder(execution.orderId, execution.price)

    def execDetailsEnd(self, reqId: int):
        super().execDetailsEnd(reqId)
        print("ExecDetailsEnd. ReqId:", reqId)

    def modifyBracketOrder(self, orderID, execPrice):
        print("modifying the bracket order")
        stopPrice = execPrice - (execPrice * 0.5)
        takePrice = execPrice + (execPrice * 0.5)

        contract = Contract()
        contract.exchange = "SMART"
        contract.symbol = "BMW"
        contract.currency = "EUR"
        contract.secType = "STK"
        modOrder = stopProfit(parentOrderId=orderID,
                                     action="BUY",
                                     quantity=4,
                                     limitPrice=100,
                                     takeProfitLimitPrice=takePrice,
                                     stopLossPrice=stopPrice)
        time.sleep(10)
        for o in modOrder:
            self.placeOrder(o.orderId, contract, o)

    def placeBracketOrder(self, orderID, takeProfitPrice, stopLossPrice):
        bracket_order = bracketOrder(orderID, "BUY", 1,limitPrice=1, takeProfitLimitPrice=takeProfitPrice,
                                     stopLossPrice=stopLossPrice)
        contract = Contract()
        contract.exchange = "SMART"
        contract.symbol = "BMW"
        contract.currency = "EUR"
        contract.secType = "STK"
        for bo in bracket_order:
            self.placeOrder(bo.orderId, contract, bo)

    def start(self):
        self.placeBracketOrder(self.nextValidOrderId, 103, 80)
        print("Hello, order id is: ", self.nextValidOrderId)

    def stop(self):
        self.done = True
        self.disconnect()


def main():
    try:
        app = TestApp()
        app.connect('192.168.43.222', 7496, clientId=0)
        print(f'{app.serverVersion()} --- {app.twsConnectionTime().decode()}')
        print(f'ibapi version: ', ibapi.__version__)
#        Timer(5, app.stop).start()
        app.run()
    except Exception as err:
        print(err)

if __name__ == '__main__':
    main()
