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

    def all(self):
        self.init_chain()
        self.init_staking()
        self.upgrate_bin_staking()
        self.upgrate_ledger_staking()
        self.after_distr_proposal()
        self.change_to_off_chain()
        self.change_to_on_chain()

    def init_chain(self):
        logging.info("------------------------initChain start--------------------------------")
        self.okcli.run_cmd("cd /Users/oker/workspace/exchain-raw/dev/testnet/;./run4v1r.sh")
        time.sleep(2)
        self.okcli.wait_ledger(1)
        self.okcli.kill_process("exchaind")

        # 迁移命令行和迁移文件夹，重新启动
        self.okcli.run_cmd("rm -rf /Users/oker/workspace/nodes/*; cp -rf /Users/oker/workspace/exchain-raw/dev/testnet/cache/* /Users/oker/workspace/nodes/")
        self.okcli.run_all_node()
        assert self.okcli.version("exchaind") == "v1.6.0"

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
        self.okcli.query_account(self.config["delegator1"])
        self.okcli.query_account(self.config["delegator2"])
        self.okcli.query_account(self.config["delegator3"])
        self.okcli.query_account(self.config["delegator4"])
        self.okcli.query_account(self.config["delegator5"])
        self.okcli.query_account(self.config["delegator6"])
        self.okcli.query_account(self.config["delegator7"])
        self.okcli.query_account(self.config["delegator8"])
        self.okcli.query_account(self.config["delegator9"])
        self.okcli.query_account(self.config["delegator10"])
        self.okcli.query_account(self.config["proxy1"])
        self.okcli.query_account(self.config["proxy2"])
        self.okcli.query_account(self.config["proxy3"])
        self.okcli.query_account(self.config["proxy4"])
        self.okcli.query_account(self.config["proxy5"])
        self.okcli.query_account(self.config["proxy6"])
        self.okcli.query_account(self.config["proxydelegator1"])
        self.okcli.query_account(self.config["proxydelegator2"])
        self.okcli.query_account(self.config["proxydelegator3"])
        self.okcli.query_account(self.config["proxydelegator4"])
        self.okcli.query_account(self.config["proxydelegator5"])
        self.okcli.query_account(self.config["proxydelegator6"])

        logging.info("------------------------initChain end--------------------------------")
        return
    def init_staking(self):
        self.okcli.kill_process("exchaind")
        self.okcli.run_all_node()
        time.sleep(3)

        logging.info("------------------------initStaking start--------------------------------")
        self.okcli.query_staking_validators()
        self.okcli.deposit(10000, self.config["delegator1"])
        self.okcli.add_shares(self.config["va1"], self.config["delegator1"])
        self.okcli.deposit(10000, self.config["proxydelegator1"])
        self.okcli.query_shares(self.config["delegator1"])
        self.okcli.query_shares(self.config["proxydelegator1"])

        self.okcli.query_commission(self.config["va1"])
        self.okcli.query_commission(self.config["va2"])
        self.okcli.query_commission(self.config["va3"])
        self.okcli.query_commission(self.config["va4"])

        # 注册代理1,绑定委托人2
        self.okcli.deposit(10000, self.config["proxy1"])
        vals = self.config["va1"] + "," + self.config["va2"] + "," + self.config["va3"] + "," + self.config["va4"]
        self.okcli.add_shares(vals, self.config["proxy1"])
        self.okcli.proxy_reg(self.config["proxy1"])
        self.okcli.proxy_bind(self.config["proxy1"], self.config["proxydelegator1"])

        logging.info("------------------------initStaking end--------------------------------")
    def upgrate_bin_staking(self):
        self.okcli.kill_process("exchaind")
        self.okcli.run_all_node()
        time.sleep(3)

        logging.info("------------------------upgrate_bin_staking start--------------------------------")

        # 编译新的的4个节点，运行
        self.okcli.run_cmd("cd /Users/oker/workspace/exchain/dev/testnet/;./run4v1r.sh")
        time.sleep(2)
        self.okcli.wait_ledger(1)
        self.okcli.kill_process("exchaind")

        self.okcli.run_all_node()
        assert self.okcli.version("exchaind") == "v1.6.1"
        time.sleep(5)
        # 使用新的程序，1个委托人 + 1个代理1（1个委托人）
        self.okcli.query_staking_validators()
        self.okcli.deposit(10000, self.config["delegator2"])
        self.okcli.add_shares(self.config["va1"], self.config["delegator2"])
        self.okcli.deposit(10000, self.config["proxydelegator2"])
        self.okcli.query_shares(self.config["delegator2"])
        self.okcli.query_shares(self.config["proxydelegator2"])

        self.okcli.add_shares(self.config["va1"], self.config["delegator2"])

        # 注册代理2,绑定委托人2
        self.okcli.deposit(10000, self.config["proxy2"])
        vals = self.config["va1"] + "," + self.config["va2"] + "," + self.config["va3"] + "," + self.config["va4"]
        self.okcli.add_shares(vals, self.config["proxy2"])
        self.okcli.proxy_reg(self.config["proxy2"])
        self.okcli.proxy_bind(self.config["proxy2"], self.config["proxydelegator2"])

        logging.info("------------------------upgrate_bin_staking end--------------------------------")
    def upgrate_ledger_staking(self):
        self.okcli.kill_process("exchaind")
        self.okcli.run_all_node()
        time.sleep(3)
        assert self.okcli.version("exchaind") == "v1.6.1"

        logging.info("------------------------upgrate_ledger_staking start--------------------------------")
        # 新的程序启动，区块升级之后，没有投票提案，仍然按照佣金100%提成计算，查询验证节点投票仍然可用，验证节点取款仍然有效
        self.okcli.wait_ledger(50)
        self.okcli.query_commission(self.config["va1"])
        self.okcli.query_commission(self.config["va2"])
        self.okcli.query_commission(self.config["va3"])
        self.okcli.query_commission(self.config["va4"])

        self.okcli.query_staking_validators()
        self.okcli.deposit(10000, self.config["delegator3"])
        self.okcli.add_shares(self.config["va1"], self.config["delegator3"])

        self.okcli.deposit(10000, self.config["proxydelegator3"])
        self.okcli.query_shares(self.config["delegator3"])
        self.okcli.query_shares(self.config["proxydelegator3"])

        self.okcli.add_shares(self.config["va1"], self.config["delegator2"])

        # 注册代理2,绑定委托人2
        self.okcli.deposit(10000, self.config["proxy3"])
        vals = self.config["va1"] + "," + self.config["va2"] + "," + self.config["va3"] + "," + self.config["va4"]
        self.okcli.add_shares(vals, self.config["proxy3"])
        self.okcli.proxy_reg(self.config["proxy3"])
        self.okcli.proxy_bind(self.config["proxy3"], self.config["proxydelegator3"])

        logging.info("------------------------upgrate_ledger_staking end--------------------------------")

    def after_distr_proposal(self):
        self.okcli.kill_process("exchaind")
        self.okcli.run_all_node()
        assert self.okcli.version("exchaind") == "v1.6.1"
        time.sleep(5)

        logging.info("------------------------after_distr_proposal start--------------------------------")
        # 发起投票提案，修改提案，此时分红比例默认为100%，各个接口可以使用，验证节点查询抽成，提取抽成正常；委托人查询分红为0；代理人查询为0，无法提取抽成；
        self.okcli.wait_ledger(65)
        self.okcli.submit_change_type_proposal_onchain(self.config["delegator1"])
        proposal_num=1
        self.okcli.query_proposal(proposal_num)
        self.okcli.vote(self.config["delegator1"], proposal_num)
        self.okcli.vote(self.config["delegator2"], proposal_num)
        self.okcli.vote(self.config["delegator3"], proposal_num)
        self.okcli.vote(self.config["proxy1"], proposal_num)
        self.okcli.vote(self.config["proxy2"], proposal_num)
        self.okcli.vote(self.config["proxy3"], proposal_num)
        self.okcli.query_proposal(proposal_num)

        # 查询抽成
        self.okcli.query_commission(self.config["va1"])
        self.okcli.query_commission(self.config["va2"])
        self.okcli.query_commission(self.config["va3"])
        self.okcli.query_commission(self.config["va4"])

        self.okcli.query_outstanding(self.config["va1"])
        self.okcli.query_outstanding(self.config["va2"])
        self.okcli.query_outstanding(self.config["va3"])
        self.okcli.query_outstanding(self.config["va4"])

        # 查询奖励
        self.okcli.query_rewards(self.config["proxy1"], "")
        self.okcli.query_rewards(self.config["proxy2"], "")
        self.okcli.query_rewards(self.config["proxy3"], "")

        self.okcli.query_rewards(self.config["delegator1"], "")
        self.okcli.query_rewards(self.config["delegator2"], "")
        self.okcli.query_rewards(self.config["delegator3"], "")

        # 验证节点提取奖励
        self.okcli.withdraw_commission(self.config["va1"], "va1")
        self.okcli.withdraw_commission(self.config["va2"], "va2")

        # 代理人提取分红
        self.okcli.withdraw_rewards(self.config["va1"], self.config["proxy1"])
        self.okcli.withdraw_rewards(self.config["va1"], self.config["delegator1"])

        # 验证节点1 设置分红比例30%
        self.okcli.edit_validator("0.1", "va1")
        time.sleep(15)

        self.okcli.query_rewards(self.config["proxy1"], "")
        self.okcli.query_rewards(self.config["proxy2"], "")
        self.okcli.query_rewards(self.config["proxy3"], "")

        self.okcli.query_rewards(self.config["delegator1"], "")
        self.okcli.query_rewards(self.config["delegator2"], "")
        self.okcli.query_rewards(self.config["delegator3"], "")

        # 验证节点提取奖励
        self.okcli.withdraw_commission(self.config["va1"], "va1")
        self.okcli.withdraw_commission(self.config["va2"], "va1")

        # 提取分红
        self.okcli.withdraw_rewards(self.config["va1"], self.config["proxy1"])
        self.okcli.withdraw_rewards(self.config["va1"], self.config["delegator1"])

        # 投票分红
        self.okcli.query_staking_validators()

        # 查询抽成
        self.okcli.query_commission(self.config["va1"])
        self.okcli.query_commission(self.config["va2"])
        self.okcli.query_commission(self.config["va3"])
        self.okcli.query_commission(self.config["va4"])

        self.okcli.query_outstanding(self.config["va1"])
        self.okcli.query_outstanding(self.config["va2"])
        self.okcli.query_outstanding(self.config["va3"])
        self.okcli.query_outstanding(self.config["va4"])

        # 验证节点提取奖励
        self.okcli.withdraw_commission(self.config["va1"], "va1")
        self.okcli.withdraw_commission(self.config["va2"], "va2")
        self.okcli.withdraw_commission(self.config["va3"], "va3")
        self.okcli.withdraw_commission(self.config["va4"], "va4")

        # 取出所有分红
        self.okcli.withdraw_all_rewards(self.config["proxy1"])
        self.okcli.withdraw_all_rewards(self.config["proxy2"])
        self.okcli.withdraw_all_rewards(self.config["proxy3"])
        self.okcli.withdraw_all_rewards(self.config["delegator1"])
        self.okcli.withdraw_all_rewards(self.config["delegator2"])
        self.okcli.withdraw_all_rewards(self.config["delegator3"])

        # 重新质押，继续以上所有操作，可正常使用 + 委托人5 + 代理3（绑定委托人6），出到100个区块暂停
        self.okcli.query_staking_validators()

        self.okcli.deposit(10000, self.config["proxy4"])
        self.okcli.add_shares(self.config["va1"], self.config["proxy4"])

        self.okcli.deposit(10000, self.config["delegator4"])
        self.okcli.add_shares(self.config["va1"], self.config["delegator4"])

        self.okcli.deposit(10000, self.config["proxydelegator4"])

        self.okcli.query_shares( self.config["proxydelegator4"])
        self.okcli.query_shares( self.config["delegator4"])
        self.okcli.query_shares( self.config["proxy4"])

        vals = self.config["va1"] + "," + self.config["va2"] + "," + self.config["va3"] + "," + self.config["va4"]
        self.okcli.add_shares(vals, self.config["proxy4"])
        self.okcli.proxy_reg(self.config["proxy4"])
        self.okcli.proxy_bind(self.config["proxy4"], self.config["proxydelegator4"])

        logging.info("------------------------after_distr_proposal end--------------------------------")

    def change_to_off_chain(self):
        self.okcli.kill_process("exchaind")
        self.okcli.run_all_node()
        assert self.okcli.version("exchaind") == "v1.6.1"
        time.sleep(5)

        logging.info("------------------------change_to_off_chain start--------------------------------")
        # 修改成链下分红
        self.okcli.submit_change_type_proposal_offchain(self.config["delegator1"])
        proposal_num=2
        self.okcli.query_proposal(proposal_num)
        self.okcli.vote(self.config["delegator1"], proposal_num)
        self.okcli.vote(self.config["delegator2"], proposal_num)
        self.okcli.vote(self.config["delegator3"], proposal_num)
        self.okcli.vote(self.config["delegator4"], proposal_num)
        self.okcli.vote(self.config["proxy1"], proposal_num)
        self.okcli.vote(self.config["proxy2"], proposal_num)
        self.okcli.vote(self.config["proxy3"], proposal_num)
        self.okcli.vote(self.config["proxy4"], proposal_num)
        self.okcli.query_proposal(proposal_num)

        # 正常提取分红
        self.okcli.withdraw_all_rewards(self.config["proxy1"])
        self.okcli.withdraw_all_rewards(self.config["proxy2"])
        self.okcli.withdraw_all_rewards(self.config["proxy3"])
        self.okcli.withdraw_all_rewards(self.config["delegator1"])
        self.okcli.withdraw_all_rewards(self.config["delegator2"])
        self.okcli.withdraw_all_rewards(self.config["delegator3"])

        # 重新质押，继续以上所有操作，可正常使用 + 委托人5 + 代理3（绑定委托人6），出到100个区块暂停
        self.okcli.query_staking_validators()
        self.okcli.deposit(10000, self.config["delegator5"])
        self.okcli.add_shares(self.config["va1"], self.config["delegator5"])

        self.okcli.deposit(10000, self.config["proxydelegator5"])

        self.okcli.query_shares( self.config["proxydelegator5"])
        self.okcli.query_shares( self.config["delegator5"])

        # 验证节点提取奖励
        self.okcli.withdraw_commission(self.config["va1"], "va1")
        self.okcli.withdraw_commission(self.config["va2"], "va2")
        self.okcli.withdraw_commission(self.config["va3"], "va3")
        self.okcli.withdraw_commission(self.config["va4"], "va4")

        # 注册代理3,绑定委托人6
        self.okcli.deposit(10000, self.config["proxy5"])
        vals = self.config["va1"] + "," + self.config["va2"] + "," + self.config["va3"] + "," + self.config["va4"]
        self.okcli.add_shares(vals, self.config["proxy5"])
        self.okcli.proxy_reg(self.config["proxy5"])
        self.okcli.proxy_bind(self.config["proxy5"], self.config["proxydelegator5"])

        # 查询抽成
        self.okcli.query_commission(self.config["va1"])
        self.okcli.query_commission(self.config["va2"])
        self.okcli.query_commission(self.config["va3"])
        self.okcli.query_commission(self.config["va4"])

        self.okcli.query_outstanding(self.config["va1"])
        self.okcli.query_outstanding(self.config["va2"])
        self.okcli.query_outstanding(self.config["va3"])
        self.okcli.query_outstanding(self.config["va4"])

        self.okcli.query_rewards(self.config["proxy1"], "")
        self.okcli.query_rewards(self.config["proxy2"], "")
        self.okcli.query_rewards(self.config["proxy3"], "")
        self.okcli.query_rewards(self.config["proxy4"], "")
        self.okcli.query_rewards(self.config["proxy5"], "")

        self.okcli.query_rewards(self.config["delegator1"], "")
        self.okcli.query_rewards(self.config["delegator2"], "")
        self.okcli.query_rewards(self.config["delegator3"], "")
        self.okcli.query_rewards(self.config["delegator4"], "")
        self.okcli.query_rewards(self.config["delegator5"], "")

        # 取出所有分红
        self.okcli.withdraw_all_rewards(self.config["delegator1"])
        self.okcli.withdraw_all_rewards(self.config["delegator2"])
        self.okcli.withdraw_all_rewards(self.config["delegator3"])
        self.okcli.withdraw_all_rewards(self.config["delegator4"])
        self.okcli.withdraw_all_rewards(self.config["delegator5"])

        self.okcli.withdraw_rewards(self.config["va1"], self.config["proxy1"])
        self.okcli.withdraw_rewards(self.config["va1"], self.config["proxy2"])
        self.okcli.withdraw_rewards(self.config["va1"], self.config["proxy3"])
        self.okcli.withdraw_rewards(self.config["va1"], self.config["proxy4"])
        self.okcli.withdraw_rewards(self.config["va1"], self.config["proxy5"])

        self.okcli.query_distr_params()

        logging.info("------------------------change_to_off_chain end--------------------------------")

    def change_to_on_chain(self):
        self.okcli.run_all_node()
        assert self.okcli.version("exchaind") == "v1.6.1"
        time.sleep(5)

        logging.info("------------------------change_to_on_chain end--------------------------------")
        # 发起投票提案，修改提案链上分红
        self.okcli.submit_change_type_proposal_onchain(self.config["delegator1"])
        proposal_num=3
        self.okcli.query_proposal(proposal_num)
        self.okcli.vote(self.config["delegator1"], proposal_num)
        self.okcli.vote(self.config["delegator2"], proposal_num)
        self.okcli.vote(self.config["delegator3"], proposal_num)
        self.okcli.vote(self.config["delegator4"], proposal_num)
        self.okcli.vote(self.config["delegator5"], proposal_num)
        self.okcli.vote(self.config["proxy1"], proposal_num)
        self.okcli.vote(self.config["proxy2"], proposal_num)
        self.okcli.vote(self.config["proxy3"], proposal_num)
        self.okcli.vote(self.config["proxy4"], proposal_num)
        # self.okcli.vote(self.config["proxy5"], proposal_num)
        self.okcli.query_proposal(proposal_num)

        # 正常提取分红
        self.okcli.withdraw_all_rewards(self.config["proxy1"])
        self.okcli.withdraw_all_rewards(self.config["proxy2"])
        self.okcli.withdraw_all_rewards(self.config["proxy3"])
        self.okcli.withdraw_all_rewards(self.config["delegator1"])
        self.okcli.withdraw_all_rewards(self.config["delegator2"])
        self.okcli.withdraw_all_rewards(self.config["delegator3"])

        self.okcli.query_staking_validators()
        self.okcli.deposit(10000, self.config["delegator6"])
        self.okcli.add_shares(self.config["va1"], self.config["delegator6"])

        self.okcli.deposit(10000, self.config["proxydelegator6"])

        self.okcli.query_shares( self.config["proxydelegator6"])
        self.okcli.query_shares( self.config["delegator6"])

        self.okcli.deposit(10000, self.config["proxy6"])
        vals = self.config["va1"] + "," + self.config["va2"] + "," + self.config["va3"] + "," + self.config["va4"]
        self.okcli.add_shares(vals, self.config["proxy6"])
        self.okcli.proxy_reg(self.config["proxy6"])
        self.okcli.proxy_bind(self.config["proxy6"], self.config["proxydelegator6"])

        # 查询抽成
        self.okcli.query_commission(self.config["va1"])
        self.okcli.query_commission(self.config["va2"])
        self.okcli.query_commission(self.config["va3"])
        self.okcli.query_commission(self.config["va4"])

        self.okcli.query_outstanding(self.config["va1"])
        self.okcli.query_outstanding(self.config["va2"])
        self.okcli.query_outstanding(self.config["va3"])
        self.okcli.query_outstanding(self.config["va4"])

        self.okcli.query_rewards(self.config["proxy1"], "")
        self.okcli.query_rewards(self.config["proxy2"], "")
        self.okcli.query_rewards(self.config["proxy3"], "")
        self.okcli.query_rewards(self.config["proxy4"], "")
        self.okcli.query_rewards(self.config["proxy5"], "")
        self.okcli.query_rewards(self.config["proxy6"], "")

        self.okcli.query_rewards(self.config["delegator1"], "")
        self.okcli.query_rewards(self.config["delegator2"], "")
        self.okcli.query_rewards(self.config["delegator3"], "")
        self.okcli.query_rewards(self.config["delegator4"], "")
        self.okcli.query_rewards(self.config["delegator5"], "")
        self.okcli.query_rewards(self.config["delegator6"], "")

        # 取出所有分红
        self.okcli.withdraw_all_rewards(self.config["delegator1"])
        self.okcli.withdraw_all_rewards(self.config["delegator2"])
        self.okcli.withdraw_all_rewards(self.config["delegator3"])
        self.okcli.withdraw_all_rewards(self.config["delegator4"])
        self.okcli.withdraw_all_rewards(self.config["delegator5"])
        self.okcli.withdraw_all_rewards(self.config["delegator6"])

        self.okcli.withdraw_rewards(self.config["va1"], self.config["proxy1"])
        self.okcli.withdraw_rewards(self.config["va1"], self.config["proxy2"])
        self.okcli.withdraw_rewards(self.config["va1"], self.config["proxy3"])
        self.okcli.withdraw_rewards(self.config["va1"], self.config["proxy4"])
        self.okcli.withdraw_rewards(self.config["va1"], self.config["proxy5"])
        self.okcli.withdraw_rewards(self.config["va1"], self.config["proxy6"])

        # 验证节点提取奖励
        self.okcli.withdraw_commission(self.config["va1"], "va1")
        self.okcli.withdraw_commission(self.config["va2"], "va2")
        self.okcli.withdraw_commission(self.config["va3"], "va3")
        self.okcli.withdraw_commission(self.config["va4"], "va4")

        self.okcli.query_distr_params()

        logging.info("------------------------change_to_on_chain end--------------------------------")

def exit():
    logging.info("Please use arg eg:  test | all")
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
        case.all()
    elif opt == "stop":
        case.okcli.kill_process("exchaind")
    elif opt == "ledger":
        logging.info(case.okcli.get_ledger_seq())
    else:
        exit()
