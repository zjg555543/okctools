set -x

# res=$(exchaincli tx wasm store /Users/oker/workspace/github/wasm-test/scripts/../contract/testcase/artifacts/testcase.wasm --fees 0.01okt --from captain --gas=2000000 -b block -y)

# code_id=$(echo "$res" | jq '.logs[0].events[1].attributes[0].value' | sed 's/\"//g')

# res=$(exchaincli tx wasm instantiate "$code_id" '{"decimals":10,"initial_balances":[{"address":"0xbbE4733d85bc2b90682147779DA49caB38C0aA1F","amount":"100000000"}],"name":"my test token", "symbol":"MTT"}' --label test1 --admin 0xbbE4733d85bc2b90682147779DA49caB38C0aA1F --fees 0.001okt --from captain -b block -y)


# contractAddr_0x=$(echo "$res" | jq '.logs[0].events[0].attributes[0].value' | sed 's/\"//g')


# res=$(exchaincli tx wasm execute $contractAddr_0x '{"transfer":{"amount":"100","recipient":"0xCf164e001d86639231d92Ab1D71DB8353E43C295"}}' --fees 0.001okt --from captain -b block -y)

# 合约store测试
# exchaincli tx wasm store /Users/oker/workspace/github/wasm-test/contract/iterator-press/artifacts/iterator_press.wasm --fees 0.01okt --from captain --gas=2000000 -b block -y
# exchaincli tx wasm store /Users/oker/workspace/github/wasm-test/contract/iterator-press/artifacts/iterator_press.wasm --fees 0.01okt --from captain --gas=2000000 -b block -y
# exchaincli tx wasm store /Users/oker/workspace/github/wasm-test/contract/iterator-press/artifacts/iterator_press.wasm --fees 0.01okt --from captain --gas=2000000 -b block -y
# exchaincli tx wasm store /Users/oker/workspace/github/wasm-test/contract/iterator-press/artifacts/iterator_press.wasm --fees 0.01okt --from captain --gas=2000000 -b block -y
# exchaincli tx wasm store /Users/oker/workspace/github/wasm-test/scripts/../contract/testcase/artifacts/testcase.wasm --fees 0.01okt --from captain --gas=2000000 -b block -y
# exchaincli tx wasm store /Users/oker/workspace/github/wasm-test/scripts/../contract/testcase/artifacts/testcase.wasm --fees 0.01okt --from captain --gas=2000000 -b block -y
# exchaincli tx wasm store /Users/oker/workspace/github/wasm-test/scripts/../contract/testcase/artifacts/testcase.wasm --fees 0.01okt --from captain --gas=2000000 -b block -y
# exchaincli tx wasm store /Users/oker/workspace/github/wasm-test/scripts/../contract/testcase/artifacts/testcase.wasm --fees 0.01okt --from captain --gas=2000000 -b block -y
# exchaincli tx wasm store /Users/oker/workspace/github/wasm-test/scripts/../contract/testcase/artifacts/testcase.wasm --fees 0.01okt --from captain --gas=2000000 -b block -y
# exchaincli tx wasm store /Users/oker/workspace/github/wasm-test/scripts/../contract/testcase/artifacts/testcase.wasm --fees 0.01okt --from captain --gas=2000000 -b block -y



# exchaincli tx wasm instantiate "15" '{"decimals":10,"initial_balances":[{"address":"0xbbE4733d85bc2b90682147779DA49caB38C0aA1F","amount":"100000000"}],"name":"my test token", "symbol":"MTT"}' --label test1 --admin 0xbbE4733d85bc2b90682147779DA49caB38C0aA1F --fees 0.001okt --from captain -b block -y

# exchaincli tx wasm execute 0x5d1aaccD4877a7682AAFe9D2Ad408a6E88DcA5Bb '{"transfer":{"amount":"100","recipient":"0xCf164e001d86639231d92Ab1D71DB8353E43C295"}}' --fees 0.001okt --from captain -b block -y


# exchaincli tx wasm execute 0x5d1aaccD4877a7682AAFe9D2Ad408a6E88DcA5Bb '{"burn":{"amount":"100","contract":"0x49A1a1201a7A28bC1EE95C879B8f4088A9F40E3b"}}'  --fees 0.01okt --from captain -b block -y

exchaincli tx wasm instantiate "1" '{"decimals":10,"initial_balances":[{"address":"0x83D83497431C2D3FEab296a9fba4e5FaDD2f7eD0","amount":"100000000"}],"name":"my test token", "symbol":"MTT"}' --label test1 --admin 0x83D83497431C2D3FEab296a9fba4e5FaDD2f7eD0 --fees 0.001okt --from captain -b block -y

exchaincli tx wasm execute 0x5A8D648DEE57b2fc90D98DC17fa887159b69638b '{"transfer":{"amount":"100","recipient":"0xCf164e001d86639231d92Ab1D71DB8353E43C295"}}' --fees 0.001okt --from captain -b block -y

exchaincli tx wasm execute 0xF44E95B40DB99D1f9747259813E8587b4A61ACc7 '{"transfer":{"amount":"100","recipient":"0xCf164e001d86639231d92Ab1D71DB8353E43C295"}}' --fees 0.001okt --from admin16 
