#! /usr/bin/env python3

from ibapi.contract import Contract

def create_single_US_contract(symbol):

    contract = Contract()

    contract.symbol = symbol
    contract.exchange = "SMART"
    contract.currency = "USD"
    contract.secType = "STK"

    return contract

def create_INR_contract(symbol):

    contract = Contract()
    contract.symbol = symbol
    contract.exchange = "NSE"
    contract.currency = "INR"
    contract.secType = "STK"

    return contract

def create_list_of_contracts(symbols, function):

    contract_list = []

    for s in symbols:
        new_contract = function(s)
        contract_list.append(new_contract)

    return contract_list

def invalid_mutiplier_fut():

    contract = Contract()
#    contract.conId = 606451203
    contract.tradingClass = "TCH"
    contract.symbol = "TCHF3"
    contract.secType = "FUT"
    contract.exchange = "HKFE"
    contract.currency = "HKD"
    contract.lastTradeDateOrContractMonth = "20230130"
    # Multiplier should be set same as in TWS, integer type
    contract.multiplier = 100 

    return contract


symbols = ['BIRLACORP', 'ABCAPITAL']
contracts = create_list_of_contracts(symbols, create_INR_contract)
aapl_contract = create_single_US_contract("AAPL")
invalid_contract = invalid_mutiplier_fut()
