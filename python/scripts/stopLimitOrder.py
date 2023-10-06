#! /usr/bin/env python3

from ibapi.order import Order

def stopLimitOrder(parentID, action, quantity, 
        limitPrice, stopPrice, trailPercent):

    limitOrder = Order()
    limitOrder.orderType = "LMT"
    limitOrder.orderId = parentID
    limitOrder.action = action
    limitOrder.totalQuantity = quantity
    limitOrder.lmtPrice = limitPrice

    stopOrder = Order()
    stopOrder.orderType = "TRAIL"
    stopOrder.orderId = parentID + 1
    stopOrder.action = "SELL" if action == "BUY" else "BUY"
    stopOrder.trailStopPrice = stopPrice
    stopOrder.totalQuantity = quantity
    stopOrder.trailingPercent = trailPercent 
    stopOrder.parentId = parentID

    stopLimitOrder = [limitOrder, stopOrder]

    return stopLimitOrder

