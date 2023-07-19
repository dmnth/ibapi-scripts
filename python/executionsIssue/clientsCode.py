#! /usr/bin/env python3

from ibapi.client import *
from ibapi.wrapper import *

class TestApp(EClient, EWrapper):

    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId):
        execFilter = ExecutionFilter()
        execFilter.time = "20230717-02:00:00"
        execFilter.secType = "BAG"
        self.reqExecutions(orderId, execFilter)
    
    def execDetails(self, reqId, contract, execution):
        print(reqId, contract, execution)

    def execDetailsEnd(self, reqId):
        print("ExecDetailsEnd", " ", reqId)

app = TestApp()
app.connect("192.168.43.222", 7497, 1007)
app.run()

