#! /usr/bin/env python3

import ibapi
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.contract import (Contract, ContractDetails)
from ibapi.account_summary_tags import *
from flask import Flask
from sqlalchemy import create_engine, text 

class dB():

    def __init__(self):
        self.engine = None 

    def createEngine(self):
        self.engine = create_engine("sqlite:///myDb.db:", echo=True)
        
    def createAcccountsTable(self):
        sqlStatement = text("CREATE TABLE IF NOT EXISTS Accounts (AccountId varchar(255), Value int, Currency varchar(255));")
        conn = self.engine.connect()
        conn.execute(sqlStatement)
        conn.commit()
        conn.close()
    
    def insertAccountData(self, accid, val, curr):
        sql = text(f"INSERT INTO Accounts (AccountId, Value, Currency) VALUES ('{accid}', {val}, '{curr}');")
        conn = self.engine.connect()
        conn.execute(sql)
        conn.commit()
        conn.close()
    
    def queryAccountsInfo(self, accId):
        sql = text(f"SELECT value, currency FROM Accounts WHERE AccountId='{accId}'")
        conn = self.engine.connect()
        result = conn.execute(sql)
        print("Result returned from DB: ", result.all())

class TestApp(EWrapper, EClient, dB):

    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, self)
        dB.__init__(self)
        self.dataframe = {}
        self.contract = None

    # WRAPPERS HERE
    def nextValidId(self, orderId):
        super().nextValidId(orderId)
        #logging.debug(f"Next valid ID is set to {orderId}")
        self.nextValidOrderId = orderId
        # As soon as next valid id is received it is safe to send requests
        self.start()

    def accountSummary(self, reqId: int, account: str, tag: str, value: str,
                       currency: str):
        super().accountSummary(reqId, account, tag, value, currency)
#        print("AccountSummary. ReqId:", reqId, "Account:", account,
#              "Tag: ", tag, "Value:", value, "Currency:", currency)
        self.dataframe['account'] = account
        self.dataframe['value'] = value
        self.dataframe['currency'] = currency

    def accountSummaryEnd(self, reqId: int):
        super().accountSummaryEnd(reqId)
        print("AccountSummaryEnd. ReqId:", reqId)
        print(self.createEngine())
        self.createAcccountsTable()
        self.insertAccountData(self.dataframe['account'],
                self.dataframe['value'], self.dataframe['currency'])
        self.queryAccountsInfo(self.dataframe['account'])
        print(self.dataframe)

    # Place requests here
    def start(self):
        self.reqAccountSummary(self.nextValidOrderId, "All", AccountSummaryTags.AllTags) 

    def stop(self):
        self.done = True
        self.disconnect()

def main():
    try:
        app = TestApp()
        app.connect('127.0.0.1', 7496, clientId=1)
        app.run()
    except Exception as err:
        print(err)

if __name__ == '__main__':
    main()
