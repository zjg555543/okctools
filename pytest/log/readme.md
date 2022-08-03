
# case_distr_proposal.py 配置说明
- 需要两个版本git：升级后的分支，和升级前的分支
- 需要两个版本git：升级后的分支，和升级前的分支

# 新分支修改
## makefile 文件修改

Version=v1.6.1
-X $(GithubTop)/okex/exchain/libs/tendermint/types.MILESTONE_VENUS3_HEIGHT=$(Venus3Height)


## okc.profile
OKCHAIN_TOP=/Users/oker/workspace/exchain

## testnet.sh
(cd ${OKCHAIN_TOP} && make install VenusHeight=1 Venus3Height=200)
echorun exchaind testnet --v $1 --r $2 --equal-voting-power -o cache -l \
LOG_LEVEL=main:info,*:error,consensus:error,state:info,distr:debug,gov:debug,staking:debug
  --consensus.timeout_commit 1000ms \


# 老分支修改
## ./testnet.sh
echorun exchaind testnet --v $1 --r $2 --equal-voting-power -o cache -l \

LOG_LEVEL=main:debug,*:debug,consensus:debug,state:debug,distr:debug,gov:debug,staking:debug
     --consensus.timeout_commit 1000ms \

## okc.profile
  OKCHAIN_TOP=/Users/oker/workspace/exchain-raw/



- 所有账户要初始化，包括验证节点
- 导入超级节点账户私钥要注意格式


- delegator 10 操作记录

exchaincli tx staking add-shares exvaloper1pt7xrmxul7sx54ml44lvv403r06clrdkehd8z7,exvaloper1q6ls3h64gkxq0r73u2eqwwr7d5mp583fm325zu,exvaloper1ve4mwgq9967gk338yptsg2fheur4ke322gzynt,exvaloper1gd6avvrg0jp5wxpfyfa4c84fygtl6cn9dage6d --from ex10t7hhfjya9k7yn9ymdg79n68zeuk224xn27fx8 --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y

exchaincli query tx 0B5C1779FDFE94131C87F94E0BA1B45FED323AB480D21EF8F7AD40233753BEB1

exchaincli query account ex10t7hhfjya9k7yn9ymdg79n68zeuk224xn27fx8

exchaincli query distr rewards  ex10t7hhfjya9k7yn9ymdg79n68zeuk224xn27fx8 

exchaincli query staking delegator ex10t7hhfjya9k7yn9ymdg79n68zeuk224xn27fx8

exchaincli tx staking deposit 700000okt --from ex10t7hhfjya9k7yn9ymdg79n68zeuk224xn27fx8 --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y 

exchaincli tx staking add-shares exvaloper1pt7xrmxul7sx54ml44lvv403r06clrdkehd8z7 --from ex10t7hhfjya9k7yn9ymdg79n68zeuk224xn27fx8 --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y 


exchaincli tx staking withdraw 100000okt --from ex10t7hhfjya9k7yn9ymdg79n68zeuk224xn27fx8 --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y 

exchaincli tx distr withdraw-all-rewards --from ex10t7hhfjya9k7yn9ymdg79n68zeuk224xn27fx8 --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y

exchaincli tx distr withdraw-rewards exvaloper1pt7xrmxul7sx54ml44lvv403r06clrdkehd8z7 --commission --from ex10t7hhfjya9k7yn9ymdg79n68zeuk224xn27fx8 --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y

exchaincli query staking shares-added-to exvaloper1pt7xrmxul7sx54ml44lvv403r06clrdkehd8z7

exchaincli tx staking proxy reg --from ex10t7hhfjya9k7yn9ymdg79n68zeuk224xn27fx8 --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y

exchaincli tx staking proxy bind ex153z8qwxkqa5p2samfn8z50kr9pt8j6afs0am6e --from ex10t7hhfjya9k7yn9ymdg79n68zeuk224xn27fx8 --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y


exchaincli tx staking proxy unbind ex10lcvjcavvhgmduskh3kw0jlcm0w0kuyuzs57xl --from ex10t7hhfjya9k7yn9ymdg79n68zeuk224xn27fx8 --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y 

exchaincli tx staking  proxy unreg --from ex10t7hhfjya9k7yn9ymdg79n68zeuk224xn27fx8 --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y 


