# /usr/bin/env python3
# --coding:utf-8 --
import json
import logging
import os
import sys
import time
import requests
import base64

import pybase
import rpc

class CaseDistrProposal:
    def __init__(self, configObj):
        self.config = configObj
        self.okcli = rpc.OKCli("exchaind", "exchaincli")
    
        #读取主链合约
        # logging.info("CaseWasm...")
        # file = open(self.config["contract_path"], 'rb')
        # raw_code = base64.b64encode(file.read())
        # self.contract_code = str(raw_code,'utf-8')
        # print(self.config["contract_path"])
        #s = 'abcr34r344r'
        #a = base64.b64encode(s.encode('utf-8'))
        #print(str(self.contract_code,'utf-8'))
        #print(a)
        #exit()
        #file.close()

        return
    def test(self):
        # result = self.okcli.version("exchaincli")
        # logging.info("version: " + result)

        # result = self.okcli.get_ledger_seq()
        # logging.info("get_ledger_seq: " + str(result))

        # self.okcli.wait_ledger(100)


        # result = self.okcli.run_tx("exchaincli tx staking deposit 10okt --from admin16 --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y")
        # logging.info("run_tx: " + result)

        # self.okcli.kill_process("exchaind")

        # self.okcli.run_node("exchaind-my start --home /Users/oker/workspace/nodes/node0/exchaind --p2p.seed_mode=true --p2p.allow_duplicate_ip --enable-dynamic-gp=false --enable-wtx=false --mempool.node_key_whitelist 0b066ca0790f27a6595560b23bf1a1193f100797,3813c7011932b18f27f172f0de2347871d27e852,6ea83a21a43c30a280a3139f6f23d737104b6975,bab6c32fa95f3a54ecb7d32869e32e85a25d2e08,testnet-node-ids --p2p.pex=false --p2p.addr_book_strict=false --p2p.laddr tcp://127.0.0.1:26656 --rpc.laddr tcp://127.0.0.1:26657 --log_level main:info,*:error,consensus:error,state:info,distr:debug,gov:debug,staking:debug --chain-id exchain-67 --upload-delta=false --enable-gid --consensus.timeout_commit 6000ms --enable-blockpart-ack=false --block-part-size 16 --block-compress-type 0 --block-compress-flag 0 --block-compress-threshold 512 --append-pid=true --elapsed DeliverTxs=0,Round=1,CommitRound=1,Produce=1 --rest.laddr tcp://localhost:8545 --enable-preruntx=false --consensus-role=v0 --rpc.enable-multi-call --keyring-backend test >/Users/oker/workspace/nodes/val0.log 2>&1 &")

        # result = self.okcli.deposit(100, "admin16")
        # logging.info("run_tx: " + result)

        # result = self.okcli.add_shares("exvaloper1pt7xrmxul7sx54ml44lvv403r06clrdkehd8z7", "admin16")
        # logging.info("run_tx: " + result)

        # result = self.okcli.transfer("ex1h0j8x0v9hs4eq6ppgamemfyu4vuvp2sl0q9p3v", "ex1x8y59yxhk64mh0ct4h73fad2w5xap2zgq4f4kz", "100")
        # logging.info("run_tx: " + result)

        # result = self.okcli.proxy_reg("ex1j5mr2jhr9pf20e7yhln5zkcsgqtdt7cydr8x3y")
        # logging.info("run_tx: " + result)

        # result = self.okcli.proxy_bind("ex1j5mr2jhr9pf20e7yhln5zkcsgqtdt7cydr8x3y", "ex1dyxj3q9tzfkwrryejygqsfh7jj7cp4yuetcz3n")
        # logging.info("run_tx: " + result)

        # result = self.okcli.submit_change_type_proposal_offchain("ex1j5mr2jhr9pf20e7yhln5zkcsgqtdt7cydr8x3y")
        # logging.info("run_tx: " + result)

        # result = self.okcli.submit_change_type_proposal_onchain("ex1j5mr2jhr9pf20e7yhln5zkcsgqtdt7cydr8x3y")
        # logging.info("run_tx: " + result)

        # result = self.okcli.vote("ex1j5mr2jhr9pf20e7yhln5zkcsgqtdt7cydr8x3y", 1)
        # logging.info("run_tx: " + result)

        # result = self.okcli.withdraw_commission("exvaloper1pt7xrmxul7sx54ml44lvv403r06clrdkehd8z7", "va1")
        # logging.info("run_tx: " + result)

        # result = self.okcli.withdraw_rewards("exvaloper1pt7xrmxul7sx54ml44lvv403r06clrdkehd8z7", "ex1j5mr2jhr9pf20e7yhln5zkcsgqtdt7cydr8x3y")
        # logging.info("run_tx: " + result)

        # result = self.okcli.withdraw_all_rewards("ex1j5mr2jhr9pf20e7yhln5zkcsgqtdt7cydr8x3y")
        # logging.info("run_tx: " + result)

        # result = self.okcli.edit_validator("0.1", "va1")
        # logging.info("run_tx: " + result)

        # result = self.okcli.query_shares("ex1j5mr2jhr9pf20e7yhln5zkcsgqtdt7cydr8x3y")
        # logging.info("run_tx: " + json.dumps(result))

        # result = self.okcli.query_account("ex1j5mr2jhr9pf20e7yhln5zkcsgqtdt7cydr8x3y")
        # logging.info("run_tx: " + str(result))

        # result = self.okcli.query_commission("exvaloper1pt7xrmxul7sx54ml44lvv403r06clrdkehd8z7")
        # logging.info("run_tx: " + str(result))

        # result = self.okcli.query_rewards("ex1j5mr2jhr9pf20e7yhln5zkcsgqtdt7cydr8x3y", "")
        # logging.info("run_tx: " + str(result))

        # result = self.okcli.query_withdraw("ex1j5mr2jhr9pf20e7yhln5zkcsgqtdt7cydr8x3y")
        # logging.info("run_tx: " + str(result))

        # result = self.okcli.query_staking_validators()
        # logging.info("run_tx: " + str(result))

        # result = self.okcli.query_proposal(1)
        # logging.info("run_tx: " + json.dumps(result))

        # result = self.okcli.query_outstanding("exvaloper1pt7xrmxul7sx54ml44lvv403r06clrdkehd8z7")
        # logging.info("run_tx: " + result)

        # result = self.okcli.query_distr_params()
        # logging.info("run_tx: " + json.dumps(result))

        result = self.okcli.run_cmd("cd /Users/oker/workspace/exchain-raw/dev/testnet/;./run4v1r.sh")
        # logging.info("run_tx: " + result)

    def init_chain(self):
        logging.info("------------------------initChain start--------------------------------")
        # self.okcli.run_cmd("cd /Users/oker/workspace/exchain-raw/dev/testnet/;./run4v1r.sh")
        # time.sleep(2)
        # self.okcli.wait_ledger(1)
        # self.okcli.kill_process("exchaind")

        # # 迁移命令行和迁移文件夹，重新启动
        # self.okcli.run_cmd("rm -rf /Users/oker/workspace/nodes/*; cp -rf /Users/oker/workspace/exchain-raw/dev/testnet/cache/* /Users/oker/workspace/nodes/")
        # self.okcli.run_all_node()
        # assert self.okcli.version("exchaind") == "v1.6.0"

        # 导入委托人账户和代理人账户
        self.okcli.recover("delegator1", self.config["mnemonicdelegator1"])
        self.okcli.recover("delegator2", self.config["mnemonicdelegator2"])
        self.okcli.recover("delegator3", self.config["mnemonicdelegator3"])
        self.okcli.recover("delegator4", self.config["mnemonicdelegator4"])
        self.okcli.recover("delegator5", self.config["mnemonicdelegator5"])
        self.okcli.recover("delegator6", self.config["mnemonicdelegator6"])
        self.okcli.recover("delegator7", self.config["mnemonicdelegator7"])
        self.okcli.recover("delegator8", self.config["mnemonicdelegator8"])
        self.okcli.recover("delegator9", self.config["mnemonicdelegator9"])
        self.okcli.recover("delegator10", self.config["mnemonicdelegator10"])
        self.okcli.recover("proxy1", self.config["mnemonicproxy1"])
        self.okcli.recover("proxy2", self.config["mnemonicproxy2"])
        self.okcli.recover("proxy3", self.config["mnemonicproxy3"])
        self.okcli.recover("proxy4", self.config["mnemonicproxy4"])
        self.okcli.recover("proxy5", self.config["mnemonicproxy5"])
        self.okcli.recover("proxy6", self.config["mnemonicproxy6"])
        self.okcli.recover("proxydelegator1", self.config["mnemonicproxydelegator2"])
        self.okcli.recover("proxydelegator3", self.config["mnemonicproxydelegator3"])
        self.okcli.recover("proxydelegator4", self.config["mnemonicproxydelegator4"])
        self.okcli.recover("proxydelegator5", self.config["mnemonicproxydelegator5"])
        self.okcli.recover("proxydelegator6", self.config["mnemonicproxydelegator6"])

        self.okcli.recover_val("va1", self.config["mnemonicva1"])
        self.okcli.recover_val("va2", self.config["mnemonicva2"])
        self.okcli.recover_val("va3", self.config["mnemonicva3"])
        self.okcli.recover_val("va4", self.config["mnemonicva4"])

        self.okcli.transfer(self.config["captain"], self.config["delegator1"], 1000000)
        self.okcli.transfer(self.config["captain"], self.config["delegator2"], 1000000)
        self.okcli.transfer(self.config["captain"], self.config["delegator3"], 1000000)
        self.okcli.transfer(self.config["captain"], self.config["delegator4"], 1000000)
        self.okcli.transfer(self.config["captain"], self.config["delegator5"], 1000000)
        self.okcli.transfer(self.config["captain"], self.config["delegator6"], 1000000)
        self.okcli.transfer(self.config["captain"], self.config["delegator7"], 1000000)
        self.okcli.transfer(self.config["captain"], self.config["delegator8"], 1000000)
        self.okcli.transfer(self.config["captain"], self.config["delegator9"], 1000000)
        self.okcli.transfer(self.config["captain"], self.config["delegator10"], 1000000)
        self.okcli.transfer(self.config["captain"], self.config["proxy1"], 1000000)
        self.okcli.transfer(self.config["captain"], self.config["proxy2"], 1000000)
        self.okcli.transfer(self.config["captain"], self.config["proxy3"], 1000000)
        self.okcli.transfer(self.config["captain"], self.config["proxy4"], 1000000)
        self.okcli.transfer(self.config["captain"], self.config["proxy5"], 1000000)
        self.okcli.transfer(self.config["captain"], self.config["proxy6"], 1000000)
        self.okcli.transfer(self.config["captain"], self.config["proxydelegator1"], 1000000)
        self.okcli.transfer(self.config["captain"], self.config["proxydelegator2"], 1000000)
        self.okcli.transfer(self.config["captain"], self.config["proxydelegator3"], 1000000)
        self.okcli.transfer(self.config["captain"], self.config["proxydelegator4"], 1000000)
        self.okcli.transfer(self.config["captain"], self.config["proxydelegator5"], 1000000)
        self.okcli.transfer(self.config["captain"], self.config["proxydelegator6"], 1000000)


   
 
        


        logging.info("------------------------initChain end--------------------------------")
        return

#   common-send $captain $proxydelegator1 1000000 
#   common-send $captain $proxydelegator2 1000000 
#   common-send $captain $proxydelegator3 1000000 
#   common-send $captain $proxydelegator4 1000000 
#   common-send $captain $proxydelegator5 1000000 
#   common-send $captain $proxydelegator6 1000000 

#   common-query-account $delegator1
#   common-query-account $delegator2
#   common-query-account $delegator3
#   common-query-account $delegator4
#   common-query-account $delegator5
#   common-query-account $delegator6
#   common-query-account $delegator7
#   common-query-account $delegator8
#   common-query-account $delegator9
#   common-query-account $delegator10
#   common-query-account $proxy1
#   common-query-account $proxy2
#   echo '------------------------initChain end--------------------------------'
# }


    def all_contract(self):
        #创建合约
        address = self.deploy_contract()

        #chainload
        input_obj = {}
        input_obj["method"] = "chainload"
        input_obj["params"] = {}
        input_obj["params"]["a"] = 1
        input_obj["params"]["b"] = 2
        input = json.dumps(input_obj)

        tx_hash = self.rpc_genesis_address.pay(address, input, 0, 0, 0)
        logging.info(self.rpc_genesis_address.get_rpc() + "/getTransactionHistory?hash=" + tx_hash)
        assert self.rpc_genesis_address.is_success(tx_hash)
        

        #chainstore
        input_obj = {}
        input_obj["method"] = "chainstore"
        input_obj["params"] = {}
        input_obj["params"]["a"] = 1
        input_obj["params"]["b"] = 2
        input = json.dumps(input_obj)

        tx_hash = self.rpc_genesis_address.pay(address, input, 0, 0, 0)
        logging.info(self.rpc_genesis_address.get_rpc() + "/getTransactionHistory?hash=" + tx_hash)
        assert self.rpc_genesis_address.is_success(tx_hash)

        #chaindel
        input_obj = {}
        input_obj["method"] = "chaindel"
        input_obj["params"] = {}
        input_obj["params"]["a"] = 1
        input_obj["params"]["b"] = 2
        input = json.dumps(input_obj)

        tx_hash = self.rpc_genesis_address.pay(address, input, 0, 0, 0)
        logging.info(self.rpc_genesis_address.get_rpc() + "/getTransactionHistory?hash=" + tx_hash)
        assert self.rpc_genesis_address.is_success(tx_hash)

        #blockhash
        input_obj = {}
        input_obj["method"] = "blockhash"
        input_obj["params"] = {}
        input_obj["params"]["a"] = 1
        input_obj["params"]["b"] = 2
        input = json.dumps(input_obj)

        tx_hash = self.rpc_genesis_address.pay(address, input, 0, 0, 0)
        logging.info(self.rpc_genesis_address.get_rpc() + "/getTransactionHistory?hash=" + tx_hash)
        assert self.rpc_genesis_address.is_success(tx_hash)

        #chaintlog
        input_obj = {}
        input_obj["method"] = "chaintlog"
        input_obj["params"] = {}
        input_obj["params"]["a"] = 1
        input_obj["params"]["b"] = 2
        input = json.dumps(input_obj)

        tx_hash = self.rpc_genesis_address.pay(address, input, 0, 0, 0)
        logging.info(self.rpc_genesis_address.get_rpc() + "/getTransactionHistory?hash=" + tx_hash)
        assert self.rpc_genesis_address.is_success(tx_hash)

        #chainstore
        input_obj = {}
        input_obj["method"] = "chainstore"
        input_obj["params"] = {}
        input_obj["params"]["a"] = 1
        input_obj["params"]["b"] = 2
        input = json.dumps(input_obj)

        tx_hash = self.rpc_genesis_address.pay(address, input, 0, 0, 0)
        logging.info(self.rpc_genesis_address.get_rpc() + "/getTransactionHistory?hash=" + tx_hash)
        assert self.rpc_genesis_address.is_success(tx_hash)

        #metadata
        input_obj = {}
        input_obj["method"] = "metadata"
        input_obj["params"] = {}
        input_obj["params"]["a"] = 1
        input_obj["params"]["b"] = 2
        input = json.dumps(input_obj)

        tx_hash = self.rpc_genesis_address.pay(address, input, 0, 0, 0)
        logging.info(self.rpc_genesis_address.get_rpc() + "/getTransactionHistory?hash=" + tx_hash)
        assert self.rpc_genesis_address.is_success(tx_hash)


        #balance
        input_obj = {}
        input_obj["method"] = "balance"
        input_obj["params"] = {}
        input_obj["params"]["a"] = 1
        input_obj["params"]["b"] = 2
        input = json.dumps(input_obj)

        tx_hash = self.rpc_genesis_address.pay(address, input, 0, 0, 0)
        logging.info(self.rpc_genesis_address.get_rpc() + "/getTransactionHistory?hash=" + tx_hash)
        assert self.rpc_genesis_address.is_success(tx_hash)

        #paycoin
        input_obj = {}
        input_obj["method"] = "paycoin"
        input_obj["params"] = {}
        input_obj["params"]["a"] = 1
        input_obj["params"]["b"] = 2
        input = json.dumps(input_obj)

        tx_hash = self.rpc_genesis_address.pay(address, input, 0, 0, 0)
        logging.info(self.rpc_genesis_address.get_rpc() + "/getTransactionHistory?hash=" + tx_hash)
        assert self.rpc_genesis_address.is_success(tx_hash)

        #timestamp
        input_obj = {}
        input_obj["method"] = "timestamp"
        input_obj["params"] = {}
        input_obj["params"]["a"] = 1
        input_obj["params"]["b"] = 2
        input = json.dumps(input_obj)

        tx_hash = self.rpc_genesis_address.pay(address, input, 0, 0, 0)
        logging.info(self.rpc_genesis_address.get_rpc() + "/getTransactionHistory?hash=" + tx_hash)
        assert self.rpc_genesis_address.is_success(tx_hash)

        #number
        input_obj = {}
        input_obj["method"] = "number"
        input_obj["params"] = {}
        input_obj["params"]["a"] = 1
        input_obj["params"]["b"] = 2
        input = json.dumps(input_obj)

        tx_hash = self.rpc_genesis_address.pay(address, input, 0, 0, 0)
        logging.info(self.rpc_genesis_address.get_rpc() + "/getTransactionHistory?hash=" + tx_hash)
        assert self.rpc_genesis_address.is_success(tx_hash)

        #txinitiator
        input_obj = {}
        input_obj["method"] = "txinitiator"
        input_obj["params"] = {}
        input_obj["params"]["a"] = 1
        input_obj["params"]["b"] = 2
        input = json.dumps(input_obj)

        tx_hash = self.rpc_genesis_address.pay(address, input, 0, 0, 0)
        logging.info(self.rpc_genesis_address.get_rpc() + "/getTransactionHistory?hash=" + tx_hash)
        assert self.rpc_genesis_address.is_success(tx_hash)

        #txsender
        input_obj = {}
        input_obj["method"] = "txsender"
        input_obj["params"] = {}
        input_obj["params"]["a"] = 1
        input_obj["params"]["b"] = 2
        input = json.dumps(input_obj)

        tx_hash = self.rpc_genesis_address.pay(address, input, 0, 0, 0)
        logging.info(self.rpc_genesis_address.get_rpc() + "/getTransactionHistory?hash=" + tx_hash)
        assert self.rpc_genesis_address.is_success(tx_hash)

        #txgasprice
        input_obj = {}
        input_obj["method"] = "txgasprice"
        input_obj["params"] = {}
        input_obj["params"]["a"] = 1
        input_obj["params"]["b"] = 2
        input = json.dumps(input_obj)

        tx_hash = self.rpc_genesis_address.pay(address, input, 0, 0, 0)
        logging.info(self.rpc_genesis_address.get_rpc() + "/getTransactionHistory?hash=" + tx_hash)
        assert self.rpc_genesis_address.is_success(tx_hash)


        #txhash
        input_obj = {}
        input_obj["method"] = "txhash"
        input_obj["params"] = {}
        input_obj["params"]["a"] = 1
        input_obj["params"]["b"] = 2
        input = json.dumps(input_obj)

        tx_hash = self.rpc_genesis_address.pay(address, input, 0, 0, 0)
        logging.info(self.rpc_genesis_address.get_rpc() + "/getTransactionHistory?hash=" + tx_hash)
        assert self.rpc_genesis_address.is_success(tx_hash)

        #txfeelimit
        input_obj = {}
        input_obj["method"] = "txfeelimit"
        input_obj["params"] = {}
        input_obj["params"]["a"] = 1
        input_obj["params"]["b"] = 2
        input = json.dumps(input_obj)

        tx_hash = self.rpc_genesis_address.pay(address, input, 0, 0, 0)
        logging.info(self.rpc_genesis_address.get_rpc() + "/getTransactionHistory?hash=" + tx_hash)
        assert self.rpc_genesis_address.is_success(tx_hash)

        #msginitiator
        input_obj = {}
        input_obj["method"] = "msginitiator"
        input_obj["params"] = {}
        input_obj["params"]["a"] = 1
        input_obj["params"]["b"] = 2
        input = json.dumps(input_obj)

        tx_hash = self.rpc_genesis_address.pay(address, input, 0, 0, 0)
        logging.info(self.rpc_genesis_address.get_rpc() + "/getTransactionHistory?hash=" + tx_hash)
        assert self.rpc_genesis_address.is_success(tx_hash)

        #msgsender
        input_obj = {}
        input_obj["method"] = "msgsender"
        input_obj["params"] = {}
        input_obj["params"]["a"] = 1
        input_obj["params"]["b"] = 2
        input = json.dumps(input_obj)

        tx_hash = self.rpc_genesis_address.pay(address, input, 0, 0, 0)
        logging.info(self.rpc_genesis_address.get_rpc() + "/getTransactionHistory?hash=" + tx_hash)
        assert self.rpc_genesis_address.is_success(tx_hash)

        #coinamount
        input_obj = {}
        input_obj["method"] = "coinamount"
        input_obj["params"] = {}
        input_obj["params"]["a"] = 1
        input_obj["params"]["b"] = 2
        input = json.dumps(input_obj)

        tx_hash = self.rpc_genesis_address.pay(address, input, 0, 0, 0)
        logging.info(self.rpc_genesis_address.get_rpc() + "/getTransactionHistory?hash=" + tx_hash)
        assert self.rpc_genesis_address.is_success(tx_hash)

        #msgnonce
        input_obj = {}
        input_obj["method"] = "msgnonce"
        input_obj["params"] = {}
        input_obj["params"]["a"] = 1
        input_obj["params"]["b"] = 2
        input = json.dumps(input_obj)

        tx_hash = self.rpc_genesis_address.pay(address, input, 0, 0, 0)
        logging.info(self.rpc_genesis_address.get_rpc() + "/getTransactionHistory?hash=" + tx_hash)
        assert self.rpc_genesis_address.is_success(tx_hash)

        #operationidx
        input_obj = {}
        input_obj["method"] = "operationidx"
        input_obj["params"] = {}
        input_obj["params"]["a"] = 1
        input_obj["params"]["b"] = 2
        input = json.dumps(input_obj)

        tx_hash = self.rpc_genesis_address.pay(address, input, 0, 0, 0)
        logging.info(self.rpc_genesis_address.get_rpc() + "/getTransactionHistory?hash=" + tx_hash)
        assert self.rpc_genesis_address.is_success(tx_hash)

        #thisaddress
        input_obj = {}
        input_obj["method"] = "thisaddress"
        input_obj["params"] = {}
        input_obj["params"]["a"] = 1
        input_obj["params"]["b"] = 2
        input = json.dumps(input_obj)

        tx_hash = self.rpc_genesis_address.pay(address, input, 0, 0, 0)
        logging.info(self.rpc_genesis_address.get_rpc() + "/getTransactionHistory?hash=" + tx_hash)
        assert self.rpc_genesis_address.is_success(tx_hash)

        #utilslog
        input_obj = {}
        input_obj["method"] = "utilslog"
        input_obj["params"] = {}
        input_obj["params"]["a"] = 1
        input_obj["params"]["b"] = 2
        input = json.dumps(input_obj)

        tx_hash = self.rpc_genesis_address.pay(address, input, 0, 0, 0)
        logging.info(self.rpc_genesis_address.get_rpc() + "/getTransactionHistory?hash=" + tx_hash)
        assert self.rpc_genesis_address.is_success(tx_hash)
        
        #intadd
        input_obj = {}
        input_obj["method"] = "intadd"
        input_obj["params"] = {}
        input_obj["params"]["a"] = 1
        input_obj["params"]["b"] = 2
        input = json.dumps(input_obj)

        tx_hash = self.rpc_genesis_address.pay(address, input, 0, 0, 0)
        logging.info(self.rpc_genesis_address.get_rpc() + "/getTransactionHistory?hash=" + tx_hash)
        assert self.rpc_genesis_address.is_success(tx_hash)

        #intsub
        input_obj = {}
        input_obj["method"] = "intsub"
        input_obj["params"] = {}
        input_obj["params"]["a"] = 1
        input_obj["params"]["b"] = 2
        input = json.dumps(input_obj)

        tx_hash = self.rpc_genesis_address.pay(address, input, 0, 0, 0)
        logging.info(self.rpc_genesis_address.get_rpc() + "/getTransactionHistory?hash=" + tx_hash)
        assert self.rpc_genesis_address.is_success(tx_hash)

        #intmul
        input_obj = {}
        input_obj["method"] = "intmul"
        input_obj["params"] = {}
        input_obj["params"]["a"] = 1
        input_obj["params"]["b"] = 2
        input = json.dumps(input_obj)

        tx_hash = self.rpc_genesis_address.pay(address, input, 0, 0, 0)
        logging.info(self.rpc_genesis_address.get_rpc() + "/getTransactionHistory?hash=" + tx_hash)
        assert self.rpc_genesis_address.is_success(tx_hash)

        #intmod
        input_obj = {}
        input_obj["method"] = "intmod"
        input_obj["params"] = {}
        input_obj["params"]["a"] = 1
        input_obj["params"]["b"] = 2
        input = json.dumps(input_obj)

        tx_hash = self.rpc_genesis_address.pay(address, input, 0, 0, 0)
        logging.info(self.rpc_genesis_address.get_rpc() + "/getTransactionHistory?hash=" + tx_hash)
        assert self.rpc_genesis_address.is_success(tx_hash)

        #intdiv
        input_obj = {}
        input_obj["method"] = "intdiv"
        input_obj["params"] = {}
        input_obj["params"]["a"] = 1
        input_obj["params"]["b"] = 2
        input = json.dumps(input_obj)

        tx_hash = self.rpc_genesis_address.pay(address, input, 0, 0, 0)
        logging.info(self.rpc_genesis_address.get_rpc() + "/getTransactionHistory?hash=" + tx_hash)
        assert self.rpc_genesis_address.is_success(tx_hash)

        #addresscheck
        input_obj = {}
        input_obj["method"] = "addresscheck"
        input_obj["params"] = {}
        input_obj["params"]["a"] = 1
        input_obj["params"]["b"] = 2
        input = json.dumps(input_obj)

        tx_hash = self.rpc_genesis_address.pay(address, input, 0, 0, 0)
        logging.info(self.rpc_genesis_address.get_rpc() + "/getTransactionHistory?hash=" + tx_hash)
        assert self.rpc_genesis_address.is_success(tx_hash)

def exit():
    logging.info("Please use arg eg:  deploy do all")
    sys.exit()

if __name__ == '__main__':
    pybase = pybase.Pybase()

    if len(sys.argv) < 2:
        exit()

    file = open('config/case_distr_proposal.json', 'r', encoding='UTF-8')
    moduleConfig = json.loads(file.read())
    file.close()
    case = CaseDistrProposal(moduleConfig)
    opt = sys.argv[1]
    if opt == "test":
        case.test()
    elif opt == "all":
        case.init_chain()
    else:
        exit()
