#! /usr/bin/env python

from ibapi.order import Order
from ibapi.contract import Contract

def create_order_pair():
    order = Order()
    order.action = "SELL"
    order.orderType = "LMT"
    order.lmtPrice = 11900
    order.totalQuantity = 1
    order.orderRef = "twap_test"


    contract = Contract()
    contract.secType = "FUT"
    contract.conId = 533620686
    contract.lastTradeDateOrContractMonth = "20230317"
    contract.symbol = "NQ"
    contract.currency = "USD"
    contract.exchange = "CME"
    contract.multiplier = 20

    return {"order": order, "contract": contract}

pair = create_order_pair()
