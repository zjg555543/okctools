#!/usr/bin/env bash

source test-common.sh
source distrtype-proposal-config.sh

initChain() {
  echo '------------------------initChain start--------------------------------'
  # 编译老的4个节点，运行
  cd $devGitPath/dev/testnet
  ./run4v1r.sh
  common-killwaitblock exchaind 1
  cd -

  # 迁移命令行和迁移文件夹，重新启动
  common-echorun rm -rf /Users/oker/workspace/nodes/*
  common-echorun cp -rf $devGitPath/dev/testnet/cache/* /Users/oker/workspace/nodes/
  common-runallnodes $nodes exchaind
  common-version v1.6.0

  # 导入委托人账户和代理人账户
  exchaincli keys add --recover delegator1 -m "$mnemonicdelegator1" -y
  exchaincli keys add --recover delegator2 -m "$mnemonicdelegator2" -y
  exchaincli keys add --recover delegator3 -m "$mnemonicdelegator3" -y
  exchaincli keys add --recover delegator4 -m "$mnemonicdelegator4" -y
  exchaincli keys add --recover delegator5 -m "$mnemonicdelegator5" -y
  exchaincli keys add --recover delegator6 -m "$mnemonicdelegator6" -y
  exchaincli keys add --recover delegator7 -m "$mnemonicdelegator7" -y
  exchaincli keys add --recover delegator8 -m "$mnemonicdelegator8" -y
  exchaincli keys add --recover delegator9 -m "$mnemonicdelegator9" -y
  exchaincli keys add --recover delegator10 -m "$mnemonicdelegator10" -y
  exchaincli keys add --recover proxy1 -m "$mnemonicproxy1" -y
  exchaincli keys add --recover proxy2 -m "$mnemonicproxy2" -y
  exchaincli keys add --recover proxy3 -m "$mnemonicproxy3" -y
  exchaincli keys add --recover proxy4 -m "$mnemonicproxy4" -y
  exchaincli keys add --recover proxy5 -m "$mnemonicproxy5" -y
  exchaincli keys add --recover proxy6 -m "$mnemonicproxy6" -y
  
  exchaincli keys add --recover proxydelegator1 -m "$mnemonicproxydelegator1" -y
  exchaincli keys add --recover proxydelegator2 -m "$mnemonicproxydelegator2" -y
  exchaincli keys add --recover proxydelegator3 -m "$mnemonicproxydelegator3" -y
  exchaincli keys add --recover proxydelegator4 -m "$mnemonicproxydelegator4" -y
  exchaincli keys add --recover proxydelegator5 -m "$mnemonicproxydelegator5" -y
  exchaincli keys add --recover proxydelegator6 -m "$mnemonicproxydelegator6" -y
  # 导入4个验证节点，并初始化账户
  exchaincli keys add --recover va1 -m "$mnemonicva1" --coin-type 996 -y
  exchaincli keys add --recover va2 -m "$mnemonicva2" --coin-type 996 -y
  exchaincli keys add --recover va3 -m "$mnemonicva3" --coin-type 996 -y
  exchaincli keys add --recover va4 -m "$mnemonicva4" --coin-type 996 -y

  common-send $captain $delegator1 1000000 
  common-send $captain $delegator2 1000000 
  common-send $captain $delegator3 1000000 
  common-send $captain $delegator4 1000000 
  common-send $captain $delegator5 1000000 
  common-send $captain $delegator6 1000000 
  common-send $captain $delegator7 1000000 
  common-send $captain $delegator8 1000000 
  common-send $captain $delegator9 1000000 
  common-send $captain $delegator10 1000000 
  common-send $captain $proxy1 1000000 
  common-send $captain $proxy2 1000000 
  common-send $captain $proxy3 1000000 
  common-send $captain $proxy4 1000000 
  common-send $captain $proxy5 1000000 
  common-send $captain $proxy6 1000000 

  common-send $captain $proxydelegator1 1000000 
  common-send $captain $proxydelegator2 1000000 
  common-send $captain $proxydelegator3 1000000 
  common-send $captain $proxydelegator4 1000000 
  common-send $captain $proxydelegator5 1000000 
  common-send $captain $proxydelegator6 1000000 

  common-query-account $delegator1
  common-query-account $delegator2
  common-query-account $delegator3
  common-query-account $delegator4
  common-query-account $delegator5
  common-query-account $delegator6
  common-query-account $delegator7
  common-query-account $delegator8
  common-query-account $delegator9
  common-query-account $delegator10
  common-query-account $proxy1
  common-query-account $proxy2
  echo '------------------------initChain end--------------------------------'
}

initStaking() {
  echo '------------------------initStaking start--------------------------------'
  # 使用旧的程序，1个委托人 + 1个代理1（1个委托人）
  common-query-staking-validators
  common-deposit 10000 $delegator1
  common-add-shares $va1 $delegator1

  common-deposit 10000 $proxydelegator1

  common-query-shares $delegator1
  common-query-shares $proxydelegator1

  common-query-commission $va1
  common-query-commission $va2
  common-query-commission $va3
  common-query-commission $va4

  # 注册代理1,绑定委托人2
  common-deposit  10000 $proxy1
  common-add-shares $va1,$va2,$va3,$va4 $proxy1
  common-proxy-reg proxy1
  common-proxy-bind $proxy1 $proxydelegator1

  echo '------------------------initStaking end--------------------------------'
}

upgrateBinStaking() {
  echo '------------------------upgrateBinStaking start--------------------------------'
  # 新的程序启动后，没有升级之前，新的接口不可用，新的交易发送失败
  common-killwaitblock exchaind 1

  # 编译新的的4个节点，运行
  cd $newGitPaht/dev/testnet
  sleep 1
  ./run4v1r.sh
  sleep 1
  common-killwaitblock exchaind 1
  sleep 1
  cd -
  sleep 1
  common-runallnodes $nodes exchaind
  sleep 1
  common-version v1.6.1

  # 使用新的程序，1个委托人 + 1个代理1（1个委托人）
  common-query-staking-validators
  common-deposit  10000 $delegator2
  common-add-shares $va1 $delegator2

  common-deposit  10000 $proxydelegator2

  common-query-shares $delegator2
  common-query-shares $proxydelegator2

  # 注册代理2,绑定委托人2
  common-deposit 10000 $proxy2
  common-add-shares $va1,$va2,$va3,$va4 $proxy2
  common-proxy-reg $proxy2
  common-proxy-bind $proxy2 $proxydelegator2
  echo '------------------------upgrateBinStaking end--------------------------------'
}

upgrateLedgerStaking() {
  echo '------------------------upgrateLedgerStaking start--------------------------------'
  # 新的程序启动，区块升级之后，没有投票提案，仍然按照佣金100%提成计算，查询验证节点投票仍然可用，验证节点取款仍然有效
  common-waitblock 50
  common-query-commission $va1
  common-query-commission $va2
  common-query-commission $va3
  common-query-commission $va4

  # 使用新的程序，继续以上所有操作，可正常使用 + 委托人5 + 代理3（绑定委托人6），出到100个区块暂停
  common-query-staking-validators
  common-deposit  10000 $delegator3
  common-add-shares $va1 $delegator3

  common-deposit  10000 $proxydelegator3

  common-query-shares $delegator3
  common-query-shares $proxydelegator3

  # 注册代理3,绑定委托人6
  common-deposit 10000 $proxy3
  common-add-shares $va1,$va2,$va3,$va4 $proxy3
  common-proxy-reg $proxy3
  common-proxy-bind $proxy3 $proxydelegator3
  echo '------------------------upgrateLedgerStaking end--------------------------------'
}

afterDistrProposal() {
  echo '------------------------afterDistrProposal start--------------------------------'
  common-runallnodes $nodes exchaind
  sleep 1
  common-version v1.6.1
  # 发起投票提案，修改提案，此时分红比例默认为100%，各个接口可以使用，验证节点查询抽成，提取抽成正常；委托人查询分红为0；代理人查询为0，无法提取抽成；
  
  common-waitblock 65
  common-submit-proposal-onchain $delegator1
  sleep 5
  proposal_num=1
  common-query-proposal $proposal_num
  common-vote $proposal_num $delegator1
  common-vote $proposal_num $delegator2
  common-vote $proposal_num $delegator3
  common-vote $proposal_num $proxy1
  common-vote $proposal_num $proxy2
  common-vote $proposal_num $proxy3
  
  # common-vote $proposal_num va1
  # common-vote $proposal_num va2
  # common-vote $proposal_num va3
  # common-vote $proposal_num va4
  sleep 5
  common-query-proposal $proposal_num

  
  # # 查询抽成
  common-query-commission $va1
  common-query-commission $va2
  common-query-commission $va3
  common-query-commission $va4

  # 查询outstanding
  common-query-outstanding $va1
  common-query-outstanding $va2
  common-query-outstanding $va3
  common-query-outstanding $va4
  

  # 查询奖励
  common-query-rewards $proxy1
  common-query-rewards $proxy2
  common-query-rewards $proxy3

  common-query-rewards $proxydelegator1
  common-query-rewards $proxydelegator2
  common-query-rewards $proxydelegator3

  common-query-rewards $delegator1
  common-query-rewards $delegator2
  common-query-rewards $delegator3

  # 验证节点提取奖励
  common-withdraw-rewards-commission $va1 va1
  common-withdraw-rewards-commission $va2 va2

  # 代理人提取分红
  common-withdraw-rewards $va1 $proxy1
  common-withdraw-rewards $va1 $delegator1


  # 验证节点1 设置分红比例30%
  common-edit-validator 0.3 va1

  sleep 15

  # 查询分红和奖励
  common-query-rewards $proxy1
  common-query-rewards $proxy2
  common-query-rewards $proxy3

  common-query-rewards $proxydelegator1
  common-query-rewards $proxydelegator2
  common-query-rewards $proxydelegator3

  common-query-rewards $delegator1
  common-query-rewards $delegator2
  common-query-rewards $delegator3

  # 验证节点提取奖励
  common-withdraw-rewards-commission $va1 va1
  common-withdraw-rewards-commission $va2 va2

  # 提取分红
  common-withdraw-rewards $va1 $proxy1
  # common-withdraw-rewards $va1 $proxydelegator1
  common-withdraw-rewards $va1 $delegator1

  # 新增验证节点
  # common-create-validator $(exchaind tendermint show-validator) $admin16
  # common-edit-validator 0.3 $admin16
  # common-query-staking-validators

  # 投票分红
  common-query-staking-validators
  common-deposit  10000 $delegator4
  common-add-shares $va1 $delegator4

  common-deposit  10000 $proxydelegator4

  common-query-shares $delegator4
  common-query-shares $proxydelegator4

  # 查询v1 v2 v3 v4 v5 的分红和outstanding
  common-query-commission $va1
  common-query-commission $va2
  common-query-commission $va3
  common-query-commission $va4
  # common-query-commission $admin16

  # 查询outstanding
  common-query-outstanding $va1
  common-query-outstanding $va2
  common-query-outstanding $va3
  common-query-outstanding $va4
  # common-query-outstanding $admin16

  # 取出抽成
  common-withdraw-rewards-commission $va1 va1
  common-withdraw-rewards-commission $va2 va2
  common-withdraw-rewards-commission $va3 va3
  common-withdraw-rewards-commission $va4 va4
  # common-withdraw-rewards-commission $admin16 admin16

  # 取出所有分红 TODO
  common-withdraw-all-rewards $proxy1
  common-withdraw-all-rewards $proxy2
  common-withdraw-all-rewards $proxy3
  common-withdraw-all-rewards $delegator1
  common-withdraw-all-rewards $delegator2
  common-withdraw-all-rewards $delegator3
  

  # 重新质押，继续以上所有操作，可正常使用 + 委托人5 + 代理3（绑定委托人6），出到100个区块暂停
  common-query-staking-validators
  common-deposit  10000 $delegator4
  common-add-shares $va1 $delegator4

  common-deposit  10000 $proxydelegator4
  common-query-shares $delegator4
  common-query-shares $proxydelegator4

  # 注册代理3,绑定委托人6
  common-deposit 10000 $proxy4
  common-add-shares $va1,$va2,$va3,$va4 $proxy4
  common-proxy-reg $proxy4
  common-proxy-bind $proxy4 $proxydelegator4

  echo '------------------------afterDistrProposal end--------------------------------'
}

addNewVal() {
  echo '------------------------addNewVal start--------------------------------'
  common-runallnodes $nodes exchaind
  sleep 1
  common-version v1.6.1
  # 发起投票提案，修改提案，此时分红比例默认为100%，各个接口可以使用，验证节点查询抽成，提取抽成正常；委托人查询分红为0；代理人查询为0，无法提取抽成；
  
  common-waitblock 65
  common-submit-proposal-onchain $delegator1
  sleep 5
  proposal_num=1
  common-query-proposal $proposal_num
  common-vote $proposal_num $delegator1
  common-vote $proposal_num $delegator2
  common-vote $proposal_num $delegator3
  common-vote $proposal_num $proxy1
  common-vote $proposal_num $proxy2
  common-vote $proposal_num $proxy3
  
  # common-vote $proposal_num va1
  # common-vote $proposal_num va2
  # common-vote $proposal_num va3
  # common-vote $proposal_num va4
  sleep 2
  common-query-proposal $proposal_num

  
  # # 查询抽成
  # common-query-commission $va1
  # common-query-commission $va2
  # common-query-commission $va3
  # common-query-commission $va4

  # # 查询outstanding
  # common-query-outstanding $va1
  # common-query-outstanding $va2
  # common-query-outstanding $va3
  # common-query-outstanding $va4
  

  # 查询奖励
  # common-query-rewards $proxy1
  # common-query-rewards $proxy2
  # common-query-rewards $proxy3

  # common-query-rewards $proxydelegator1
  # common-query-rewards $proxydelegator2
  # common-query-rewards $proxydelegator3

  # common-query-rewards $delegator1
  # common-query-rewards $delegator2
  # common-query-rewards $delegator3

  # 验证节点1 设置分红比例30%
  #common-edit-validator 0.3 va1

  sleep 1

  # 查询分红和奖励
  # common-query-rewards $proxy1
  # common-query-rewards $proxy2
  # common-query-rewards $proxy3

  # common-query-rewards $proxydelegator1
  # common-query-rewards $proxydelegator2
  # common-query-rewards $proxydelegator3

  # common-query-rewards $delegator1
  # common-query-rewards $delegator2
  # common-query-rewards $delegator3

  # 新增验证节点
  common-create-validator $(exchaind tendermint show-validator) $admin16
  common-edit-validator 0.01 $admin16
  common-query-staking-validators

  # 注册代理3,绑定委托人6
  common-deposit  800000 $proxydelegator4
  common-deposit 800000 $proxy4

  common-add-shares $vaadmin16 $proxy4
  common-proxy-reg $proxy4
  common-proxy-bind $proxy4 $proxydelegator4

  # common-query-rewards $proxy4

  echo '------------------------addNewVal end--------------------------------'
}


changeToOffchain() {
  echo '------------------------changeToOffchain start--------------------------------'
  common-runallnodes $nodes exchaind
  sleep 1
  common-version v1.6.1
  # 修改成链下分红
  common-submit-proposal-offchain $delegator1
  sleep 6
  proposal_num=2
  common-query-proposal $proposal_num
  common-vote $proposal_num $delegator1
  common-vote $proposal_num $delegator2
  common-vote $proposal_num $delegator3
  common-vote $proposal_num $delegator4
  common-vote $proposal_num $proxy1
  common-vote $proposal_num $proxy2
  common-vote $proposal_num $proxy3
  common-vote $proposal_num $proxy4
  
  # common-vote $proposal_num va1
  # common-vote $proposal_num va2
  # common-vote $proposal_num va3
  # common-vote $proposal_num va4
  sleep 10
  common-query-proposal $proposal_num

  # 正常提取分红
  common-withdraw-all-rewards $proxy1
  common-withdraw-all-rewards $proxy2
  common-withdraw-all-rewards $proxy3
  common-withdraw-all-rewards $delegator1
  common-withdraw-all-rewards $delegator2
  common-withdraw-all-rewards $delegator3

  # 重新质押，继续以上所有操作，可正常使用 + 委托人5 + 代理3（绑定委托人6），出到100个区块暂停
  common-query-staking-validators
  common-deposit  10000 $delegator5
  common-add-shares $va1 $delegator5

  common-deposit  10000 $proxydelegator5

  common-query-shares $delegator5
  common-query-shares $proxydelegator5

  # 取出抽成
  common-withdraw-rewards-commission $va1 va1
  common-withdraw-rewards-commission $va2 va2
  common-withdraw-rewards-commission $va3 va3
  common-withdraw-rewards-commission $va4 va4

  # 注册代理3,绑定委托人6
  common-deposit 10000 $proxy5
  common-add-shares $va1,$va2,$va3,$va4 $proxy5
  common-proxy-reg $proxy5
  common-proxy-bind $proxy5 $proxydelegator5

  # 查询outstaning
  common-query-outstanding $va1
  common-query-outstanding $va2
  common-query-outstanding $va3
  common-query-outstanding $va4

  # 查询分红和奖励
  common-query-rewards $proxy1
  common-query-rewards $proxy2
  common-query-rewards $proxy3
  common-query-rewards $proxy4
  common-query-rewards $proxy5

  common-query-rewards $proxydelegator1
  common-query-rewards $proxydelegator2
  common-query-rewards $proxydelegator3
  common-query-rewards $proxydelegator4
  common-query-rewards $proxydelegator5

  common-query-rewards $delegator1
  common-query-rewards $delegator2
  common-query-rewards $delegator3
  common-query-rewards $delegator4
  common-query-rewards $delegator5

  # 取出抽成
  common-withdraw-rewards-commission $va1 va1
  common-withdraw-rewards-commission $va2 va2
  common-withdraw-rewards-commission $va3 va3
  common-withdraw-rewards-commission $va4 va4
  # common-withdraw-rewards-commission $admin16 admin16

  # 取出分红
  common-withdraw-rewards $va1 $proxy1
  common-withdraw-rewards $va1 $proxy2
  common-withdraw-rewards $va1 $proxy3
  common-withdraw-rewards $va1 $proxy4
  common-withdraw-rewards $va1 $proxy5
  
  common-withdraw-rewards $va1 $delegator1
  common-withdraw-rewards $va1 $delegator2
  common-withdraw-rewards $va1 $delegator3
  common-withdraw-rewards $va1 $delegator4
  common-withdraw-rewards $va1 $delegator5

  common-withdraw-rewards $va2 $proxy2
  common-withdraw-rewards $va2 $delegator1
  common-withdraw-rewards $va2 $delegator2
  common-withdraw-rewards $va2 $delegator3
  common-withdraw-rewards $va1 $delegator4
  common-withdraw-rewards $va1 $delegator5

  # 取出所有分红
  common-withdraw-all-rewards $proxy1
  common-withdraw-all-rewards $proxy2
  common-withdraw-all-rewards $proxy3
  common-withdraw-all-rewards $proxy4
  common-withdraw-all-rewards $proxy5
  common-withdraw-all-rewards $delegator1
  common-withdraw-all-rewards $delegator2
  common-withdraw-all-rewards $delegator3
  common-withdraw-all-rewards $delegator4
  common-withdraw-all-rewards $delegator5

  # 查询分红比例
  common-query-staking-validators

  # 查询参数
  common-query-distr-params

  echo '------------------------changeToOffchain end--------------------------------'
}

changeToOnchain() {
  echo '------------------------changeToOnchain start--------------------------------'

  common-runallnodes $nodes exchaind
  sleep 3
  common-version v1.6.1
  # 发起投票提案，修改提案，此时分红比例默认为100%，各个接口可以使用，验证节点查询抽成，提取抽成正常；委托人查询分红为0；代理人查询为0，无法提取抽成；
  
  common-waitblock 65
  common-submit-proposal-onchain $delegator1
  sleep 5
  proposal_num=3
  common-query-proposal $proposal_num
  common-vote $proposal_num $delegator1
  common-vote $proposal_num $delegator2
  common-vote $proposal_num $delegator3
  common-vote $proposal_num $delegator4
  common-vote $proposal_num $delegator5
  common-vote $proposal_num $proxy1
  common-vote $proposal_num $proxy2
  common-vote $proposal_num $proxy3
  common-vote $proposal_num $proxy4
  # common-vote $proposal_num $proxy5
  
  # common-vote $proposal_num va1
  # common-vote $proposal_num va2
  # common-vote $proposal_num va3
  # common-vote $proposal_num va4
  sleep 5
  common-query-proposal $proposal_num

  # 正常提取分红
  common-withdraw-all-rewards $proxy1
  common-withdraw-all-rewards $proxy2
  common-withdraw-all-rewards $proxy3
  common-withdraw-all-rewards $delegator1
  common-withdraw-all-rewards $delegator2
  common-withdraw-all-rewards $delegator3

  # 重新质押，继续以上所有操作，可正常使用 + 委托人5 + 代理3（绑定委托人6），出到100个区块暂停
  common-query-staking-validators
  common-deposit  10000 $delegator6
  common-add-shares $va1 $delegator6

  common-deposit  10000 $proxydelegator6

  common-query-shares $delegator6
  common-query-shares $proxydelegator6

  # 注册代理3,绑定委托人6
  common-deposit 10000 $proxy6
  common-add-shares $va1,$va2,$va3,$va4 $proxy6
  common-proxy-reg $proxy6
  common-proxy-bind $proxy6 $proxydelegator6

  # 取出抽成
  common-withdraw-rewards-commission $va1 va1
  common-withdraw-rewards-commission $va2 va2
  common-withdraw-rewards-commission $va3 va3
  common-withdraw-rewards-commission $va4 va4
  # common-withdraw-rewards-commission $admin16 $admin16


  # 取出所有分红
  common-withdraw-all-rewards $proxy1
  common-withdraw-all-rewards $proxy2
  common-withdraw-all-rewards $proxy3
  common-withdraw-all-rewards $proxy4
  common-withdraw-all-rewards $proxy5
  common-withdraw-all-rewards $proxy6
  common-withdraw-all-rewards $delegator1
  common-withdraw-all-rewards $delegator2
  common-withdraw-all-rewards $delegator3
  common-withdraw-all-rewards $delegator4
  common-withdraw-all-rewards $delegator5
  common-withdraw-all-rewards $delegator6

  # 查询分红比例
  common-query-staking-validators

  # 查询参数
  common-query-distr-params
  echo '------------------------changeToOnchain end--------------------------------'
}

testForSMB(){

  common-runnode0 $nodes exchaind-my
  common-runnode1 $nodes exchaind-my
  common-runnode2 $nodes exchaind-dev
  common-runnode3 $nodes exchaind-dev
  common-runnode4 $nodes exchaind-dev

  # 导入委托人账户和代理人账户
  exchaincli keys add --recover delegator1 -m "$mnemonicdelegator1" -y
  exchaincli keys add --recover delegator2 -m "$mnemonicdelegator2" -y
  exchaincli keys add --recover delegator3 -m "$mnemonicdelegator3" -y
  exchaincli keys add --recover delegator4 -m "$mnemonicdelegator4" -y
  exchaincli keys add --recover delegator5 -m "$mnemonicdelegator5" -y
  exchaincli keys add --recover delegator6 -m "$mnemonicdelegator6" -y
  exchaincli keys add --recover delegator7 -m "$mnemonicdelegator7" -y
  exchaincli keys add --recover delegator8 -m "$mnemonicdelegator8" -y
  exchaincli keys add --recover delegator9 -m "$mnemonicdelegator9" -y
  exchaincli keys add --recover delegator10 -m "$mnemonicdelegator10" -y
  exchaincli keys add --recover proxy1 -m "$mnemonicproxy1" -y
  exchaincli keys add --recover proxy2 -m "$mnemonicproxy2" -y
  exchaincli keys add --recover proxy3 -m "$mnemonicproxy3" -y
  exchaincli keys add --recover proxy4 -m "$mnemonicproxy4" -y
  exchaincli keys add --recover proxy5 -m "$mnemonicproxy5" -y
  exchaincli keys add --recover proxy6 -m "$mnemonicproxy6" -y
  
  exchaincli keys add --recover proxydelegator1 -m "$mnemonicproxydelegator1" -y
  exchaincli keys add --recover proxydelegator2 -m "$mnemonicproxydelegator2" -y
  exchaincli keys add --recover proxydelegator3 -m "$mnemonicproxydelegator3" -y
  exchaincli keys add --recover proxydelegator4 -m "$mnemonicproxydelegator4" -y
  exchaincli keys add --recover proxydelegator5 -m "$mnemonicproxydelegator5" -y
  exchaincli keys add --recover proxydelegator6 -m "$mnemonicproxydelegator6" -y
  # 导入4个验证节点，并初始化账户
  exchaincli keys add --recover va1 -m "$mnemonicva1" --coin-type 996 -y
  exchaincli keys add --recover va2 -m "$mnemonicva2" --coin-type 996 -y
  exchaincli keys add --recover va3 -m "$mnemonicva3" --coin-type 996 -y
  exchaincli keys add --recover va4 -m "$mnemonicva4" --coin-type 996 -y

  common-send $captain $delegator1 1000000 
  common-send $captain $delegator2 1000000 
  common-send $captain $delegator3 1000000 
  common-send $captain $delegator4 1000000 
  common-send $captain $delegator5 1000000 
  common-send $captain $delegator6 1000000 
  common-send $captain $delegator7 1000000 
  common-send $captain $delegator8 1000000 
  common-send $captain $delegator9 1000000 
  common-send $captain $delegator10 1000000 
  common-send $captain $proxy1 1000000 
  common-send $captain $proxy2 1000000 
  common-send $captain $proxy3 1000000 
  common-send $captain $proxy4 1000000 
  common-send $captain $proxy5 1000000 
  common-send $captain $proxy6 1000000 

  common-send $captain $proxydelegator1 1000000 
  common-send $captain $proxydelegator2 1000000 
  common-send $captain $proxydelegator3 1000000 
  common-send $captain $proxydelegator4 1000000 
  common-send $captain $proxydelegator5 1000000 
  common-send $captain $proxydelegator6 1000000 


  common-deposit 10000 $delegator1
  common-add-shares $va1 $delegator1
  common-deposit 10000 $proxydelegator1

  common-deposit  10000 $proxy1
  common-add-shares $va1,$va2,$va3,$va4 $proxy1
  common-proxy-reg proxy1
  common-proxy-bind $proxy1 $proxydelegator1

  common-withdraw-rewards $va1 va1

  exchaincli tx staking create-validator --pubkey=$(exchaind-dev tendermint show-validator) --moniker="my nickname" --identity="logo|||http://mywebsite/pic/logo.jpg" --website="http://mywebsite" --details="my slogan" --from admin16 --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y
  exchaincli tx staking edit-validator --moniker=“my new nickname” --identity="zhujianguo.jpg" --website="http://mynewwebsite" --details="my new slogan"  --from admin16 --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y
  exchaincli tx staking deposit 10okt --from admin16 --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y
  exchaincli tx staking add-shares exvaloper1s0vrf96rrsknl64jj65lhf89ltwj7lks4e348l --from admin16 --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y

}

initChain
initStaking

upgrateBinStaking
upgrateLedgerStaking

afterDistrProposal

changeToOffchain
changeToOnchain



# testForSMB