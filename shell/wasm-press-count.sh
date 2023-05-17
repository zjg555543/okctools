# set -x

res=$(okbchaincli keys add temp -y)
res=$(okbchaincli keys show temp)
# echo $res
new_address=$(echo "$res" | jq '.eth_address')
echo $new_address

press_paras="{"add":{"spender":[" + 


# res=$(okbchaincli tx wasm store /Users/oker/workspace/github/wasm-test/contract/iterator-press/artifacts/iterator_press.wasm --fees 0.01okb --from captain --gas=2000000 -b block -y)

# code_id=$(echo "$res" | jq '.logs[0].events[1].attributes[0].value' | sed 's/\"//g')

# res=$(okbchaincli tx wasm instantiate "$code_id" '{}' --label test1 --admin 0xbbE4733d85bc2b90682147779DA49caB38C0aA1F --fees 0.001okb --from captain -b block -y)

# contractAddr_0x=$(echo "$res" | jq '.logs[0].events[0].attributes[0].value' | sed 's/\"//g')

# okbchaincli tx wasm execute $contractAddr_0x '{"add":{"spender":["0x83D83497431C2D3FEab296a9fba4e5FaDD2f7eD0","0x4C12e733e58819A1d3520f1E7aDCc614Ca20De64","0x2Bd4AF0C1D0c2930fEE852D07bB9dE87D8C07044"]}}' --fees 0.001okb --from captain -b block -y

# okbchaincli tx wasm execute $contractAddr_0x '{"press":{"ascending":true}}' --fees 0.001okb --from captain -b block -y

# echo '
# {
#   "name": "temp",
#   "type": "local",
#   "address": "ex1a0vwcag9zvnvqew6u29wslzum6e6vrx6nf86ts",
#   "eth_address": "0xEBD8eC75051326c065daE28Ae87c5CDeB3A60CDa",
#   "oper_address": "exvaloper1a0vwcag9zvnvqew6u29wslzum6e6vrx69wd702",
#   "pubkey": "expub17weu6qepqdhwxvzma8drxyvk7527fdwv2wdvxqhs8t0xlqaz24psfv6tplxlqw3cn34",
#   "mnemonic": "ignore stick garment tooth simple clap cave object write art still hybrid"
# }' | jq '.eth_address'