#! /usr/bin/env python3
import ibapi
import logging
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.contract import Contract
#from contracts import CustomContracts


class TestApp(EWrapper, EClient):

    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, self)

    # WRAPPERS HERE

#    def error(self, reqId: int, errorCode: int, errorString: str,
#            advansedOrderreject=""):
#        super().error(reqId, errorCode, errorString, advansedOrderreject)
#        error_message = f'Error id: {reqId}, Error code: {errorCode}, ' \
#                        + f'Msg: {errorString}'

    # Provides next valid identifier needed to place an order
    # Indicates that the connection has been established and other messages can be sent from
    # API to TWS
    def nextValidId(self, orderId):
        #super().nextValidId(orderId)
        logging.debug(f"Next valid ID is set to {orderId}")
        self.nextValidOrderId = orderId
        self.start()
        print(f"Next valid order ID: {orderId}")

    def historicalData(self, reqId, bar):
        super().historicalData(reqId, bar)
        print("Historical data: ", reqId, bar)

    def historicalDataEnd(self, reqId, start, end):
        super().historicalDataEnd(reqId, start, end)
        print("Historical data end for: ", self.clientId)

    def receiveFA(self, faData, cxml):
        super().receiveFA(faData, cxml)
        print("Receiving FA: ", faData)
        open("receivedFA.xml", 'w').write(cxml)

    def start(self):


        faString = open('simpleXml.xml', 'r').read()
        xmlString = faString.replace("\t", "").replace("\n", "")
        print(xmlString)
#        faString = '?xml version="1.0" encoding="UTF-8"?><ListOfGroups><Group><name>Profile_ContractsShares</name><defaultMethod>ContractsOrShares</defaultMethod><ListOfAccts varName="list"><Account><acct>DU74649</acct><amount>1</amount></Account><Account><acct>DU74650</acct><amount>1</amount></Account></ListOfAccts></Group></ListOfGroups>'
#        print(faString)
        self.replaceFA(self.nextValidOrderId, 1, xmlString)
        self.requestFA(1)

    def stop(self):
        self.done = True
        self.disconnect()

def main():
    try:
        app = TestApp()
        app.connect('192.168.1.167', 7496, clientId=1)
        print(f'{app.serverVersion()} --- {app.twsConnectionTime().decode()}')
        print(f'ibapi version: ', ibapi.__version__)
#        Timer(15, app.stop).start()
        app.run()
    except Exception as err:
        print(err)

if __name__ == '__main__':
    main()
