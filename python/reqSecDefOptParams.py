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
from ibapi.utils import decimalMaxString, floatMaxString, intMaxString
from accumulate_distribute import pair

"""

    Get Options data for SPX OPT USD CBOE using options chains
    Observe SPX and SPXW in the resulti - note the expiry
    NB. SPXW is the S&P 500 weekly Options, is traded on CBOE
    SPXW is set as trading class.
    reqSecDefOptParams for SPX IND -> reqContractDetails for every strike-exp
    pair in response

"""

g_strike = 0
g_expiry = 0
g_right = 0

def usTechOpt(symbol, sec_type="OPT", currency="USD", exchange="CBOE"):
    global g_right, g_expiry, g_strike
    contract = Contract()
    contract.symbol = symbol
    contract.secType = sec_type
    contract.currency = currency
    contract.exchange = exchange
    contract.strike = g_strike
    contact.right = g_right
    contract.lastTradeDateOrContractMonth = g_expiry
    contract.multiplier = 100
    contract.tradingClass = ""
    return Contract

def spx_contract(symbol="SPX", secType="OPT", currency="USD", exchange="CBOE"):
    contract = Contract()
    contract.symbol = symbol
    contract.secType = secType
    contract.currency = currency
    contract.exchange = exchange
    return contract

def sample_contract():

    contract = Contract()
    contract.symbol = "AAPL"
    contract.exchange = "SMART"
    contract.currency = "USD"
    contract.secType = "STK"
    
    return contract

def spx_index():

    contract = Contract()
    contract.symbol = "SPX"
    contract.secType = "IND"
    contract.exchange = "CBOE" 
    contract.currency = "USD"

    return contract

def spxw_opt():

    contract = Contract()
    contract.symbol = "SPX"
    contract.secType = "OPT"
    contract.exchange = "SMART"
    contract.currency = "USD"
    contract.tradingClass = "SPXW"
    contract.multiplier = 100
    contract.lastTradeDateOrContractMonth = "20230307"
    contract.strike = 4100.0 

    return contract

def eminiContract():

    contract = Contract()
    contract.exchange = "CME"
    contract.symbol = "NQM3"
    contract.currency = "USD"
    contract.secType= "FUT"
    contract.multiplier = 20
    contract.lastTradeDateOrContractMonth = "20230616"

    return contract

class TestApp(EWrapper, EClient):

    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, self)


    def error(self, reqId: int, errorCode: int, errorString: str,
            advansedOrderreject):
        super().error(reqId, errorCode, errorString, advansedOrderreject)
        error_message = f'Error id: {reqId}, Error code: {errorCode}, ' \
                        + f'Msg: {errorString}'

    def currentTime(self, time:int):
        super().currentTime(time)
        print("CurrentTime:", datetime.datetime.fromtimestamp(time).strftime("%Y%m%d-%H:%M:%S"))

    def nextValidId(self, orderId):
        #super().nextValidId(orderId)
        logging.debug(f"Next valid ID is set to {orderId}")
        self.nextValidOrderId = orderId
        self.start()
        print(f"Next valid order ID: {orderId}")

    def securityDefinitionOptionParameter(self, reqId: int, exchange: str,
                                          underlyingConId: int, tradingClass: str, multiplier: str,
                                          expirations, strikes):
        super().securityDefinitionOptionParameter(reqId, exchange,
                                                  underlyingConId, tradingClass, multiplier, expirations, strikes)
        print("SecurityDefinitionOptionParameter.",
                  "ReqId:", reqId, "Exchange:", exchange, "Underlying conId:", intMaxString(underlyingConId), "TradingClass:", tradingClass, "Multiplier:", multiplier,
                  "Expirations:", expirations, "Strikes:", str(strikes))


    def contractDetails(self, reqId: int, contractDetails):
        super().contractDetails(reqId, contractDetails)
        print(contractDetails)

    def start(self):
        self.reqCurrentTime()
#        self.reqSecDefOptParams(self.nextValidOrderId, "AAPL", "", "STK", 265598)

        contract = Contract()
        contract.symbol = "AAPL"
        contract.secType = "OPT"
        contract.exchange = "CBOE"
        contract.underlyingConId = 265598
        contract.tradingClass = "AAPL"
        contract.multiplier = 100
        contract.right = "PUT"
        contract.lastTradeDateOrContractMonth = "20230818"
        self.reqContractDetails(self.nextValidOrderId, contract)

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
