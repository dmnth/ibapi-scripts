#! /usr/bin/env/python3

from ibapi.order import Order
from ibapi.utils import Decimal
from ibapi.tag_value import TagValue

def BracketOrder(parentOrderId:int, action:str, quantity:Decimal,
                 limitPrice:float, takeProfitLimitPrice:float,
                 stopLossPrice:float):

    print("Parent order id: ", parentOrderId)
    parent_order = Order()
    parent_order.action = "BUY"
    parent_order.orderId = parentOrderId
    parent_order.orderType = "LMT"
    parent_order.totalQuantity = 100
    parent_order.lmtPrice = 130
    parent_order.tif = "GTC"
    parent_order.transmit = False
    parent_order.algoStrategy = "Adaptive"
    parent_order.algoParams = []
    parent_order.algoParams.append(TagValue("adaptivePriority", "Normal"))

    take_profit = Order()
    take_profit.parentId= parent_order.orderId
    take_profit.orderId = parent_order.orderId + 1
    take_profit.action = "SELL"
    take_profit.orderType = "LMT"
    take_profit.totalQuantity = 100
    take_profit.lmtPrice = 135
    take_profit.transmit = False
    take_profit.algoStrategy = "Adaptive"

    stop_loss = Order()
    stop_loss.parentId= parent_order.orderId
    stop_loss.orderId = parent_order.orderId + 2
    stop_loss.action = "SELL"
    stop_loss.orderType = "STP"
    stop_loss.totalQuantity = 100
    stop_loss.auxPrice = 125
    stop_loss.transmit = False
    stop_loss.algoStrategy = "Adaptive"

    closing = Order()
    closing.orderId = parent_order.orderId + 3
    closing.action = "SELL"
    closing.orderType = "MKT"
    closing.totalQuantity = 12
    closing.parentId = parent_order.orderId
    closing.tif = "GTC"
    closing.transmit = True

    bracket_order = [parent_order, take_profit, stop_loss, closing] 

    return bracket_order
