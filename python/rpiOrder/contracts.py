#! /usr/bin/env python3

from ibapi.contract import Contract
from ibapi.contract import ComboLeg


class CustomContracts():

    def __init__(self):
        self.args = ""

    def avgrContrac(self):

        contract = Contract()

        contract.exchange = "SMART" 
        contract.primaryExchange = "NASDAQ"
        contract.symbol = "AVGR"
        contract.currency = "USD"
        contract.secType = "STK"

        return contract

    def alibabaContract(self):

        contract = Contract()

        contract.exchange = "NYSE"
        contract.symbol = "BABA"
        contract.currency = "USD"
        contract.secType = "STK"

        return contract

    def esFutContract(self):

        contract = Contract()

        contract.exchange = "CME"
        contract.currency = "USD"
        contract.symbol = "ESM4"
        contract.lastTradeDateOrContractMonth = "20230616"
        contract.localSymbol = "ESM4"
        contract.conId = 551601561 

        return contract

    def spyStkContract(self):

        contract = Contract()

        contract.exchange = "Smart"
        contract.symbol = "SPY"
        contract.secType = "STK"
        contract.currency = "USD"

        return contract

    def crudeOilFut(self):

        contract = Contract()

        contract.secType = "CONTFUT"
        contract.symbol = "QMV3"
        contract.exchange = "NYMEX"
        contract.conId = 296349619
        contract.currency = "USD"

        return contract

    def goldContFut(self):

        contract = Contract()

        contract.symbol = '1690600A0'
        contract.exchange = "OSE.JPN"
        contract.currency = "JPY"
        contract.conId = 639440272

        return contract

    def mesContract(self):

        contract = Contract()

        contract.symbol = "MES"
        contract.secType = "CONTFUT"
        contract.currency = "USD"
        contract.exchange = "CME"

        return contract

    def spxStock(self):

        contract = Contract()

        contract.symbol = "SPX"
        contract.exchange = "SMART"
        contract.secType = "STK"
        contract.currency = "USD"

        return contract

    def amdCadContract(self):

        contract = Contract()

        contract.symbol = "FMCC"
        contract.secType = "STK"
        contract.exchange = "OTCLNKECN"
        contract.currency = "USD"

        return contract

    def spyFutContract(self):

        contract = Contract()

        contract.symbol = "SPY"
        contract.exchange = "ASX"
        contract.secType = "FUT"
        contract.lastTradeDateOrContractMonth = "20230921"
        contract.multiplier = 25
        contract.currency = "AUD"

        return contract

    def aaplOptions(self):

        contract = Contract()

        contract.symbol = "AAPL"
        contract.conId = 606333065
        contract.secType = "OPT"
        contract.currency = "USD"
        contract.exchange = "SMART"
        contract.strike = 190
        contract.right = "C"
        contract.multiplier = 100
        contract.lastTradeDateOrContractMonth = "20230818"
        contract.tradingClass = "AAPL"
        
        return contract

    def vixFuturesSpread(self):

        contract = Contract()

        contract.symbol = "VIX"
        contract.secType = "BAG"
        contract.currency = "USD"
        contract.exchange = "CFE"

        leg1 = ComboLeg()
        leg1.conId = 598829973 
        leg1.ratio = 1
        leg1.action = "BUY"
        leg1.exchange = "CFE"

        leg2 = ComboLeg()
        leg2.conId = 605219372 
        leg2.ratio = 1
        leg2.action = "SELL"
        leg2.exchange = "CFE"

        contract.comboLegs = []
        contract.comboLegs.append(leg1)
        contract.comboLegs.append(leg2)

        return contract


    def hkStockIndex(self):

        contract = Contract()

        contract.symbol = "HSIN3"
        contract.secType = "FUT"
        contract.lastTradeDateOrContractMonth = "202307"
        contract.currency = "HKD"
        contract.exchange = "HKFE"
        contract.multiplier = 50
        contract.tradingClass = "HSI"

        return contract

    def goldContract(self):

        contract = Contract()

        contract.symbol = "GC"
        contract.conId = 639787335
        contract.secType = "FUT"
        contract.exchange = "COMEX"
        contract.currency = "USD"

        return contract

    def silverContract(self):

        contract = Contract()

        contract.symbol = "SI"
        contract.conId = 523408698 
        contract.secType = "FUT"
        contract.exchange = "COMEX"
        contract.currency = "USD"

        return contract

    def silverSpread(self):

        contract = Contract()

        contract.symbol = "SI"
        contract.secType = "BAG"
        contract.currency = "USD"
        contract.exchange = "COMEX"

        leg1 = ComboLeg()
        leg1.conId = 523408698
        leg1.ratio = 1
        leg1.action = "BUY"
        leg1.exchange = "COMEX"

        leg2 = ComboLeg()
        leg2.conId = 633994090 
        leg2.ratio = 1
        leg2.action = "BUY"
        leg2.exchange = "COMEX"

        contract.comboLegs = []
        contract.comboLegs.append(leg1)
        contract.comboLegs.append(leg2)

        return contract

    def goldSpread(self):

        contract = Contract()

        contract.symbol = "GC"
        contract.secType = "BAG"
        contract.currency = "USD"
        contract.exchange = "COMEX"

        leg1 = ComboLeg()
        leg1.conId = 639787335 
        leg1.ratio = 1
        leg1.action = "BUY"
        leg1.exchange = "COMEX"

        leg2 = ComboLeg()
        leg2.conId = 517660678 
        leg2.ratio = 1
        leg2.action = "BUY"
        leg2.exchange = "COMEX"

        contract.comboLegs = []
        contract.comboLegs.append(leg1)
        contract.comboLegs.append(leg2)

        return contract

    def copperSpread(self):

        contract = Contract()

        contract.symbol = "HG"
        contract.secType = "BAG"
        contract.currency = "USD"
        contract.exchange = "COMEX"

        leg1 = ComboLeg()
        leg1.conId = 511505493 
        leg1.ratio = 1
        leg1.action = "BUY"
        leg1.exchange = "COMEX"

        leg2 = ComboLeg()
        leg2.conId = 335154381 
        leg2.ratio = 1
        leg2.action = "BUY"
        leg2.exchange = "COMEX"

        contract.comboLegs = []
        contract.comboLegs.append(leg1)
        contract.comboLegs.append(leg2)

        return contract


    def espContract(self):

        contract = Contract()

        contract.symbol = "ES"
        contract.secType = "FUT"
        contract.lastTradeDateOrContractMonth = "20230915"
        contract.exchange = "QBALGO"
        contract.currency = "USD"
        contract.multiplier = 50
        contract.localSymbol = "ESU3"

        return contract

    def contFutContract(self):

        contract = Contract()

        contract.symbol = "GBL"
        contract.secType = "CONTFUT"
        contract.exchange = "EUREX"
        
        return contract

    def audUSDcontract(self):
        
        contract = Contract()

        contract.symbol = "AUD"
        contract.secType = "CASH"
        contract.currency = "USD"
        contract.exchange = "IDEALPRO"

        return contract

    def bagContract(self):

        contract = Contract()

        contract.symbol = "SPX"
        contract.secType = "BAG"
        contract.exchange = "SMART"
        contract.currency = "USD"

        leg1 = ComboLeg()
        leg1.conId =634358014 
        leg1.ratio = 1
        leg1.side = 2

        leg2 = ComboLeg()
        leg2.conId = 635133675 
        leg2.ratio = 2
        leg2.side = 1

        contract.comboLegs = []
        contract.comboLegs.append(leg1)
        contract.comboLegs.append(leg2)

        return contract

    def mbcnContract(self):

        contract = Contract()
        contract.symbol = "MBCN"
        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.currency = "USD"

        return contract

    def metContract(self):
        contract = Contract()
        contract.conId = 570162771
        contract.symbol = "METM3"
        contract.exchange = "CME"
        contract.secType = "FUT"
        contract.lastTradeDateOrContractMonth = "20230623"
        contract.multiplier = 0.1


        return contract

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

    def comboContract(self):

        contract = Contract()




if __name__ == "__main__":
    contracts = CustomContracts()
