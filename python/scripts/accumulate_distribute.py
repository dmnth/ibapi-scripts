#! /usr/bin/env python3

import datetime
from ibapi.contract import Contract 
from ibapi.order import Order
from AvailableAlgoParams import AvailableAlgoParams
from ibapi.tag_value import TagValue
from datetime import datetime, timedelta

def create_order_pair():
    order = Order()
    order.action = "SELL"
    order.orderType = "LMT"
    order.lmtPrice = 11900
    order.totalQuantity = 1
    order.orderRef = "twap_test"

    contract = Contract()
    contract.secType = "STK"
#    contract.conId = 533620686
#    contract.lastTradeDateOrContractMonth = "20230317"
    contract.symbol = "BAC"
    contract.currency = "USD"
    contract.exchange = "SMART"
#    contract.multiplier = 20

    time_now = datetime.now()
    startTime = time_now.strftime("%H:%M:%S")
    time_future = time_now + timedelta(minutes=15)
    endTime = time_future.strftime("%H:%M:%S")

    AvailableAlgoParams.FillAccumulateDistributeParams(order, 1, 5, False,
            False, 1, True, True, startTime, endTime)

    return {'contract': contract, 'order': order}

pair = create_order_pair()
