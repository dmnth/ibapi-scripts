#! /usr/bin/env python3

from ibapi.contract import Contract

class TestContracts():

    def __init__(self):
        self.param = None

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

    def porsche_contract():

       contract = Contract()
       contract.secType = "STK"
       contract.exchange = "SMART"
       contract.currency = "EUR"
       contract.symbol = "P911"

       return contract

    def create_mes_contract():

       contract = Contract()
       contract.secType = "FUT"
       contract.conId = 533620623
       contract.symbol = "MES"
       contract.lastTradeDateOrContractMonth = "20230317"
       contract.multiplier = 5
       contract.exchange = "CME"
       contract.currency = "USD"
       contract.localSymbol = "MESH3"
       contract.tradingClass = "MES"

       return contract

