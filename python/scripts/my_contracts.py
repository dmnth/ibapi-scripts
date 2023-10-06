#! /usr/bin/env python3

class CustomContracts():

    def __init__(self):
        self.args = ""

    def forex_pair(self):

        contract = Contract()
        contract.symbol = "EUR"
        contract.exchange = "IDEALPRO"
        contract.secType = "CASH"
        contract.currency = "USD"

        return contract

    def bmw_contract(self):

        contract = Contract()
        contract.symbol = 'BMW'
        contract.exchange = 'SMART'
        contract.currency = 'EUR'
        contract.secType = "STK"
        
        return contract

    def aapl_contract(self):

        contract = Contract()
        contract.symbol = "AAPL"
        contract.exchange = "SMART"
        contract.currency = "USD"
        contract.secType = "STK"

        return contract1

