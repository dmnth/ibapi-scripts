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
from ibapi.tag_value import TagValue
# from ibapi import CustomContracts
from ibapi.execution import ExecutionFilter
from ibapi.contract import ComboLeg

PORT = 9496

def getJGBFuture():
    contract = Contract()
    contract.conId = 582517266
    return contract


class PlaceLegOrders(EWrapper, EClient):

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
        # super().nextValidId(orderId)
        logging.debug(f"Next valid ID is set to {orderId}")
        self.nextValidOrderId = orderId
        self.start()
        print(f"Next valid order ID: {orderId}")

    def contractDetails(self, reqId, contractDetails):
        super().contractDetails(reqId, contractDetails)
        print("contract details: ", reqId, contractDetails)
        self.nextValidOrderId = reqId + 1
        order = Order()
        order.orderType = "MKT"
        order.action = 'BUY'
        order.totalQuantity = 1

        contract: Contract = contractDetails.contract
        self.placeOrder(self.nextValidOrderId, contract, order)

    def contractDetailsEnd(self, reqId: int):
        print(
            datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3],
            "contractDetailsEnd.",
            f"reqId:{reqId}",
        )

    def openOrder(self, orderId, contract, order: Order,
                  orderState):
        super().openOrder(orderId, contract, order, orderState)
        if orderId == None:
            print("OpenOrder. PermId:", intMaxString(order.permId), "ClientId:", intMaxString(order.clientId),
                  " OrderId:", intMaxString(orderId), "Account:", order.account, "Symbol:", contract.symbol, "SecType:",
                  contract.secType,
                  "Exchange:", contract.exchange, "Action:", order.action, "OrderType:", order.orderType,
                  "TotalQty:", decimalMaxString(order.totalQuantity), "CashQty:", floatMaxString(order.cashQty),
                  "LmtPrice:", floatMaxString(order.lmtPrice), "AuxPrice:", floatMaxString(order.auxPrice), "Status:",
                  orderState.status,
                  "MinTradeQty:", intMaxString(order.minTradeQty), "MinCompeteSize:",
                  intMaxString(order.minCompeteSize),
                  "competeAgainstBestOffset:", floatMaxString(order.competeAgainstBestOffset),
                  "MidOffsetAtWhole:", floatMaxString(order.midOffsetAtWhole), "MidOffsetAtHalf:",
                  floatMaxString(order.midOffsetAtHalf))

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
        print("ExecDetails. ReqId:", reqId, "Symbol:", contract.symbol, "SecType:", contract.secType, "Currency:",
              contract.currency, execution)

    def execDetailsEnd(self, reqId: int):
        super().execDetailsEnd(reqId)
        print("ExecDetailsEnd. ReqId:", reqId)
        self.stop()

    def openOrderEnd(self):
        super().openOrderEnd()
        print("OpenOrderEnd")

    def placeLeg(self):

        jgbContract = getJGBFuture()
        orderId = self.nextValidOrderId
        self.reqContractDetails(reqId=orderId, contract=jgbContract)
        #self.placeOrder(orderId, jgbContract, order)

        execFilter = ExecutionFilter()
        self.reqExecutions(self.nextValidOrderId, execFilter)

    def start(self):

        self.placeLeg()

    def stop(self):
        self.done = True
        self.disconnect()


def main():
    try:
        app = PlaceLegOrders()
        app.connect('192.168.43.222', 7496, clientId=0)
        print(f'{app.serverVersion()} --- {app.twsConnectionTime().decode()}')
        print(f'ibapi version: ', ibapi.__version__)
        #        Timer(15, app.stop).start()
        app.run()
    except Exception as err:
        print(err)


if __name__ == '__main__':
    main()
