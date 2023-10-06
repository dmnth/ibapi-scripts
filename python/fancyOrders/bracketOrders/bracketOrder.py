#! /usr/bin/env python3

from ibapi.order import Order
from ibapi.utils import Decimal
from ibapi.tag_value import TagValue

def bracketOrder(parentOrderId:int, action:str, quantity:Decimal,
                 limitPrice:float, takeProfitLimitPrice:float,
                 stopLossPrice:float):

     #This will be our main or "parent" order
     # Please try to attach price adjustment in perscent
     parent = Order()
     parent.orderId = parentOrderId
     parent.action = action
     parent.orderType = "MKT"
     parent.totalQuantity = quantity
#     parent.lmtPrice = limitPrice
     #The parent and children orders will need this attribute set to False to prevent accidental executions.
     #The LAST CHILD will have it set to True,
     parent.transmit = False

     takeProfit = Order()
     takeProfit.orderId = parent.orderId + 1
     takeProfit.action = "SELL" if action == "BUY" else "BUY"
     takeProfit.orderType = "LMT"
     takeProfit.totalQuantity = quantity
     takeProfit.lmtPrice = takeProfitLimitPrice
     takeProfit.parentId = parentOrderId
#     takeProfit.trailingPercent = 10
#     takeProfit.percentOffset = 12
     takeProfit.transmit = False

     stopLoss = Order()
     stopLoss.orderId = parent.orderId + 2
     stopLoss.action = "SELL" if action == "BUY" else "BUY"
     stopLoss.orderType = "STP"
     #Stop trigger price
     stopLoss.auxPrice = stopLossPrice
     stopLoss.totalQuantity = quantity
     stopLoss.parentId = parentOrderId
     #In this case, the low side order will be the last child being sent. Therefore, it needs to set this attribute to True
     #to activate all its predecessors
#     stopLoss.trailingPercent = 10
#     stopLoss.percentOffset = 12
     stopLoss.algoStrategy = "Adaptive" 
     stopLoss.algoParams = []
     stopLoss.algoParams.append(TagValue("adaptivePriority", "Patient"))
     stopLoss.transmit = True

     bracketOrder = [parent, takeProfit, stopLoss]
     return bracketOrder

def stopProfit(parentOrderId:int, action:str, quantity:Decimal,
                 limitPrice:float, takeProfitLimitPrice:float,
                 stopLossPrice:float):

     takeProfit = Order()
     takeProfit.orderId = parentOrderId + 1
     takeProfit.action = "SELL" if action == "BUY" else "BUY"
     takeProfit.orderType = "LMT"
     takeProfit.totalQuantity = quantity
     takeProfit.lmtPrice = takeProfitLimitPrice
     takeProfit.transmit = False

     stopLoss = Order()
     stopLoss.orderId = parentOrderId + 2
     stopLoss.action = "SELL" if action == "BUY" else "BUY"
     stopLoss.orderType = "STP"
     stopLoss.AuxPrice = stopLossPrice
     stopLoss.totalQuantity = quantity
     stopLoss.algoStrategy = "Adaptive" 
     stopLoss.algoParams = []
     stopLoss.algoParams.append(TagValue("adaptivePriority", "Patient"))
     stopLoss.transmit = True

     modProfitStop= [takeProfit, stopLoss]
     return modProfitStop 

