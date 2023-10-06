#! /usr/bin/env python2

payload0 = {
        "conid": 265598,
        "period": "w",
        "bar": "d"
        }

payloadEmpty = {
        "conid": "",
        "period": "",
        "bar": "",
        "outsideRth": ""
        }

payloadInvalid = {
        "conid": "string",
        "period": "1/0",
        "bar": -1,
        "outsideRth": "-1/0"
        }

payloadInvalid2 = {
        "conid": 1,
        "period": "1/0",
        "bar": -1,
        "outsideRth": "-1/0"
        }

payloadInvalid3 = {
        "conid": 265598,
        "period": "1/0",
        "bar": -1,
        "outsideRth": "-1/0"
        }

payloadInvalid4 = {
        "conid": "265598",
        "period": "1/0",
        "bar": -1,
        "outsideRth": "-1/0"
        }

payloadInvalid4 = {
        "conid": "265598",
        "period": "1/0",
        "bar": -1,
        "outsideRth": "-1/0"
        }

payloadErr = {
        "conid": 265598,
        "period": "w",
        }

payload1 = {
        "conid": 265598,
        "period": "1w",
        "bar": "1d"
        }

payload2 = {
        "conid": 265598,
        "period": "1d",
        "bar": "1h",
        "outsideRth": True,
        "randomKey": "value"
        }

payload3 = {
        "conid": 265598,
        "period": "1d",
        "bar": "1h",
        "outsiderRth": "true"
        }

payload4 = {
        "conid": 265598,
        "period": "1d",
        "bar": "1h",
        "outsiderRth": True 
        }


payload5 = {
        'conid': 265598,
        'period': '1d',
        'bar': '1h',
        'outsiderRth': True 
        }


payload6 = {
        }

payload7 = {
        'conid': 265598,
        'period': '1d',
        'bar': '1h'
        }


payload8 = {
        'conid': 0,
        'period': '"',
        'bar': '"'
        }

payload9 = {
        'conid': "265598\'",
        'period': "'",
        'bar': "'"
        }


payload10 = {
        'conid': "265598 or 1=1;#",
        'period': "'",
        'bar': "'"
        }

payload11 = {
        'conid': "265598\' or 1=1;--",
        'period': "'",
        'bar': "'"
        }


payload11 = {
        'conid': "0\' or 1=1;--",
        'period': "'",
        'bar': "'"
        }

payload12 = {
        'conid': "0\' || 1=1;--",
        'period': "'",
        'bar': "'"
        }

validPayload = {
        "conid": 265598,
        "period": "1w",
        "bar": "1d",
        "barType": "feeRate" # or inventory as per JIRA CPWAPI-75
        }

validPayload2 = {
        "conid": 265598,
        "period": "1w",
        "bar": "1d",
        "barType": "trades" # or inventory as per JIRA CPWAPI-75
        }

validPayload3 = {
        "conid": 265598,
        "period": "1w",
        "bar": "1d",
        "barType": "last" # or inventory as per JIRA CPWAPI-75
        }

validPayload4 = {
        "conid": 265598,
        "period": "1w",
        "bar": "1d",
        "barType": "midpoint" # or inventory as per JIRA CPWAPI-75
        }

validPayload5 = {
        "conid": 265598,
        "period": "1w",
        "bar": "1d",
        "barType": "bidask" # or inventory as per JIRA CPWAPI-75
        }

validPayload6 = {
        "conid": 265598,
        "period": "1w",
        "bar": "1d",
        "barType": "bid" # or inventory as per JIRA CPWAPI-75
        }

validPayload6 = {
        "conid": 265598,
        "period": "1w",
        "bar": "1d",
        "barType": "ask" # or inventory as per JIRA CPWAPI-75
        }
