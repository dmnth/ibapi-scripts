#! /usr/bin/env python3

from ibapi.contract import Contract
from ibapi.contract import ComboLeg


class CustomContracts():

    def __init__(self):
        self.args = ""

    def mesContractFut(self):

        contract = Contract()

        contract.exchange = ""
        return

    def mecContractCuntFut(self):

        contract = Contract()

        contract.exchange = "CME"
        contract.currency = "USD"
        contract.secType = "CONTFUT"
        contract.symbol = "MES"

        return contract



if __name__ == "__main__":
    contracts = CustomContracts()
