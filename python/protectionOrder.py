#! /usr/bin/env python3

from ibapi.order import Order
from ibapi.utils import Decimal
from ibapi.tag_value import TagValue

def fillAdaptiveAlgoParams(order, priority):
    order.algoStrategy = "Adaptive"
    order.algoParams = []
    order.algoParams.append(TagValue("adaptivePriority", priority))

def BracketOrder(parentOrderId:int, action:str, quantity:Decimal,
                 limitPrice:float, takeProfitLimitPrice:float,
                 stopLossPrice:float):

     #This will be our main or "parent" order
     # Please try to attach price adjustment in perscent
     parent = Order()
     parent.orderId = parentOrderId
     parent.action = action
     parent.orderType = "LMT"
     parent.totalQuantity = quantity
     parent.lmtPrice = limitPrice
     #The parent and children orders will need this attribute set to False to prevent accidental executions.
     #The LAST CHILD will have it set to True,
     parent.transmit = False
     parent.tif = "DAY"
     fillAdaptiveAlgoParams(parent, "Normal")

     takeProfit = Order()
     takeProfit.orderId = parent.orderId + 11
     takeProfit.action = "SELL" if action == "BUY" else "BUY"
     takeProfit.orderType = "MKT"
     takeProfit.totalQuantity = quantity
     takeProfit.lmtPrice = takeProfitLimitPrice
     takeProfit.parentId = parentOrderId
     takeProfit.transmit = True 
     fillAdaptiveAlgoParams(takeProfit, "Normal")

     stopLoss = Order()
     stopLoss.orderId = parent.orderId + 12
     stopLoss.action = "SELL" if action == "BUY" else "BUY"
     stopLoss.orderType = "TRAIL"
     #Stop trigger price
     stopLoss.auxPrice = stopLossPrice
     stopLoss.totalQuantity = quantity
     stopLoss.parentId = parentOrderId
     stopLoss.tif = "DAY"
     stopLoss.transmit = True 

     bracketOrder = [parent, takeProfit, stopLoss]
     return bracketOrder

