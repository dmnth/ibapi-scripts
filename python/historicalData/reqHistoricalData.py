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
from zoneinfo import ZoneInfo


class TestApp(EWrapper, EClient):

    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, self)
        self.historicalBars = []

    # WRAPPERS HERE

    def error(self, reqId: int, errorCode: int, errorString: str,
            advansedOrderreject=''):
        super().error(reqId, errorCode, errorString, advansedOrderreject)
        error_message = f'Error id: {reqId}, Error code: {errorCode}, ' \
                        + f'Msg: {errorString}'

    def historicalData(self, reqId, bar):
        super().historicalData(reqId, bar)
        print("Historical data: ", reqId, bar.date, f"BID: {bar.open}", f"CLOSE: {bar.close}", type(bar)) 
        self.historicalBars.append(bar)

    def historicalDataEnd(self, reqId, start, end):
        super().historicalDataEnd(reqId, start, end)
        #TODO: crop timezone id into separate string.
        #TODO: format bar date time to more human readable form
        if len(self.historicalBars) != 0:
            print("Writing bars...")
            with open('eurUsd/17d1m.txt', 'a') as file:
                file.write(f"{start}-{end}\n")
                file.write("BAR DATE   OPEN   HIGH    LOW\n")
                for bar in self.historicalBars:
                    time = datetime.fromtimestamp(int(bar.date), tz=ZoneInfo("UTC"))
                    string = f"{time}, {bar.open}, {bar.high}, {bar.low}\n"
                    file.write(string)
                file.write('\n')
                file.close()
                print("Finished writing bars")
        print("Historical data end for: ", self.clientId)
        self.disconnect()
    
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
        # TWS will retunr data only for instrument's timezone or 
        # for time zone that is configured as local in TWS settings.
        timezone = "US/Eastern"
#        timezone = "US/Central"
        querytime = f"20230518 15:00:00 {timezone}"
        contract = CustomContracts().eudUsdContract()
        print(self.clientId)
        self.reqContractDetails(self.nextValidOrderId, contract)
#        endDateTime= f"20230904 10:30:00 {timezone}"
#        endDate = f'20230418 16:30:00 {timezone}'
#        endDate = f"20230211 16:30:00 {timezone}"
        endDate = "20231003-15:19:28"
        self.reqHeadTimeStamp(self.nextValidOrderId, contract, "MIDPOINT", True,
                1)

#        self.reqHistoricalTicks(self.nextValidOrderId, contract, startDate, endDate,
#                10, "TRADES", 1, True, [])
        self.reqHistoricalData(self.nextValidOrderId, contract, endDate, 
                '17 D', '1 min', 'MIDPOINT', 1, 1, False, [])
#        print(self.serverVersion())

    def stop(self):
        self.done = True
        self.disconnect()

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
