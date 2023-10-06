#! /usr/bin/env python3

from ibapi.order import Order
from ibapi.contract import Contract
from ibapi.tag_value import TagValue

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

def fill_twap_params(baseOrder, strategyType, startTime,
        endTime, allowPastEndTime):
    baseOrder.algoStrategy = "Twap"
    baseOrder.algoParams = []
    baseOrder.algoParams.append(TagValue("startTime", startTime))
    baseOrder.algoParams.append(TagValue("endTime", endTime))
    baseOrder.algoParams.append(TagValue("allowPastEndTime", allowPastEndTime))

pair = create_order_pair()
fill_twap_params(pair["order"], "Marketable", "16:03 SGT", "17:20 SGT", True) 
