#! /usr/bin/env python3

import time
import logging
import ibapi
from threading import Timer
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.order import Order
from ibapi.contract import Contract
from datetime import datetime 
from custom_contracts import contracts

class TestApp(EWrapper, EClient):

    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, self)
        self.my_list = []

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


    
    # Gets constantly updated, all variables are reinitialised every call
    # One way is to determine how many minutes passed from last bar until
    # currently available bar if % 5 == 0, than its a five minute bar
    def fiveMinBars(self, bar):
        if self.my_list:
            last_available_bar = self.my_list[-1][reqId].date
            current_tick = self.get_me_minutes(last_available_bar)
            next_tick = self.get_me_minutes(bar.date)
            one_tick = abs(int(current_tick) - int(next_tick)) 
            if one_tick != 0 and one_tick % 5 == 0:
                print("first occasion when match: ")
                print("5 mins passed")
                print("start: ", last_available_bar)
                print("end: ", datetime.now())
                print("current tick: ", current_tick)
                print("next tick: ", next_tick)
                self.my_list.append({reqId: bar})

    def historicalData(self, reqId: int, bar):
        super().historicalData(reqId, bar)
        print("Historical data for: ", reqId, bar)
        time.sleep(0.001)
    
    def historicalDataUpdate(self, reqId, bar):
        super().historicalDataUpdate(reqId, bar)

    def historicalDataEnd(self, reqId, start, end):
        super().historicalDataEnd(reqId, start, end)
        print("Historical data end for ", reqId, f"from {start} to {end}")

    def get_me_minutes(self, bar):
        mins = bar.split()[1].split(':')[1]
        return int(mins)


    def start(self):
        print(self.serverVersion())
#        sample_contract = contracts[1]
#        now = datetime.now().strftime("")
#        self.reqHistoricalData(self.nextValidOrderId, sample_contract, now, '1 D',
#                '1 min', "TRADES", useRTH=1, formatDate=1, keepUpToDate=False, 
#                chartOptions=[])
        
        while True:

            start = time.time()
            now = datetime.now().strftime("")
            id = self.nextValidOrderId
            for contract in contracts:
                self.reqHistoricalData(id, contract, now, '1 D',
                        '1 min', "TRADES", useRTH=1, formatDate=1, keepUpToDate=False, 
                        chartOptions=[])
                id += 1

    def stop(self):
        self.done = True
        self.disconnect()

def main():
    try:
        app = TestApp()
        app.connect('192.168.1.167', 7496, clientId=0)
        print(f'{app.serverVersion()} --- {app.twsConnectionTime().decode()}')
        print(f'ibapi version: ', ibapi.__version__)
        app.run()
    except Exception as err:
        print(err)

if __name__ == '__main__':
    main()
