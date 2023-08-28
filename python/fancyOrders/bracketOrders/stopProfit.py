#! /usr/bin/env python3

from ibapi.order import Order
from ibapi.utils import Decimal

def stopProfit(parentOrderId:int, action:str, quantity:Decimal,
                 limitPrice:float, takeProfitLimitPrice:float,
                 stopLossPrice:float):

     takeProfit = Order()
     takeProfit.orderId =parentOrderId  + 1
     takeProfit.action = "SELL" if action == "BUY" else "BUY"
     takeProfit.orderType = "LMT"
     takeProfit.totalQuantity = quantity
     takeProfit.lmtPrice = takeProfitLimitPrice
     takeProfit.transmit = False

     stopLoss = Order()
     stopLoss.orderId = parentOrderId + 2
     stopLoss.action = "SELL" if action == "BUY" else "BUY"
     stopLoss.orderType = "STP"
     stopLoss.auxPrice = stopLossPrice
     stopLoss.totalQuantity = quantity
     stopLoss.transmit = True

     modProfitStop= [takeProfit, stopLoss]
     return modProfitStop 

stopProfit = stopProfit(265598, "SELL", 1,0.1, 0.1, 0.2)
