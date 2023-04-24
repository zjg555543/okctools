#!/bin/bash
curl "http://127.0.0.1:8545/v1/wasm/code"
echo

curl "http://127.0.0.1:8545/v1/wasm/code/1/contracts"
echo

curl "http://127.0.0.1:8545/v1/wasm/code/1"
echo

curl "http://127.0.0.1:8545/v1/wasm/contract/0x5A8D648DEE57b2fc90D98DC17fa887159b69638b"
echo

curl "http://127.0.0.1:8545/v1/wasm/contract/0x5A8D648DEE57b2fc90D98DC17fa887159b69638b/history"
echo

curl "http://127.0.0.1:8545/v1/wasm/contract/0x5A8D648DEE57b2fc90D98DC17fa887159b69638b/state"
echo

curl "http://127.0.0.1:8545/v1/wasm/contract/0x5A8D648DEE57b2fc90D98DC17fa887159b69638b/smart/eyJiYWxhbmNlIjp7ImFkZHJlc3MiOiIweGJiRTQ3MzNkODViYzJiOTA2ODIxNDc3NzlEQTQ5Y2FCMzhDMGFBMUYifX0KCg==?encoding=base64"
echo

curl "http://127.0.0.1:8545/v1/wasm/contract/0x5A8D648DEE57b2fc90D98DC17fa887159b69638b/raw/636F6E74726163745F696E666F?encoding=hex"
echo

curl --request POST "http://127.0.0.1:8545/v1/wasm/contract/0x5A8D648DEE57b2fc90D98DC17fa887159b69638b" -d \
'{
    "base_req":{
        "from":"0xbbE4733d85bc2b90682147779DA49caB38C0aA1F",
        "memo":"",
        "chain_id":"exchain-67",
        "account_number":"0",
        "sequence":"1",
        "fees":[
            {
                "denom":"okt",
                "amount":"1.000000000000000000"
            }
        ],
        "gas":"30000000",
        "gas_adjustment":"1",
        "simulate":true
    },
    "exec_msg":"eyJ0cmFuc2ZlciI6eyJhbW91bnQiOiIxMDAiLCJyZWNpcGllbnQiOiIweDJCZDRBRjBDMUQwYzI5MzBmRUU4NTJEMDdiQjlkRTg3RDhDMDcwNDQifX0KCg==",
    "coins":[
        {
            "denom":"okt",
            "amount":"1.000000000000000000"
        }
    ]
}'
echo
