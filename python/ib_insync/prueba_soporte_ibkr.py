#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 20:03:15 2023

@author: alejandrovicentemoreno
"""


import os
#os.environ['KMP_WARNINGS'] = 'off'
from datetime import datetime, time
from ib_insync import *
import pandas as pd
from configparser import ConfigParser
import pytz
config = ConfigParser()
import nest_asyncio
nest_asyncio.apply()
import numpy as np  


tickers = ['SPY']
expiration_date = '20230929'
exp_date_format = '2023-09-29'
today_format = '2023-09-26 18:00'

for ticker in tickers:
 try:
    print(ticker)
    from datetime import datetime, time
    def in_between(now, start=time(9,30), end=time(16)):
        if start <= now < end:
            return 1
        else:
            return 2
    
    
    timeZ_Ny = pytz.timezone('America/New_York')
    data_type = in_between(datetime.now(timeZ_Ny).time())
    
    
    #port = int(config.get('main', 'ibkr_port'))
    
    # TWs 7497, IBGW 4001
    ib = IB().connect('127.0.0.1', 7497, 69)
    
    def get_chain(ticker,exp_list):
        exps = {}
        df = pd.DataFrame(columns=['strike','kind','close','last'])
        ib.reqMarketDataType(2) #Donde el 2 en realidad debería ir in_between, pero tengo demasiada prisa como para solucionar el problema ahora
        for i in exp_list:
            cds = ib.reqContractDetails(Option(ticker, i, exchange='SMART'))
            # print(cds)
            options = [cd.contract for cd in cds]
            # print(options)
            l = []
            for x in options:
                # print(x)
                contract = Option(ticker, i, x.strike, x.right, "SMART", currency="USD")
                # print(contract)
                snapshot = ib.reqMktData(contract, "", True, False)
                l.append([x.strike,x.right,snapshot])
                # print(snapshot)
    
            while util.isNan(snapshot.bid):
                ib.sleep()
            for ii in l:
             try:
                df = df.append({'strike':ii[0],'kind':ii[1],'close':ii[2].close,'last':ii[2].last,'bid':ii[2].bid,'ask':ii[2].ask,'mid':(ii[2].bid+ii[2].ask)/2,'volume':ii[2].volume,'ticker':ticker,'expiration_date':exp_date_format,'quote_date':today_format, 'impliedVol':ii[2].askGreeks.impliedVol, 'delta':ii[2].askGreeks.delta, 'gamma':ii[2].askGreeks.gamma, 'vega':ii[2].askGreeks.vega, 'theta':ii[2].askGreeks.theta, 'underlying':ii[2].askGreeks.undPrice},ignore_index=True)
                exps[i] = df
             except:
                 continue
        return exps
    
    
    t0 = datetime.now()
    options_chain = get_chain(ticker,[expiration_date])
    
    print(datetime.now()-t0)
    
    options_data_df = list(options_chain.values())[0]
    #options_data_df=options_data_df.dropna()
    #options_data_df = options_data_df[(options_data_df.ask != -1.0) & (options_data_df.bid != -1.0)]
    print(options_data_df)
    
    ib.disconnect()
    
    path= '/Users/alejandrovicentemoreno/Desktop/Desktop/TFM/prueba_spy.csv'
    options_data_df.to_csv(path, index=True, mode="a", header=not os.path.isfile(path),sep=',', decimal=',')
   

 except:
     ib.disconnect()
     continue
 
account_number = 'U7695471' #Real U7695471 // Demo DU3196895

def l_call(K,price,ticker,fecha,takeprofit,stoploss):
    spy_call = Option(ticker, fecha, K, 'C', 'SMART')
    ib.qualifyContracts(spy_call)
    
    
    #Place a straddle order
    order = ib.bracketOrder("BUY", 1, limitPrice = np.round(price,2), takeProfitPrice = takeprofit + np.round(price,2) , stopLossPrice = np.round(price,2) - stoploss, tif="GTC", account = account_number) ##algos only DAY         
    trade = ib.placeOrder(spy_call, order[0])   
    takeprofit = ib.placeOrder(spy_call, order[1])     
    stoploss = ib.placeOrder(spy_call, order[2])     

    return trade, takeprofit, stoploss

#data = pd.read_csv(r'/Users/alejandrovicentemoreno/Desktop/Desktop/TFM/prueba_spy.csv')


#K = data['strike'][10]
#precio =  float(data['ask'][10].replace(',', '.'))*0.5

ib = IB()
ib.connect('192.168.43.222', 7496, clientId=21)
   
#stoploss = 6
#takeprofit = 6

#l_call(K, (precio), ticker, expiration_date,takeprofit,stoploss)

time.sleep(5)
    
#Disconnect
ib.disconnect()
