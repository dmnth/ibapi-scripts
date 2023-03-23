import logging
import ibapi
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.contract import Contract
from ibapi.execution import Execution
from bracket_order import BracketOrder

# Bracket order with parent of type market 
# stopLoss and takeProfit are set with n% values
# from execution price of parent order

class TestApp(EWrapper, EClient):


    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, self)
        self.dataframe = {}

    # WRAPPERS HERE

    def error(self, reqId: int, errorCode: int, errorString: str,
              advansedOrderreject):
        super().error(reqId, errorCode, errorString, advansedOrderreject)
        error_message = f'Error id: {reqId}, Error code: {errorCode}, ' \
                        + f'Msg: {errorString}'
        print(error_message)
    #
    # Provides next valid identifier needed to place an order
    # Indicates that the connection has been established and other messages can be sent from
    # API to TWS
    def nextValidId(self, orderId):
        super().nextValidId(orderId)
        logging.debug(f"Next valid ID is set to {orderId}")
        self.nextValidOrderId = orderId # Snippet 1
        print(self.nextValidOrderId)
        self.start()

    def execDetails(self, reqId: int, contract: Contract, execution: Execution):
        super().execDetails(reqId, contract, execution)
        print("ExecDetails. ReqId:", reqId, "Symbol:", contract.symbol, "SecType:", contract.secType, "Currency:", contract.currency, execution)
        if execution.orderId == self.nextValidOrderId:
            print("Here order will be modified")
            self.modifyBracketOrder(execution.orderId, execution.price)

    def execDetailsEnd(self, reqId: int):
        super().execDetailsEnd(reqId)
        print("ExecDetailsEnd. ReqId:", reqId)

    def modifyBracketOrder(self, orderID, execPrice):
        stopPrice = execPrice - execPrice * 0.01
        takePrice = execPrice + execPrice * 0.01

        contract = Contract()
        contract.exchange = "SMART"
        contract.symbol = "BMW"
        contract.currency = "EUR"
        contract.secType = "STK"
        # takeprofitlimitprice value can be set to any value, or completely removed from bracket order implementation
        bracket_order = BracketOrder(parentOrderId=execution.orderId,
                                     action="BUY",
                                     quantity=1,
                                     limitPrice=1,
                                     takeProfitLimitPrice=takePrice,
                                     stopLossPrice=stopPrice)
        for bo in bracket_order[1:]:
            self.placeOrder(bo.orderId, contract, bo)

    def placeBracketOrder(self, orderID, takeProfitPrice, stopLossPrice):
        bracket_order = BracketOrder(orderID, "BUY", 1,limitPrice=1, takeProfitLimitPrice=takeProfitPrice,
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
        app.connect('127.0.0.1', 7496, clientId=0)
        print(f'{app.serverVersion()} --- {app.twsConnectionTime().decode()}')
        print(f'ibapi version: ', ibapi.__version__)
#        Timer(5, app.stop).start()
        app.run()
    except Exception as err:
        print(err)

if __name__ == '__main__':
    main()
