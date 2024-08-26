#! /usr/bin/env python3

import datetime
import logging
from ib_insync import *
import time

#ib = IB()
#ib.connect('127.0.0.1', 7496, clientId=1)

contract = Stock('BMW', 'SMART', 'EUR')
dt = ''
barList = []

class MyBot(IB):

    def __init__(self):
        IB.__init__(self)
        self.ib = IB()

    def getHistoricalData(self):
        bar = self.ib.reqHistoricalData(
                contract,
                endDateTime=dt,
                durationStr='60 S',
                barSizeSetting='1 min',
                whatToShow='MIDPOINT',
                useRTH=True,
                formatDate=1,
                keepUpToDate=True
                )
        print(f"[+] Current reqId: {bar.reqId}")
        self.ib.cancelHistoricalData(bar)

    def start(self):
        self.ib.connect('127.0.0.1', 7496, clientId=1)
        while True:
            self.getHistoricalData()

if __name__ == "__main__":
    
    bot = MyBot()
    bot.start()
