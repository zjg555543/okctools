
# case_distr_proposal.py 配置说明
- 需要两个版本git：升级后的分支，和升级前的分支
- 需要两个版本git：升级后的分支，和升级前的分支

# 新分支修改
## makefile 文件修改
Version=v1.6.9
## okc.profile
OKCHAIN_TOP=/Users/oker/workspace/exchain
## testnet.sh
(cd ${OKCHAIN_TOP} && make install VenusHeight=1 Venus5Height=400)

# 老分支修改
## ./testnet.sh
echorun exchaind testnet --v $1 --r $2 --equal-voting-power=true -o cache -l \
## okc.profile
OKCHAIN_TOP=/Users/oker/workspace/exchain-raw/

