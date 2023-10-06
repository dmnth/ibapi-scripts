#! /usr/bin/env python3

import ibapi
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.contract import (Contract, ContractDetails)
from ibapi.utils import Decimal, decimalMaxString, floatMaxString

def MarketOrder(action:str, quantity:Decimal):

    order = Order()
    order.action = action
    order.orderType = "MKT"
    order.totalQuantity = quantity

    return order

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

    def position(self, account: str, contract: Contract, position: Decimal,
                 avgCost: float):
        super().position(account, contract, position, avgCost)
        print("Position.", "Account:", account, "Symbol:", contract.symbol, "SecType:",
              contract.secType, "Currency:", contract.currency,
              "Position:", decimalMaxString(position), "Avg cost:", floatMaxString(avgCost))
        order = MarketOrder("SELL", position)
        contract = contract

        self.placeOrder(self.nextValidOrderId, contract, order)
        
    def positionEnd(self):
        super().positionEnd()
        print("Position End")

    # Place requests here
    def start(self):
        self.reqPositions()


    def stop(self):
        self.done = True
        self.disconnect()

def main():
    try:
        app = TestApp()
        app.connect('192.168.43.222', 7496, clientId=1)
        app.run()
    except Exception as err:
        print(err)

if __name__ == '__main__':
    main()
