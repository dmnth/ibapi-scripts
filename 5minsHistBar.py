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
        self.my_dict = {}

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
        # super().nextValidId(orderId)
        logging.debug(f"Next valid ID is set to {orderId}")
        self.nextValidOrderId = orderId
        self.start()
        print(f"Next valid order ID: {orderId}")

    # Gets constantly updated, all variables are reinitialised every call
    # One way is to determine how many minutes passed from last bar until
    # currently available bar if % 5 == 0, than its a five minute bar
    # Concurrent requests wont work since they all use same list
    def fiveMinBars(self, reqId, bar):
        if len(self.my_dict) != 0:
            last_available_bar = self.my_dict[reqId][-1].date
            current_tick = self.get_me_minutes(last_available_bar)
            next_tick = self.get_me_minutes(bar.date)
            one_tick = abs(int(current_tick) - int(next_tick))
            if one_tick != 0 and one_tick % 5 == 0:
                print("first occasion when match: ", reqId)
                print("5 mins passed")
                print("start: ", last_available_bar)
                print("end: ", datetime.now())
                print("current tick: ", current_tick)
                print("next tick: ", next_tick)
                self.my_dict[reqId].append(bar)
                return

    # Bars are received in async manner
    def historicalData(self, reqId: int, bar):
        super().historicalData(reqId, bar)
        # Create a field for every ID
        if reqId not in self.my_dict.keys():
            self.my_dict[reqId] = []
        # Add bars for received id
        self.my_dict[reqId].append(bar)


    # Since multiple reqId's are getting stored into
    # the dict - last item might not be the one with
    # current reqId
    # Need a way to store data in a way that for every reqid
    # latest available bar can be withdrawn {reqID: [bars]}
    def historicalDataUpdate(self, reqId, bar):
        super().historicalDataUpdate(reqId, bar)
        if reqId in self.my_dict.keys():
            self.fiveMinBars(reqId, bar)
            return

    def historicalDataEnd(self, reqId, start, end):
        super().historicalDataEnd(reqId, start, end)
        print("Historical data end for ", reqId, f"from {start} to {end}")

    def get_me_minutes(self, bar):
        mins = bar.split()[1].split(':')[1]
        return int(mins)

    def start(self):
        print(self.serverVersion())
    
        start = time.time()
        now = datetime.now().strftime("")
        id = self.nextValidOrderId
        cont = cont_list[0]
        for cont in cont_list:
            self.reqHistoricalData(id, cont, now, '1 D',
                                   '5 mins', "TRADES", useRTH=1, formatDate=1, keepUpToDate=True,
                                       chartOptions=[])
            id += 1

    def stop(self):
        self.done = True
        self.disconnect()


def main():
    try:
        app = TestApp()
        app.connect('127.0.0.1', 7496, clientId=0)
        print(f'{app.serverVersion()} --- {app.twsConnectionTime().decode()}')
        print(f'ibapi version: ', ibapi.__version__)
        app.run()
    except Exception as err:
        print(err)


if __name__ == '__main__':
    main()
