#! /usr/bin/env python3

import subprocess
import json
from restRequests import getAccounts

def readOrder():
    txtFile = open('response.txt', 'r').readlines()
    return txtFile

def generateCurlCommand(orderDetails):
    orderDetails = orderDetails.replace("'", '"')
    
    print(orderDetails)
    jsonData = json.dumps(orderDetails).replace('False', 'false')
    print("JSON: ", jsonData)
    accountID = getAccounts()
    payload = f"curl -v --insecure -X POST https://localhost:5000/v1/api/iserver/account/{accountID}/orders -H 'accept: application/json' -H 'Content-Type: application/json'"
    data = f" -d {{'orders':[{orderDetails}]}}".replace("'", '"')
    payload = payload + data
    return payload

def sendCurlCommad(payload):
    result = subprocess.check_output(payload, shell=True)
    print(result)
    return

def main():

    orderDetails = readOrder()[-1]
    payload = generateCurlCommand(orderDetails)
    print(payload)
#    sendCurlCommad(payload)

if __name__ == "__main__":
    main()

