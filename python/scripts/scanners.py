#! /usr/bin/env python3

import logging
from threading import Timer
import ibapi
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.scanner import ScannerSubscription
from ibapi.tag_value import TagValue

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
        self.start()

    def scannerData(self, reqId: int, rank: int, contractDetails,
                    distance: str, benchmark: str, projection: str, legsStr: str):
        super().scannerData(reqId, rank, contractDetails, distance, benchmark,
                            projection, legsStr)
        print("ScannerData. ReqId:", reqId, contractDetails.contract, rank, distance, benchmark, projection, legsStr)

    def scannerDataEnd(self, reqId:int):
        super().scannerDataEnd(reqId)
        print("ScannerData ReqId: ", reqId)

    def start(self):

        scanner = ScannerSubscription()
        scanner.scanCode = "TOP_PERC_GAIN"
        scanner.instrument = "STK"
        scanner.locationCode = "STK.US.MAJOR"

        tag_values = []

        tag_values.append(TagValue("changePercAbove", "5"))

        self.reqScannerSubscription(self.nextValidOrderId, scanner, [], tag_values)

    def stop(self):
        self.done = True
        self.disconnect()


def main():
    try:
        app = TestApp()
        app.connect('127.0.0.1', 7496, clientId=0)
        print(f'{app.serverVersion()} --- {app.twsConnectionTime().decode()}')
        print(f'ibapi version: ', ibapi.__version__)
        Timer(5, app.stop).start()
        app.run()
    except Exception as err:
        print(err)

if __name__ == '__main__':
    main()
