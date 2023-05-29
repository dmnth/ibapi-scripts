#! /usr/bin/env python3

from restRequests import checkAuthStatus, getAccounts, placeSingleOrder, getPortfolioPositionsByPage,\
        callPortfolioAccounts, getPortfolioPositions


def positionUpdate():
    checkAuthStatus()
    callPortfolioAccounts()
    placeSingleOrder("TSLA")
    accId = getAccounts()[0]
    getPortfolioPositionsByPage(accId, 100)
#    getPortfolioPositions(accId)
    return

def main():
    positionUpdate()

if __name__ == "__main__":
    main()

