#! /usr/bin/env python3

# So reqSecDefOptParams returns different amount of expiries and 
# strikes, what if strikes < expiries and vise versa

expirations = []
strikes = [1, 2, 3, 4, 3, 4, 5, 6]
"""
for right in ["C", "P"]:
    for expiration in expirations:
        for strike in strikes:
            print(right, expiration, strike)
"""

# Black magic 
contracts = [(right, expiration, strike) for right in ["C", "P"] for expiration \
        in expirations for strike in strikes]

def print_contracts(*contracts):
    for el in contracts:
        print(el)

print_contracts(*contracts)
