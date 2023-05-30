#! /usr/bin/env python3


class CustomContracts():

    def __init__(self):
        self.args = ""

    def xauusd_contract(self):

        contract = Contract()

        contract.symbol = "XAUUSD"
        contract.secType = "CFD"
        contract.exchange = "SMART"
        contract.currency = "USD"

        return contract

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

    def ndx_nasdaq_contract(self):

        contract = Contract()
        contract.symbol = "NDX"
        contract.secType = "STK"
        contract.exchange = "VALUE"
        contract.currency = "CAD"

        return contract

    def ndx_idx_nasdaq(self):

        contract = Contract()
        contract.symbol = "NDX"
        contract.secType = "IND"
        contract.exchange = "NASDAQ"
        contract.currency = "USD"

        return contract

    def cnh_contract(self):
        contract = Contract()
        contract.symbol = "CNH"
        contract.lastTradeDateOrContractMonth = "20230416"
        contract.secType = "FUT"
        contract.multiplier = 100000
        contract.exchange = "CME"
        contract.currency = "CNH"
        contract.localSymbol = "CNHJ3"
        return contract

    def spy_contract(self):
        contract = Contract()
        contract.symbol = "SPY"
        contract.secType = "OPT"
        contract.exchange = "SMART"
        contract.lastTradeDateOrContractMonth = "20230818"
        contract.right = "CALL"
        contract.strike = "330"
        return contract

    def idx_contract(self):
        contract = Contract()
        contract.symbol = "SPX"
        contract.exchange = "CBOE"
        contract.currency = "USD"
        contract.secType = "IND"

        return contract

    def options_contract(self):
        contract = Contract()
        contract.symbol = "SPY"
        contract.secType = "OPT"
        contract.exchange = "SMART"
        contract.currency = "USD"
        contract.right = "P"
        contract.strike = 396
        contract.lastTradeDateOrContractMonth = "202303"
        return contract

    def tsla_contract(self):

        contract = Contract()

        contract.symbol = "TSLA"
        contract.secType = "STK"
        contract.exchange = "NYSE"
        contract.currency = "USD"

        return contract

    def shkntl_contract(self):

        contract = Contract()
        contract.symbol = "600519"
        contract.secType = "STK"
        contract.exchange = "SEHKNTL"
        contract.currency = "CNH"

        return contract

    def qmi_contract(self):

        contract = Contract()
        contract.symbol = "QMI"
        contract.secType = "IND"
        contract.currency = "USD"
        contract.exchange = "NASDAQ"

        return contract

    def aapl_contract(self):

        contract = Contract()
        contract.symbol = "AAPL"
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "SMART"

        return contract

    def contFutContract(self):

        contract = Contract()
        contract.symbol = "DAX"
        contract.exchange = "EUREX"
        contract.currency = "EUR"
        contract.secType = "CONTFUT"

        return contract

if __name__ == "__main__":
    contracts = CustomContracts()
