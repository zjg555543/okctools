#!/usr/bin/env bash

echorun() {
  beginHeight=`exchaincli status | grep "latest_block_height" | sed -r 's/.*"(.*)".*/\1/'`
  echo "Waiting..."
  for((i=1;i<=10;i++));
  do
      sleep 1
      curHeight=`exchaincli status | grep "latest_block_height" | sed -r 's/.*"(.*)".*/\1/'`
      if [ $curHeight -gt $beginHeight ]
      then
  #      echo $curHeight
  #      echo "Mint a new block now."
        break
  #    else
  #      echo "Waiting a new block, cur height:" $curHeight
      fi
  done
  echo "------------------------------------------------------------------------------------------------"
  echo "["$@"]"
  $@
  echo "------------------------------------------------------------------------------------------------"
}

echorun exchaincli tx gov submit-proposal community-pool-spend proposal.json --from admin16 --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y

echorun exchaincli query gov proposal 1

echorun exchaincli tx staking deposit 100000000okt --from admin16 --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y

echorun exchaincli tx staking add-shares exvaloper1pt7xrmxul7sx54ml44lvv403r06clrdkehd8z7 --from admin16 --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y

echorun exchaincli tx gov vote 1 yes --from va1 --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y

echorun exchaincli query gov proposal 1
