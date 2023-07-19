#! /usr/bin/env python3

import logging
import ibapi
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.order import Order
from ibapi.contract import Contract
from ibapi.utils import decimalMaxString, floatMaxString, intMaxString, Decimal
from ibapi.execution import ExecutionFilter
from ibapi.contract import ComboLeg 

class spreadContracts():

    def silverSpread(self):

        contract = Contract()

        contract.symbol = "SI"
        contract.secType = "BAG"
        contract.currency = "USD"
        contract.exchange = "COMEX"

        leg1 = ComboLeg()
        leg1.conId = 523408698
        leg1.ratio = 1
        leg1.action = "BUY"
        leg1.exchange = "COMEX"

        leg2 = ComboLeg()
        leg2.conId = 633994090 
        leg2.ratio = 1
        leg2.action = "BUY"
        leg2.exchange = "COMEX"

        contract.comboLegs = []
        contract.comboLegs.append(leg1)
        contract.comboLegs.append(leg2)

        return contract

    def goldSpread(self):

        contract = Contract()

        contract.symbol = "GC"
        contract.secType = "BAG"
        contract.currency = "USD"
        contract.exchange = "COMEX"

        leg1 = ComboLeg()
        leg1.conId = 639787335 
        leg1.ratio = 1
        leg1.action = "BUY"
        leg1.exchange = "COMEX"

        leg2 = ComboLeg()
        leg2.conId = 517660678 
        leg2.ratio = 1
        leg2.action = "BUY"
        leg2.exchange = "COMEX"

        contract.comboLegs = []
        contract.comboLegs.append(leg1)
        contract.comboLegs.append(leg2)

        return contract

    def copperSpread(self):

        contract = Contract()

        contract.symbol = "HG"
        contract.secType = "BAG"
        contract.currency = "USD"
        contract.exchange = "COMEX"

        leg1 = ComboLeg()
        leg1.conId = 511505493 
        leg1.ratio = 1
        leg1.action = "BUY"
        leg1.exchange = "COMEX"

        leg2 = ComboLeg()
        leg2.conId = 335154381 
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

    def execDetails(self, reqId: int, contract: Contract, execution):
        super().execDetails(reqId, contract, execution)
        print("ExecDetails. ReqId:", reqId, "Symbol:", contract.symbol, "SecType:", contract.secType, "Currency:", contract.currency, execution)

    def execDetailsEnd(self, reqId: int):
        super().execDetailsEnd(reqId)
        print("ExecDetailsEnd. ReqId:", reqId)

    def placeOrders(self, reqId):
        contracts = spreadContracts()

        goldSpreadContract = contracts.goldSpread()
        silverSpreadContract = contracts.silverSpread()
        copperSpreadContract = contracts.copperSpread()

        contracts = [goldSpreadContract, silverSpreadContract, copperSpreadContract]
        order = Order()
        order.orderType = "MKT"
        order.action = "BUY"
        order.totalQuantity = 1

        orderId = self.nextValidOrderId
        for contract in contracts:
            self.placeOrder(orderId, contract, order)
            orderId += 1


    def start(self):

#        self.placeOrders(self.nextValidOrderId)

        execFilter = ExecutionFilter()
        execFilter.time = "20230718 02:00:00"
        execFilter.secType = "BAG"
        self.reqExecutions(self.nextValidOrderId, execFilter) 

    def stop(self):
        self.done = True
        self.disconnect()


def main():
    try:
        app = PlaceBagOrders()
        app.connect('192.168.43.222', 7497, clientId=0)
        print('{app.serverVersion()} --- {app.twsConnectionTime().decode()}')
        print(f'ibapi version: ', ibapi.__version__)
#        Timer(15, app.stop).start()
        app.run()
    except Exception as err:
        print(err)

if __name__ == '__main__':
    main()
