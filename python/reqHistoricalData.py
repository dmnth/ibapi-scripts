#! /usr/bin/env python3

import logging
import datetime
import time
from threading import Timer
import ibapi
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.order import Order
from ibapi.contract import Contract
from datetime import datetime
from threading import Thread
from contracts import CustomContracts 


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
        print("Historical data: ", reqId, bar.open, bar.volume)
    
    def contractDetails(self, reqId, contractDetails):
        super().contractDetails(reqId, contractDetails)
        print("contract details: ", reqId, contractDetails.minTick)

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

    def historicalDataEnd(self, reqId, start, end):
        super().historicalDataEnd(reqId, start, end)
        print("Historical data end for: ", self.clientId)

    def start(self):
        # TWS will retunr data only for instrument's timezone or 
        # for time zone that is configured as local in TWS settings.
        timezone = "US/Eastern"
        querytime = f"202300518 13:00:00 {timezone}"
        contracts = CustomContracts()
        contract = contracts.audUSDcontract()
        print(self.clientId)
        self.reqContractDetails(self.nextValidOrderId, contract)
#        startDate = f"20230308 10:30:00 {timezone}"
#        endDate = f'20230418 16:30:00 {timezone}'
#        endDate = "20230418 16:30:00"
        endDate = ""
        self.reqHeadTimeStamp(self.nextValidOrderId, contract, "TRADES", True,
                1)

#        self.reqHistoricalTicks(self.nextValidOrderId, contract, startDate, "",
#                10, "TRADES", 1, True, [])
        self.reqHistoricalData(self.nextValidOrderId, contract, endDate, 
                '1 M', '1 hour', 'BID_ASK', 0, 1, False, [])
#        print(self.serverVersion())

    def stop(self):
        self.done = True
        self.disconnect()

# Create a list of clients:
def threadedExecution():

    def createConnectApp(ip, port, clientId):
        print("Connected")
        app = TestApp()
        app.connect(ip, port, clientId)
        app.run()
    
    cls = []
    for i in range(2):
        thread = Thread(target=createConnectApp, args=("192.168.1.167", 7496, i))
        thread.start()
        cls.append(thread)

    for thread in cls:
        thread.join()


def main():
    try:
        app = TestApp()
        app.connect('192.168.43.222', 7496, clientId=0)
        print(f'{app.serverVersion()} --- {app.twsConnectionTime().decode()}')
        print(f'ibapi version: ', ibapi.__version__)
        app.run()
    except Exception as err:
        print(err)

if __name__ == '__main__':
    main()
