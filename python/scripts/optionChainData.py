#! /usr/bin/env python3

import logging
from threading import Timer
import ibapi
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.contract import Contract

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

    def contractDetails(self, reqId, contractDetails):
        super().contractDetails(reqId, contractDetails)
        print("contract details: ", reqId,
                contractDetails.contract.tradingClass + '\n',
                contractDetails.contract.strike + '\n',
                contractDetails.contract.lastTradeDateOrContractMonth)

    def tickPrice(self, reqId, tickType, price: float,
                  attrib):
        super().tickPrice(reqId, tickType, price, attrib)
        print("TickPrice. TickerId:", reqId, "tickType:", tickType,
              "Price:", floatMaxString(price), "CanAutoExecute:", attrib.canAutoExecute)

    def tickSize(self, reqId, tickType, size):
        super().tickSize(reqId, tickType, size)
        print("TickSize. TickerId:", reqId, "TickType:", tickType, "Size: ", decimalMaxString(size))
    #
    # Provides next valid identifier needed to place an order
    # Indicates that the connection has been established and other messages can be sent from
    # API to TWS
    def nextValidId(self, orderId):
        super().nextValidId(orderId)
        logging.debug(f"Next valid ID is set to {orderId}")
        self.nextValidOrderId = orderId # Snippet 1
        self.start()

    def getChainData(exchange, underlyingConId, tradingClass, multiplier, expirations, strikes):
        for strike in strikes:
            for ex in expirations:

                contract = Contract()

                contract.symbol = "IBM"
                contract.secType = "OPT" 
                contract.exchange = exchange
                contract.underlyingConId = underlyingConId
                contract.tradingClass = tradingClass
                contract.multiplier = multiplier
                contract.lastTradeDateOrContractMonth = ex
                contract.strike = strike

                self.reqContractDetails(self.nextValidOrderId, contract)


    def securityDefinitionOptionParameter(self, reqId: int, exchange: str,
                                          underlyingConId: int, tradingClass: str, multiplier: str,
                                          expirations, strikes):
        super().securityDefinitionOptionParameter(reqId, exchange,
                                                  underlyingConId, tradingClass, multiplier, expirations, strikes)

#        getChainData(exchange, underlyingConId, tradingClass, multiplier, expirations, strikes)
        print(strikes)
        print(expirations)


    def start(self):
        contract = Contract()
        contract.exchange = "SMART"
        contract.symbol = "AAPL"
        contract.secType = "OPT"
        contract.currency = "USD"
        self.reqContractDetails(self.nextValidOrderId, contract)
#        self.reqSecDefOptParams(self.nextValidOrderId, "IBM", "", "STK", 8314)

    def stop(self):
        self.done = True
        self.disconnect()


def main():
    try:
        app = TestApp()
        app.connect('192.168.43.222', 4002, clientId=0)
        print(f'{app.serverVersion()} --- {app.twsConnectionTime().decode()}')
        print(f'ibapi version: ', ibapi.__version__)
        Timer(5, app.stop).start()
        app.run()
    except Exception as err:
        print(err)

if __name__ == '__main__':
    main()
