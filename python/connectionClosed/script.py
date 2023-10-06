#! /usr/bin/env python3

import logging
import ibapi
from ibapi.wrapper import EWrapper
from ibapi.client import EClient

class PlaceBagOrders(EWrapper, EClient):

    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, self)

    # WRAPPERS HERE

    def error(self, reqId: int, errorCode: int, errorString: str,
            advansedOrderreject=""):
        super().error(reqId, errorCode, errorString, advansedOrderreject)
        error_message = f'Error id: {reqId}, Error code: {errorCode}, ' \
                        + f'Msg: {errorString}'

    def nextValidId(self, orderId):
        #super().nextValidId(orderId)
        logging.debug(f"Next valid ID is set to {orderId}")
        self.nextValidOrderId = orderId
        self.start()
        print(f"Next valid order ID: {orderId}")

    def connectionClosed(self):
        print("Connection has been closed occasionally")

    def start(self):
        return


    def stop(self):
        self.done = True
        self.disconnect()


def main():
    try:
        app = PlaceBagOrders()
        app.connect('192.168.43.222', 7497, clientId=0)
        print('{app.serverVersion()} --- {app.twsConnectionTime().decode()}')
        print(f'ibapi version: ', ibapi.__version__)
#        Timer(15, app.stop).start()
        app.run()
    except Exception as err:
        print(err)

if __name__ == '__main__':
    main()
