#!/bin/bash

count=10
captain=ex1h0j8x0v9hs4eq6ppgamemfyu4vuvp2sl0q9p3v
admin18=ex17kn7d20d85yymu45h79dqs5pxq9m3nyx2mdmcs
seq1=$(curl http://127.0.0.1:8545/v1/auth/accounts/"${captain}" | jq ".value.sequence")
seq2=$(curl http://127.0.0.1:8545/v1/auth/accounts/"${admin18}" | jq ".value.sequence")
echo "the start nonce is" "seq1" $seq1 "seq2" $seq2

batchSendWrapReplaceCmtx() {
for i in $(seq 1 $count)
do
  okbchaincli tx send captain ex1dyxj3q9tzfkwrryejygqsfh7jj7cp4yuetcz3n 1okb --fees 1okb -b block -y --node tcp://127.0.0.1:26657 --chain-id okbchain-67 --wrapcmtx --broadcast-mode async --sequence $seq1
  seq1=$(expr $seq1 + 1)
  okbchaincli tx send captain ex1dyxj3q9tzfkwrryejygqsfh7jj7cp4yuetcz3n 1okb --fees 1okb -b block -y --node tcp://127.0.0.1:26657 --chain-id okbchain-67 --wrapcmtx --broadcast-mode async --sequence $seq1
  sleep 3
  okbchaincli tx send captain ex1dyxj3q9tzfkwrryejygqsfh7jj7cp4yuetcz3n 10okb --fees 2okb -b block -y --node tcp://127.0.0.1:26657 --chain-id okbchain-67 --wrapcmtx --broadcast-mode async --sequence $seq1
done
}

batchSendWrapReplaceCmtxCase2() {
for i in $(seq 1 $count)
do
  okbchaincli tx send captain ex1dyxj3q9tzfkwrryejygqsfh7jj7cp4yuetcz3n 1okb --fees 1okb -b block -y --node tcp://127.0.0.1:26657 --chain-id okbchain-67 --wrapcmtx --broadcast-mode async --sequence $seq1
  seq1=$(expr $seq1 + 1)
  okbchaincli tx send captain ex1dyxj3q9tzfkwrryejygqsfh7jj7cp4yuetcz3n 1okb --fees 2okb -b block -y --node tcp://127.0.0.1:26657 --chain-id okbchain-67 --wrapcmtx --broadcast-mode async --sequence $seq1
  sleep 3
  okbchaincli tx send captain ex1dyxj3q9tzfkwrryejygqsfh7jj7cp4yuetcz3n 10okb --fees 1okb -b block -y --node tcp://127.0.0.1:26657 --chain-id okbchain-67 --wrapcmtx --broadcast-mode async --sequence $seq1
done
}

batchSendWrapCmtx() {
for i in $(seq 1 $count)
do
  okbchaincli tx send captain ex1dyxj3q9tzfkwrryejygqsfh7jj7cp4yuetcz3n 1okb --fees 1okb -b block -y --node tcp://127.0.0.1:26657 --chain-id okbchain-67 --wrapcmtx --broadcast-mode async --sequence $seq1
  seq1=$(expr $seq1 + 1)
done
}

batchSendMixCmtx() {
  for i in $(seq 1 $count)
  do
    okbchaincli tx send captain ex1dyxj3q9tzfkwrryejygqsfh7jj7cp4yuetcz3n 1okb --fees 1okb -b block -y --node tcp://127.0.0.1:26657 --chain-id okbchain-67 --wrapcmtx --broadcast-mode async --sequence $seq1
    seq1=$(expr $seq1 + 1)
    okbchaincli tx send captain ex1dyxj3q9tzfkwrryejygqsfh7jj7cp4yuetcz3n 1okb --fees 1okb -b block -y --node tcp://127.0.0.1:26657 --chain-id okbchain-67 --broadcast-mode async --sequence $seq1
    seq1=$(expr $seq1 + 1)
  done
}

mutAddrBatchSendMixCmtx() {
  for i in $(seq 1 $count)
  do
    echo "ex1dyxj3q9tzfkwrryejygqsfh7jj7cp4yuetcz3n $seq1"
    okbchaincli tx send captain ex1dyxj3q9tzfkwrryejygqsfh7jj7cp4yuetcz3n 1okb --fees 1okb -b block -y --node tcp://127.0.0.1:26657 --chain-id okbchain-67 --wrapcmtx --broadcast-mode async --sequence $seq1
    seq1=$(expr $seq1 + 1)
    echo "ex1dyxj3q9tzfkwrryejygqsfh7jj7cp4yuetcz3n $seq1"
    okbchaincli tx send captain ex1dyxj3q9tzfkwrryejygqsfh7jj7cp4yuetcz3n 1okb --fees 1okb -b block -y --node tcp://127.0.0.1:26657 --chain-id okbchain-67 --broadcast-mode async --sequence $seq1
    seq1=$(expr $seq1 + 1)

    echo "**************************************************"

    echo "ex1j5mr2jhr9pf20e7yhln5zkcsgqtdt7cydr8x3y $seq2"
    okbchaincli tx send admin18 ex1j5mr2jhr9pf20e7yhln5zkcsgqtdt7cydr8x3y 1okb --fees 1okb -b block -y --node tcp://127.0.0.1:26657 --chain-id okbchain-67 --wrapcmtx --broadcast-mode async --sequence $seq2
    seq2=$(expr $seq2 + 1)
    echo "ex1j5mr2jhr9pf20e7yhln5zkcsgqtdt7cydr8x3y $seq2"
    okbchaincli tx send admin18 ex1j5mr2jhr9pf20e7yhln5zkcsgqtdt7cydr8x3y 1okb --fees 1okb -b block -y --node tcp://127.0.0.1:26657 --chain-id okbchain-67 --broadcast-mode async --sequence $seq2
    seq2=$(expr $seq2 + 1)

  done
}

# mempool.enable_pending_pool true
# mempool.pending_pool_size 1 Replace
# rpc 节点发送
# 手动发跳nonce， 5，6，4

# batchSendWrapReplaceCmtxCase2
# batchSendWrapReplaceCmtx
# batchSendWrapCmtx
# batchSendMixCmtx
mutAddrBatchSendMixCmtx
