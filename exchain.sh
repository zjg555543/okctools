#!/bin/bash

echorun() {
  echo "sleep 1------------------------------------------------------------------------------------------------"
  echo "["$@"]"
  $@
  echo "------------------------------------------------------------------------------------------------"
}

runnode0(){
    echorun nohup exchaind start --home /Users/oker/workspace/exchain/dev/testnet/cache/node0/exchaind --p2p.seed_mode=true --p2p.allow_duplicate_ip --enable-dynamic-gp=false --enable-wtx=false --mempool.node_key_whitelist 0b066ca0790f27a6595560b23bf1a1193f100797,3813c7011932b18f27f172f0de2347871d27e852,6ea83a21a43c30a280a3139f6f23d737104b6975,bab6c32fa95f3a54ecb7d32869e32e85a25d2e08,testnet-node-ids --p2p.pex=false --p2p.addr_book_strict=false --p2p.laddr tcp://127.0.0.1:26656 --rpc.laddr tcp://127.0.0.1:26657 --log_level main:info,*:error,consensus:error,state:info,distr:debug,gov:debug,staking:debug --chain-id exchain-67 --upload-delta=false --enable-gid --consensus.timeout_commit 6000ms --enable-blockpart-ack=false --block-part-size 16 --block-compress-type 0 --block-compress-flag 0 --block-compress-threshold 512 --append-pid=true --elapsed DeliverTxs=0,Round=1,CommitRound=1,Produce=1 --rest.laddr tcp://localhost:8545 --enable-preruntx=false --consensus-role=v0 --keyring-backend test >/Users/oker/workspace/exchain/dev/testnet/cache/val0.log 2>&1 &
}

runnode1(){
    echorun nohup exchaind start --home /Users/oker/workspace/exchain/dev/testnet/cache/node1/exchaind --p2p.seed_mode=false --p2p.allow_duplicate_ip --enable-dynamic-gp=false --enable-wtx=false --mempool.node_key_whitelist 0b066ca0790f27a6595560b23bf1a1193f100797,3813c7011932b18f27f172f0de2347871d27e852,6ea83a21a43c30a280a3139f6f23d737104b6975,bab6c32fa95f3a54ecb7d32869e32e85a25d2e08,testnet-node-ids --p2p.pex=false --p2p.addr_book_strict=false --p2p.seeds 0b066ca0790f27a6595560b23bf1a1193f100797@127.0.0.1:26656 --p2p.laddr tcp://127.0.0.1:26756 --rpc.laddr tcp://127.0.0.1:26757 --log_level main:info,*:error,consensus:error,state:info,distr:debug,gov:debug,staking:debug --chain-id exchain-67 --upload-delta=false --enable-gid --consensus.timeout_commit 6000ms --enable-blockpart-ack=false --block-part-size 16 --block-compress-type 0 --block-compress-flag 0 --block-compress-threshold 512 --append-pid=true --elapsed DeliverTxs=0,Round=1,CommitRound=1,Produce=1 --rest.laddr tcp://localhost:8645 --enable-preruntx=false --consensus-role=v1 --keyring-backend test >/Users/oker/workspace/exchain/dev/testnet/cache/val1.log 2>&1 &
}

runnode2(){
    echorun nohup exchaind start --home /Users/oker/workspace/exchain/dev/testnet/cache/node2/exchaind --p2p.seed_mode=false --p2p.allow_duplicate_ip --enable-dynamic-gp=false --enable-wtx=false --mempool.node_key_whitelist 0b066ca0790f27a6595560b23bf1a1193f100797,3813c7011932b18f27f172f0de2347871d27e852,6ea83a21a43c30a280a3139f6f23d737104b6975,bab6c32fa95f3a54ecb7d32869e32e85a25d2e08,testnet-node-ids --p2p.pex=false --p2p.addr_book_strict=false --p2p.seeds 0b066ca0790f27a6595560b23bf1a1193f100797@127.0.0.1:26656 --p2p.laddr tcp://127.0.0.1:26856 --rpc.laddr tcp://127.0.0.1:26857 --log_level main:info,*:error,consensus:error,state:info,distr:debug,gov:debug,staking:debug --chain-id exchain-67 --upload-delta=false --enable-gid --consensus.timeout_commit 6000ms --enable-blockpart-ack=false --block-part-size 16 --block-compress-type 0 --block-compress-flag 0 --block-compress-threshold 512 --append-pid=true --elapsed DeliverTxs=0,Round=1,CommitRound=1,Produce=1 --rest.laddr tcp://localhost:8745 --enable-preruntx=false --consensus-role=v2 --keyring-backend test  >/Users/oker/workspace/exchain/dev/testnet/cache/val2.log 2>&1 &
}

runnode3(){
    echorun nohup exchaind start --home /Users/oker/workspace/exchain/dev/testnet/cache/node3/exchaind --p2p.seed_mode=false --p2p.allow_duplicate_ip --enable-dynamic-gp=false --enable-wtx=false --mempool.node_key_whitelist 0b066ca0790f27a6595560b23bf1a1193f100797,3813c7011932b18f27f172f0de2347871d27e852,6ea83a21a43c30a280a3139f6f23d737104b6975,bab6c32fa95f3a54ecb7d32869e32e85a25d2e08,testnet-node-ids --p2p.pex=false --p2p.addr_book_strict=false --p2p.seeds 0b066ca0790f27a6595560b23bf1a1193f100797@127.0.0.1:26656 --p2p.laddr tcp://127.0.0.1:26956 --rpc.laddr tcp://127.0.0.1:26957 --log_level main:info,*:error,consensus:error,state:info,distr:debug,gov:debug,staking:debug --chain-id exchain-67 --upload-delta=false --enable-gid --consensus.timeout_commit 6000ms --enable-blockpart-ack=false --block-part-size 16 --block-compress-type 0 --block-compress-flag 0 --block-compress-threshold 512 --append-pid=true --elapsed DeliverTxs=0,Round=1,CommitRound=1,Produce=1 --rest.laddr tcp://localhost:8845 --enable-preruntx=false --consensus-role=v3 --keyring-backend test >/Users/oker/workspace/exchain/dev/testnet/cache/val3.log 2>&1 &
}

runnode4(){
    echorun nohup exchaind start --home /Users/oker/workspace/exchain/dev/testnet/cache/node4/exchaind --p2p.seed_mode=false --p2p.allow_duplicate_ip --enable-dynamic-gp=false --enable-wtx=false --mempool.node_key_whitelist 0b066ca0790f27a6595560b23bf1a1193f100797,3813c7011932b18f27f172f0de2347871d27e852,6ea83a21a43c30a280a3139f6f23d737104b6975,bab6c32fa95f3a54ecb7d32869e32e85a25d2e08,testnet-node-ids --p2p.pex=false --p2p.addr_book_strict=false --p2p.seeds 0b066ca0790f27a6595560b23bf1a1193f100797@127.0.0.1:26656 --p2p.laddr tcp://127.0.0.1:27056 --rpc.laddr tcp://127.0.0.1:27057 --log_level main:info,*:error,consensus:error,state:info,distr:debug,gov:debug,staking:debug --chain-id exchain-67 --upload-delta=false --enable-gid --consensus.timeout_commit 6000ms --enable-blockpart-ack=false --block-part-size 16 --block-compress-type 0 --block-compress-flag 0 --block-compress-threshold 512 --append-pid=true --elapsed DeliverTxs=0,Round=1,CommitRound=1,Produce=1 --rest.laddr tcp://localhost:8945 --enable-preruntx=false --consensus-role=v4 --keyring-backend test >/Users/oker/workspace/exchain/dev/testnet/cache/val4.log 2>&1 &
}

if [ $1 == "build" ];then
    echo "build my exchaind...."
    cd /Users/oker/workspace/exchain
    make install Venus1Height=1 SaturnHeight=1 Saturn1Height=1
    cd -
elif [ $1 == "build-dev" ];then
    cd /Users/oker/workspace/exchain-raw
    make install Venus1Height=1 SaturnHeight=1 Saturn1Height=1
    mv /Users/oker/go/bin//exchaind /Users/oker/go/bin//exchaind-dev 
    cd -
elif [ $1 == "init" ];then
    cd /Users/oker/workspace/exchain/dev/testnet
    ./run4v1r.sh 
    cd -
elif [ $1 == "start" ];then
    runnode0
    runnode1
    runnode2
    runnode3
    runnode4
elif [ $1 == "start0" ];then
    runnode0
elif [ $1 == "start1" ];then
    runnode1
elif [ $1 == "start2" ];then
    runnode2
elif [ $1 == "start3" ];then
    runnode3
elif [ $1 == "start4" ];then
    runnode4
elif [ $1 == "ps" ];then
    ps axu | grep exchaind
elif [ $1 == "stop" ];then
    killall exchaind
elif [ $1 == "ledger" ];then
    curHeight=`exchaincli status | grep "latest_block_height" | sed -r 's/.*"(.*)".*/\1/'`
    echo $curHeight
else
    echo "unknown cmd" $1 
fi
