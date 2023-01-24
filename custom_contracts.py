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

    def create_futures_contracts():
        # Three sample contracts from 
        # beggining, end and middle of the list

       contract = Contract()

       contract.symbol = "GC"
       contract.secType = "FUT"
       contract.exchange = "COMEX"
       contract.currency = "USD"
       contract.lastTradeDateOrContractMonth = "202302"

       contract1 = Contract()

       contract1.symbol = "6B"
       contract1.secType = "FUT"
       contract1.exchange = "CME"
       contract1.currency = "USD"
       contract1.lastTradeDateOrContractMonth = "202303"

       contract2 = Contract()

       contract2.symbol = "HO"
       contract2.secType = "FUT"
       contract2.exchange = "NYMEX"
       contract2.currency = "USD"
       contract2.lastTradeDateOrContractMonth = "202303"

       return [contract, contract1, contract2]

    def create_NYMEX_mar_fut_cont(symbol):

       contract2 = Contract()

       contract2.symbol = symbol 
       contract2.secType = "FUT"
       contract2.exchange = "NYMEX"
       contract2.currency = "USD"
       contract2.lastTradeDateOrContractMonth = "202303"
        
       return contract2
        
    def create_mult_NYMEX(list_of_symbols):
        cont_list = []
        for symb in list_of_symbols:
            cont = TestContracts.create_NYMEX_mar_fut_cont(symb)
            cont_list.append(cont)

        return cont_list

    def create_CBOT_mar_cont(symbol):

       contract2 = Contract()

       contract2.symbol = symbol 
       contract2.secType = "FUT"
       contract2.exchange = "CBOT"
       contract2.currency = "USD"
       contract2.lastTradeDateOrContractMonth = "202303"
        
       return contract2
        
    def create_contract_list(list_of_symbols, exchange):
        cont_list = []
        for symb in list_of_symbols:
            if exchange == "CBOT":
                cont = TestContracts.create_CBOT_mar_cont(symb)
            if exchange == "NYMEX":
                cont = TestContracts.create_NYMEX_mar_fut_cont(symb)
            cont_list.append(cont)

        return cont_list
