#! /usr/bin/env python3

from ibapi.order import Order 
from ibapi.order_condition import *
from datetime import datetime
from datetime import time

def conditionalBracketOrder(nextValidId):

    sellOrder = Order()
    sellOrder.action = "SELL"
    sellOrder.orderType = "LMT"
    sellOrder.lmtPrice = 12300
    sellOrder.totalQuantity = 10
    sellOrder.orderId = nextValidId

    # Time condition
#    tc = Create(OrderCondition.Time)
#    tc.isMore = True
#    tc.time = datetime.combine(datetime.now().date(), time(15, 0, 0))
#    tc.isConjunctionConnection = "OR"
#    sellOrder.conditions.append(tc)

    pc = Create(OrderCondition.Price)
    pc.isMore = True
    pc.price = 0 
    pc.exchange = "SMART"
    pc.conId = 265598 
    pc.triggerMethod = 0 
    sellOrder.conditions.append(pc)

    return sellOrder
