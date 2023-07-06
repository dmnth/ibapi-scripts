#! /usr/bin/env python3


import logging
import datetime
import threading
import datetime
from threading import Timer
import ibapi
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.order import Order
from ibapi.contract import Contract
import json

class TestApp(EWrapper, EClient):


    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, self)
        self.dataframe = {}

    # WRAPPERS HERE

    def error(self, reqId: int, errorCode: int, errorString: str,
              advansedOrderreject=""):
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

    def compareDates(self, currentDate, endDate):
        print(currentDate, endDate)
        print(currentDate.replace('.0', ''))
        currentDate = currentDate.replace('.0', '')
        currentDateObject = datetime.datetime.strptime(currentDate, "%y-%m-%d %H:%M:%S") 
        print(currentDateObject)
        return True

    def historicalNews(self, reqId: int, time: str, providerCode: str,
                       articleId: str, headline: str):
        print(time, headline)
        endDate = "2022-05-28 23:59:59"
#        result = self.compareDates(time, endDate)

    def historicalNewsEnd(self, reqId, hasMore):
        super().historicalNewsEnd(reqId, hasMore)
        print(reqId, hasMore)

    def tickNews(self, tickerId, timeStamp, providerCode, articleId, headline, extraData):
        print(extraData)

#    def newsArticle(self, reqId: int, articleType: int, articleText: str):
#        print("NewsArticle. ReqId:", reqId, "ArticleType:", articleType,
#              "ArticleText:", articleText)
#        print('sentiment' in articleText)
#        print(articleText.index('sentiment'))
#        print(articleText[5060:5190])


    def tickPrice(self, reqId, tickType, price:float,
                  attrib):
        print(reqId, tickType, price, attrib)


    def start(self):
        print('@###################################')
        print("Start date is a lie")
        endDate = "asoklfbnhklasjdf"
        endDate = "'"
        endDate = "\u0000"
        endDate = 0x00 
        endDate = '\x0af'
        endDate = '\x00'
        endDate = '?'
        endDate = "2021-05-28 23:59:59"
        self.reqHistoricalNews(10003, 265598, "BRFG+BRFUPDN+DJNL", "2022-06-28 23:59:59", endDate, '300', [])
     #   self.reqNewsArticle(self.nextValidOrderId, "BZ", "BZ$1387d258", [])



    def stop(self):
        self.done = True
        self.disconnect()


def main():
    try:
        app = TestApp()
        app.connect('192.168.43.223', 7497, clientId=0)
        print(f'{app.serverVersion()} --- {app.twsConnectionTime().decode()}')
        print(f'ibapi version: ', ibapi.__version__)
        Timer(5, app.stop).start()
        app.run()
    except Exception as err:
        print(err)

if __name__ == '__main__':
    main()
