#!/bin/bash

### 方法简要说明：
### 1. 是先查找一个字符串：带双引号的key。如果没找到，则直接返回defaultValue。
### 2. 查找最近的冒号，找到后认为值的部分开始了，直到在层数上等于0时找到这3个字符：,}]。
### 3. 如果有多个同名key，则依次全部打印（不论层级，只按出现顺序）
### @author lux feary
###
### 3 params: json, key, defaultValue
function getJsonValuesByAwk() {
  awk -v json="$1" -v key="$2" -v defaultValue="$3" 'BEGIN{
      foundKeyCount = 0
      while (length(json) > 0) {
          # pos = index(json, "\""key"\""); ## 这行更快一些，但是如果有value是字符串，且刚好与要查找的key相同，会被误认为是key而导致值获取错误
          pos = match(json, "\""key"\"[ \\t]*?:[ \\t]*");
          if (pos == 0) {if (foundKeyCount == 0) {print defaultValue;} exit 0;}

          ++foundKeyCount;
          start = 0; stop = 0; layer = 0;
          for (i = pos + length(key) + 1; i <= length(json); ++i) {
              lastChar = substr(json, i - 1, 1)
              currChar = substr(json, i, 1)

              if (start <= 0) {
                  if (lastChar == ":") {
                      start = currChar == " " ? i + 1: i;
                      if (currChar == "{" || currChar == "[") {
                          layer = 1;
                      }
                  }
              } else {
                  if (currChar == "{" || currChar == "[") {
                      ++layer;
                  }
                  if (currChar == "}" || currChar == "]") {
                      --layer;
                  }
                  if ((currChar == "," || currChar == "}" || currChar == "]") && layer <= 0) {
                      stop = currChar == "," ? i : i + 1 + layer;
                      break;
                  }
              }
          }

          if (start <= 0 || stop <= 0 || start > length(json) || stop > length(json) || start >= stop) {
              if (foundKeyCount == 0) {print defaultValue;} exit 0;
          } else {
              print substr(json, start, stop - start);
          }

          json = substr(json, stop + 1, length(json) - stop)
      }
  }'
}

common-echorunwait() {
  sleep 1
  beginHeight=`exchaincli status | grep "latest_block_height" | sed -r 's/.*"(.*)".*/\1/'`
  #echo "Waiting..."
  for((i=1;i<=10;i++));
  do
      sleep 1
      curHeight=`exchaincli status | grep "latest_block_height" | sed -r 's/.*"(.*)".*/\1/'`
      if [ $curHeight -gt $beginHeight ]
      then
  #      echo $curHeight
  #      echo "Mint a new block now."
        break
      #else
        #echo "Waiting a new block, cur height:" $curHeight
      fi
  done
  echo "------------------------------------------------------------------------------------------------"
  echo "["$@"]"
  result=`$@`
  hash=`echo "$result" | grep "txhash" | sed -r 's/.*"(.*)".*/\1/'`
  if [ ${#hash} != 64 ];then
    echo $result
    echo "error tx result."
    exit
  else
    echo $result | python3 -m json.tool
  fi

  echo "------------------------------------------------------------------------------------------------"
}

common-echorun() {
  echo "------------------------------------------------------------------------------------------------"
  echo "["$@"]"
  $@
  echo "------------------------------------------------------------------------------------------------"
}

common-killwaitblock(){
  while true;do
      sleep 1
      curHeight=`exchaincli status | grep "latest_block_height" | sed -r 's/.*"(.*)".*/\1/'`
      echo $curHeight
      if [ "$curHeight"x == ""x ];then
        echo "error..."
        break
      elif [ $curHeight -ge $2 ];then
        echo "Waiting a new block, cur height:" $curHeight ", killall " $1
        killall $1
        break
      else
        echo "Waiting a new block, cur height:" $curHeight
      fi
  done
}

common-waitblock(){
  while true;do
      sleep 1
      curHeight=`exchaincli status | grep "latest_block_height" | sed -r 's/.*"(.*)".*/\1/'`
      if [ "$curHeight"x == ""x ];then
        echo "error..."
        break
      elif [ $curHeight -ge $1 ];then
        echo "Waiting " $1 ", cur height:" $curHeight
        break
      else
        echo "Waiting a new block, cur height:" $curHeight
      fi
  done
}

common-kill(){
  killall $1
}

common-runallnodes(){
  common-runnode0 $1 $2
  common-runnode1 $1 $2
  common-runnode2 $1 $2
  common-runnode3 $1 $2
  common-runnode4 $1 $2
  sleep 3
}

common-runnode0(){
    common-echorun nohup $2 start --home $1/node0/exchaind --p2p.seed_mode=true --p2p.allow_duplicate_ip --enable-dynamic-gp=false --enable-wtx=false --mempool.node_key_whitelist 0b066ca0790f27a6595560b23bf1a1193f100797,3813c7011932b18f27f172f0de2347871d27e852,6ea83a21a43c30a280a3139f6f23d737104b6975,bab6c32fa95f3a54ecb7d32869e32e85a25d2e08,testnet-node-ids --p2p.pex=false --p2p.addr_book_strict=false --p2p.laddr tcp://127.0.0.1:26656 --rpc.laddr tcp://127.0.0.1:26657 --log_level main:info,*:error,consensus:error,state:info,distr:debug,gov:debug,staking:debug --chain-id exchain-67 --upload-delta=false --enable-gid --consensus.timeout_commit 1000ms --enable-blockpart-ack=false --block-part-size 16 --block-compress-type 0 --block-compress-flag 0 --block-compress-threshold 512 --append-pid=true --elapsed DeliverTxs=0,Round=1,CommitRound=1,Produce=1 --rest.laddr tcp://localhost:8545 --enable-preruntx=false --consensus-role=v0 --keyring-backend test >$1/val0.log 2>&1 &
}

common-runnode1(){
    common-echorun nohup $2 start --home $1/node1/exchaind --p2p.seed_mode=false --p2p.allow_duplicate_ip --enable-dynamic-gp=false --enable-wtx=false --mempool.node_key_whitelist 0b066ca0790f27a6595560b23bf1a1193f100797,3813c7011932b18f27f172f0de2347871d27e852,6ea83a21a43c30a280a3139f6f23d737104b6975,bab6c32fa95f3a54ecb7d32869e32e85a25d2e08,testnet-node-ids --p2p.pex=false --p2p.addr_book_strict=false --p2p.seeds 0b066ca0790f27a6595560b23bf1a1193f100797@127.0.0.1:26656 --p2p.laddr tcp://127.0.0.1:26756 --rpc.laddr tcp://127.0.0.1:26757 --log_level main:info,*:error,consensus:error,state:info,distr:debug,gov:debug,staking:debug --chain-id exchain-67 --upload-delta=false --enable-gid --consensus.timeout_commit 1000ms --enable-blockpart-ack=false --block-part-size 16 --block-compress-type 0 --block-compress-flag 0 --block-compress-threshold 512 --append-pid=true --elapsed DeliverTxs=0,Round=1,CommitRound=1,Produce=1 --rest.laddr tcp://localhost:8645 --enable-preruntx=false --consensus-role=v1 --keyring-backend test >$1/val1.log 2>&1 &
}

common-runnode2(){
    common-echorun nohup $2 start --home $1/node2/exchaind --p2p.seed_mode=false --p2p.allow_duplicate_ip --enable-dynamic-gp=false --enable-wtx=false --mempool.node_key_whitelist 0b066ca0790f27a6595560b23bf1a1193f100797,3813c7011932b18f27f172f0de2347871d27e852,6ea83a21a43c30a280a3139f6f23d737104b6975,bab6c32fa95f3a54ecb7d32869e32e85a25d2e08,testnet-node-ids --p2p.pex=false --p2p.addr_book_strict=false --p2p.seeds 0b066ca0790f27a6595560b23bf1a1193f100797@127.0.0.1:26656 --p2p.laddr tcp://127.0.0.1:26856 --rpc.laddr tcp://127.0.0.1:26857 --log_level main:info,*:error,consensus:error,state:info,distr:debug,gov:debug,staking:debug --chain-id exchain-67 --upload-delta=false --enable-gid --consensus.timeout_commit 1000ms --enable-blockpart-ack=false --block-part-size 16 --block-compress-type 0 --block-compress-flag 0 --block-compress-threshold 512 --append-pid=true --elapsed DeliverTxs=0,Round=1,CommitRound=1,Produce=1 --rest.laddr tcp://localhost:8745 --enable-preruntx=false --consensus-role=v2 --keyring-backend test  >$1/val2.log 2>&1 &
}

common-runnode3(){
    common-echorun nohup $2 start --home $1/node3/exchaind --p2p.seed_mode=false --p2p.allow_duplicate_ip --enable-dynamic-gp=false --enable-wtx=false --mempool.node_key_whitelist 0b066ca0790f27a6595560b23bf1a1193f100797,3813c7011932b18f27f172f0de2347871d27e852,6ea83a21a43c30a280a3139f6f23d737104b6975,bab6c32fa95f3a54ecb7d32869e32e85a25d2e08,testnet-node-ids --p2p.pex=false --p2p.addr_book_strict=false --p2p.seeds 0b066ca0790f27a6595560b23bf1a1193f100797@127.0.0.1:26656 --p2p.laddr tcp://127.0.0.1:26956 --rpc.laddr tcp://127.0.0.1:26957 --log_level main:info,*:error,consensus:error,state:info,distr:debug,gov:debug,staking:debug --chain-id exchain-67 --upload-delta=false --enable-gid --consensus.timeout_commit 1000ms --enable-blockpart-ack=false --block-part-size 16 --block-compress-type 0 --block-compress-flag 0 --block-compress-threshold 512 --append-pid=true --elapsed DeliverTxs=0,Round=1,CommitRound=1,Produce=1 --rest.laddr tcp://localhost:8845 --enable-preruntx=false --consensus-role=v3 --keyring-backend test >$1/val3.log 2>&1 &
}

common-runnode4(){
    common-echorun nohup $2 start --home $1/node4/exchaind --p2p.seed_mode=false --p2p.allow_duplicate_ip --enable-dynamic-gp=false --enable-wtx=false --mempool.node_key_whitelist 0b066ca0790f27a6595560b23bf1a1193f100797,3813c7011932b18f27f172f0de2347871d27e852,6ea83a21a43c30a280a3139f6f23d737104b6975,bab6c32fa95f3a54ecb7d32869e32e85a25d2e08,testnet-node-ids --p2p.pex=false --p2p.addr_book_strict=false --p2p.seeds 0b066ca0790f27a6595560b23bf1a1193f100797@127.0.0.1:26656 --p2p.laddr tcp://127.0.0.1:27056 --rpc.laddr tcp://127.0.0.1:27057 --log_level main:info,*:error,consensus:error,state:info,distr:debug,gov:debug,staking:debug --chain-id exchain-67 --upload-delta=false --enable-gid --consensus.timeout_commit 1000ms --enable-blockpart-ack=false --block-part-size 16 --block-compress-type 0 --block-compress-flag 0 --block-compress-threshold 512 --append-pid=true --elapsed DeliverTxs=0,Round=1,CommitRound=1,Produce=1 --rest.laddr tcp://localhost:8945 --enable-preruntx=false --consensus-role=v4 --keyring-backend test >$1/val4.log 2>&1 &
}

common-deposit(){
  common-echorunwait exchaincli tx staking deposit $1okt --from $2 --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y
}

common-add-shares(){
  common-echorunwait exchaincli tx staking add-shares $1 --from $2 --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y
}


common-send(){
  common-echorunwait exchaincli tx send $1 $2 $3okt --from $1 --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y
}

common-proxy-reg(){
  common-echorunwait exchaincli tx staking proxy reg --from $1 --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y
}

common-proxy-bind(){
  common-echorunwait exchaincli tx staking proxy bind $1 --from $2 --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y
}

common-submit-proposal-onchain(){
  common-echorunwait exchaincli tx gov submit-proposal change-distr-type proposal-change-distr-type-1.json --from $1 --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y
}

common-submit-proposal-offchain(){
  common-echorunwait exchaincli tx gov submit-proposal change-distr-type proposal-change-distr-type-0.json --from $1 --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y
}

common-vote(){
  common-echorunwait exchaincli tx gov vote $1 yes --from $2 --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y
}

common-withdraw-rewards-commission(){
  common-echorunwait exchaincli tx distr withdraw-rewards $1 --commission --from $2 --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y
}

common-withdraw-rewards(){
  common-echorunwait exchaincli tx distr withdraw-rewards $1 --from $2 --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y
}

common-withdraw-all-rewards(){
  common-echorunwait exchaincli tx distr withdraw-all-rewards --from $1 --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y
}

common-create-validator(){
  common-echorunwait exchaincli tx staking create-validator --pubkey=$1 --moniker=zhujianguo --from $2 --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y
}

common-edit-validator(){
  common-echorunwait exchaincli tx staking edit-validator-commission-rate $1 --from $2 --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y
}

common-query-shares(){
  common-echorun exchaincli query  staking delegator $1
}

common-query-account(){
  cmd="exchaincli query account $1"
  echo [$cmd]
  result=`$cmd`
  newReuslt=`echo $result | sed 's/ //g'`
  value=`getJsonValuesByAwk "$newReuslt" "amount" "-1"`
  echo $value
  if [ $1 == -1 ]; then
    echo "errror query"
    echo $result
    exit
  fi

  # json='{"type":"okexchain/EthAccount","value":{"address":"ex1j5mr2jhr9pf20e7yhln5zkcsgqtdt7cydr8x3y","eth_address":"0x9536354AE32852A7E7C4BFe7415b104016d5Fb04","coins":[{"denom":"okt","amount":"10000.000000000000000000"}],"public_key":"","account_number":19,"sequence":0,"code_hash":"c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470"}}'
  # getJsonValuesByAwk "$json" "amount" "defaultValue"
}

common-query-commission(){
  common-echorun exchaincli query distr commission $1
}

common-query-rewards(){
  common-echorun exchaincli query distr rewards $1 $2
}

common-query-withdraw(){
  common-echorun exchaincli query distr withdraw-addr $1
}

common-query-staking-validators(){
  common-echorun exchaincli query staking validators
}

common-query-proposal(){
  common-echorun exchaincli query gov proposal $1
}

common-query-outstanding(){
  common-echorun exchaincli query distr outstanding-rewards $1
}

common-query-distr-params(){
  common-echorun exchaincli query distr params
}

common-version(){
  cmd="exchaincli version"
  result=`$cmd`
  echo "now version:"$result
  if [ "$1"x != "$result"x ]; then
    echo "error version"
    echo "expect version:" $1
    exit
  fi
}

