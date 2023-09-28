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

