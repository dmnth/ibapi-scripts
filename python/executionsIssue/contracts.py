#! /usr/bin/env python3

from ibapi.contract import Contract
from ibapi.contract import ComboLeg


class CustomContracts():

    def __init__(self):
        self.args = ""

    def silverSpread(self):

        contract = Contract()

        contract.symbol = "SI"
        contract.secType = "BAG"
        contract.currency = "USD"
        contract.exchange = "COMEX"

        leg1 = ComboLeg()
        leg1.conId = 645364413 
        leg1.ratio = 1
        leg1.action = "BUY"
        leg1.exchange = "COMEX"

        leg2 = ComboLeg()
        leg2.conId = 651096968 
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
        leg2.conId = 529413273 
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
        leg1.conId = 3351154381 
        leg1.ratio = 1
        leg1.action = "BUY"
        leg1.exchange = "COMEX"

        leg2 = ComboLeg()
        leg2.conId = 639787335 
        leg2.ratio = 1
        leg2.action = "BUY"
        leg2.exchange = "COMEX"

        contract.comboLegs = []
        contract.comboLegs.append(leg1)
        contract.comboLegs.append(leg2)

        return contract

