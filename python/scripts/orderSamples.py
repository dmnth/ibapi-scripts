#! /usr/bin/env python3

from ibapi.order import Order

def trailStopLimit(action):

    order = Order()

    order.action = action 
    order.orderType = "TRAIL LIMIT"
    order.totalQuantity = 1
    order.trailStopPrice = 10.25 
    order.lmtPriceOffset = 0.25 
    order.auxPrice = 10 
    order.transmit = True

    return order
