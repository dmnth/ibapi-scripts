#! /usr/bin/env python3

from ibapi.order import Order


def createTrailingStopHedge(parentOrderId):

    mktOrder = Order()
    mktOrder.orderType = "MKT"
    mktOrder.action = "BUY"
    mktOrder.totalQuantity = 1
    mktOrder.orderId = parentOrderId
    mktOrder.transmit = True

    trailingStop = Order() 
    trailingStop.orderType = "TRAIL"
    trailingStop.action = "SELL" 
    trailingStop.totalQuantity = 1
    trailingStop.trailingPercent = 0.2 
    trailingStop.trailStopPrice = 1
    trailingStop.parentId = order.parentId
    trailingStop.transmit = False

    return [mktOrder, trailingStop]

