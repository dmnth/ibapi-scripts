#! /usr/bin/env python3

import logging
import datetime
from threading import Timer
import ibapi
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.order import Order
from ibapi.contract import Contract
from datetime import datetime

class CustomContracts():

    def __init__(self):
        self.args = ""

    def forex_pair(self):

        contract = Contract()
        contract.symbol = "EUR"
        contract.exchange = "IDEALPRO"
        contract.secType = "CASH"
        contract.currency = "USD"

        return contract

    def bmw_contract(self):

        contract = Contract()
        contract.symbol = 'BMW'
        contract.exchange = 'SMART'
        contract.currency = 'EUR'
        contract.secType = "STK"
        
        return contract

    def ndx_nasdaq_contract(self):

        contract = Contract()
        contract.symbol = "NDX"
        contract.secType = "STK"
        contract.exchange = "VALUE"
        contract.currency = "CAD"

        return contract

    def ndx_idx_nasdaq(self):

        contract = Contract()
        contract.symbol = "NDX"
        contract.secType = "IND"
        contract.exchange = "NASDAQ"
        contract.currency = "USD"

        return contract

    def cnh_contract(self):
        contract = Contract()
        contract.symbol = "CNH"
        contract.lastTradeDateOrContractMonth = "20230416"
        contract.secType = "FUT"
        contract.multiplier = 100000
        contract.exchange = "CME"
        contract.currency = "CNH"
        contract.localSymbol = "CNHJ3"
        return contract

    def spy_contract(self):
        contract = Contract()
        contract.symbol = "SPY"
        contract.secType = "OPT"
        contract.exchange = "SMART"
        contract.lastTradeDateOrContractMonth = "20230818"
        contract.right = "CALL"
        contract.strike = "330"
        return contract

    def idx_contract(self):
        contract = Contract()
        contract.symbol = "SPX"
        contract.exchange = "CBOE"
        contract.currency = "USD"
        contract.secType = "IND"

        return contract

    def options_contract(self):
        contract = Contract()
        contract.symbol = "SPY"
        contract.secType = "OPT"
        contract.exchange = "SMART"
        contract.currency = "USD"
        contract.right = "P"
        contract.strike = 396
        contract.lastTradeDateOrContractMonth = "202303"
        return contract

    def tsla_contract(self):

        contract = Contract()

        contract.symbol = "TSLA"
        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.currency = "USD"

        return contract

    def shkntl_contract(self):

        contract = Contract()
        contract.symbol = "600519"
        contract.secType = "STK"
        contract.exchange = "SEHKNTL"
        contract.currency = "CNH"

        return contract

    def qmi_contract(self):

        contract = Contract()
        contract.symbol = "QMI"
        contract.secType = "IND"
        contract.currency = "USD"
        contract.exchange = "NASDAQ"

        return contract


contracts = CustomContracts()

class TestApp(EWrapper, EClient):

    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, self)

    # WRAPPERS HERE

    def error(self, reqId: int, errorCode: int, errorString: str,
            advansedOrderreject=''):
        super().error(reqId, errorCode, errorString, advansedOrderreject)
        error_message = f'Error id: {reqId}, Error code: {errorCode}, ' \
                        + f'Msg: {errorString}'

    def historicalData(self, reqId, bar):
        super().historicalData(reqId, bar)
        print("Historical data: ", reqId, bar)
    
    def contractDetails(self, reqId, contractDetails):
        super().contractDetails(reqId, contractDetails)
        print("contract details: ", reqId, contractDetails)

    # Provides next valid identifier needed to place an order
    # Indicates that the connection has been established and other messages can be sent from
    # API to TWS
    def nextValidId(self, orderId):
        #super().nextValidId(orderId)
        logging.debug(f"Next valid ID is set to {orderId}")
        self.nextValidOrderId = orderId
        self.start()
        print(f"Next valid order ID: {orderId}")

    def headTimestamp(self, reqId, headTimeStamp):
        print("HeadTimeStamp: ", headTimeStamp)

    def convert_unix_timestamp(self, stamp):
        print(stamp)
        ts = int(stamp)
        print(datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S"))
        
    def historicalTicksBidAsk(self, reqId: int, ticks,
                              done: bool):
        for tick in ticks:
            self.convert_unix_timestamp(tick.time)
            print("HistoricalTickBidAsk. ReqId:", reqId, tick)

    def historicalTicksLast(self, reqId: int, ticks,
                            done: bool):
        for tick in ticks:
            self.convert_unix_timestamp(tick.time)
            print("HistoricalTickLast. ReqId:", reqId, tick)

    def start(self):
        timezone = "US/Eastern"
        querytime = f"20230127 15:00:00 {timezone}"

        contract = contracts.qmi_contract()

        self.reqContractDetails(self.nextValidOrderId, contract)
        startDate = f"20230308 10:30:00 {timezone}"
        endDate = f'20230308 16:30:00 {timezone}'
        self.reqHeadTimeStamp(self.nextValidOrderId, contract, "TRADES", True,
                1)

#        self.reqHistoricalTicks(self.nextValidOrderId, contract, startDate, "",
#                10, "TRADES", 1, True, [])
        self.reqHistoricalData(self.nextValidOrderId, contract, endDate, 
                '1 D', '5 secs', 'TRADES', 0, 1, False, [])
#        print(self.serverVersion())

    def stop(self):
        self.done = True
        self.disconnect()

def main():
    try:
        app = TestApp()
        app.connect('192.168.1.167', 7496, clientId=0)
        print(f'{app.serverVersion()} --- {app.twsConnectionTime().decode()}')
        print(f'ibapi version: ', ibapi.__version__)
#        Timer(5, app.stop).start()
        app.run()
    except Exception as err:
        print(err)

if __name__ == '__main__':
    main()
