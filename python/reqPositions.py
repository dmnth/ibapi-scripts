#! /usr/bin/env python3

import logging
import datetime
from threading import Timer
import ibapi
import time
import csv
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.order import Order
from ibapi.contract import Contract
from ibapi.utils import decimalMaxString, floatMaxString, intMaxString, Decimal
from datetime import datetime

class TestApp(EWrapper, EClient):

    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, self)
        self.account = "DU6036902"
        self.positions = []

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

    def position(self, account: str, contract: Contract, position: Decimal,
                 avgCost: float):
        super().position(account, contract, position, avgCost)
        print(account, contract.symbol, contract.secType, contract.currency, position, avgCost)
        timeStamp = datetime.now()
        string = [f"[{timeStamp}] -- {account},{contract.symbol},{contract.secType},{contract.currency}," +\
                f"{position},{avgCost}"]
#        if string not in self.position:
        self.positions.append(string)

    def positionEnd(self):
        super().positionEnd()
        print("PositionEnd")
        if len(self.positions) != 0:
            print("Writing positions...")
            with open('positionsTest.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile, quotechar='|')
                writer.writerow(["##########BEGIN#########\n"])
                writer.writerows(self.positions)
                writer.writerow(["##########FIN#########\n"])
                print("Finished writing positions")
        print("Positions data end for: ", self.clientId)
        time.sleep(10)
        self.reqPositions()
#        self.disconnect()

    def contractDetails(self, reqId: int, contractDetails):
        super().contractDetails(reqId, contractDetails)
        print(contractDetails.contract.exchange , '\n')

        contract = Contract()
        contract.conId = contractDetails.contract.conId
        contract.exchange = contractDetails.contract.exchange

        order = Order()
        order.action = "SELL"
        order.orderType = "MKT"
        order.totalQuantity = 1

#        self.placeOrder(self.nextValidOrderId, contract, order)

    def updatePortfolio(self, contract: Contract, position: Decimal,
                        marketPrice: float, marketValue: float,
                        averageCost: float, unrealizedPNL: float,
                        realizedPNL: float, accountName: str):
        super().updatePortfolio(contract, position, marketPrice, marketValue,
                                averageCost, unrealizedPNL, realizedPNL, accountName)
        print("UpdatePortfolio.", "Symbol:", contract.symbol, "SecType:", contract.secType, "Exchange:",
              contract.exchange, "Position:", decimalMaxString(position), "MarketPrice:", floatMaxString(marketPrice),
              "MarketValue:", floatMaxString(marketValue), "AverageCost:", floatMaxString(averageCost),
              "UnrealizedPNL:", floatMaxString(unrealizedPNL), "RealizedPNL:", floatMaxString(realizedPNL),
              "AccountName:", accountName)

    def openOrder(self, orderId, contract: Contract, order: Order,
                  orderState ):
        super().openOrder(orderId, contract, order, orderState)
        print("OpenOrder. PermId:", intMaxString(order.permId), "ClientId:", intMaxString(order.clientId), " OrderId:", intMaxString(orderId), 
              "Account:", order.account, "Symbol:", contract.symbol, "SecType:", contract.secType,
              "Exchange:", contract.exchange, "Action:", order.action, "OrderType:", order.orderType,
              "TotalQty:", decimalMaxString(order.totalQuantity), "CashQty:", floatMaxString(order.cashQty), 
              "LmtPrice:", floatMaxString(order.lmtPrice), "AuxPrice:", floatMaxString(order.auxPrice), "Status:", orderState.status,
              "MinTradeQty:", intMaxString(order.minTradeQty), "MinCompeteSize:", intMaxString(order.minCompeteSize),
              "competeAgainstBestOffset:",
              "MidOffsetAtWhole:", floatMaxString(order.midOffsetAtWhole),"MidOffsetAtHalf:" ,floatMaxString(order.midOffsetAtHalf))


    def start(self):
        contract = Contract()
        contract.conId = "254010991" 
        contract.exchange = "IPE" 

        order = Order()
        order.action = "SELL"
        order.orderType = "MKT"
        order.totalQuantity = 1
        self.reqPositions()

        self.reqAccountUpdates(True, self.account)

    def stop(self):
        self.done = True
        self.disconnect()

def main():
    try:
        app = TestApp()
        app.connect('192.168.43.222', 7496, clientId=0)
        print(f'{app.serverVersion()} --- {app.twsConnectionTime().decode()}')
        print(f'ibapi version: ', ibapi.__version__)
#        Timer(15, app.stop).start()
        app.run()
    except Exception as err:
        print(err)

if __name__ == '__main__':
    main()

