import numpy as np
import pandas as pd

import datetime as dt
from datetime import datetime
from datetime import timedelta

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import threading
import time

d_date_last = '20221214'

tickers = ['LIN']
d_datetime_last_ib = d_date_last + ' 00:00:01 US/Eastern'
#tickers = ['INDU']
#d_datetime_last_ib = d_date_last + ' 00:00:01 US/Central'

Duration = '1 D'
#tickers = d_symbols
d_orig_location_model_temp = "Data-Orig-IB-API/Data-For-Model/Temp/"

class TradeApp(EWrapper, EClient):
    def __init__(self):
    EClient.__init__(self, self)
    self.data = {} #Initialize variable to store candle

    def historicalData(self, reqId, bar):
        if reqId not in self.data:
            self.data[reqId] = [{"DateTime":bar.date,"Open":bar.open,"High":bar.high,"Low":bar.low,"Close":bar.close,"Volume":bar.volume}]
        else:
            self.data[reqId].append({"DateTime":bar.date,"Open":bar.open,"High":bar.high,"Low":bar.low,"Close":bar.close,"Volume":bar.volume})

    def historicalDataEnd(self, reqId, start, end):
        super().historicalDataEnd(reqId, start, end)
        event.set()

    def usTechStk(symbol,sec_type="STK",currency="USD",exchange="ISLAND"):
        #def usTechStk(symbol,sec_type="IND",currency="USD",exchange="CME"):
        contract = Contract()
        contract.symbol = symbol
        contract.secType = sec_type
        contract.currency = currency
        contract.exchange = exchange
        return contract

    def histData(req_num,contract,endDateTime1, duration,candle_size):
        """Extract historical data"""
        app.reqHistoricalData(reqId=req_num,
        contract=contract,
        endDateTime=endDateTime1,
        durationStr=duration,#'5 D',
        barSizeSetting=candle_size,#'1 min',
        #whatToShow='ADJUSTED_LAST',#'TRADES',
        whatToShow='TRADES',
        useRTH=0,
        formatDate=1,#2,
        keepUpToDate=0,#False,
        chartOptions=[])

    def websocket_con():
        app.run()

app = TradeApp()
#app.connect(host='127.0.0.1', port=7496, clientId=123)
app.connect(host='127.0.0.1', port=7497, clientId=123)
con_thread = threading.Thread(target=websocket_con, daemon=True)
con_thread.start()
time.sleep(1)

event = threading.Event()

isymbol = 0
print('isymbol of',len(tickers),'=', end = ' ')
for ticker in tickers:
    isymbol += 1
    if ticker != tickers[-1]:
        print(isymbol,'-',ticker, end = ', ')
    else:
        print(isymbol,'-',ticker)
        
    event.clear()
    histData(tickers.index(ticker),usTechStk(ticker),d_datetime_last_ib,Duration,'1 min')
    event.wait()
    df = pd.DataFrame(app.data[tickers.index(ticker)])
    df.to_csv(d_orig_location_model_temp + ticker + '.csv', index=False)

app.disconnect()
