# /usr/bin/env python3
# --coding:utf-8 --
from cmath import log
import json
import logging
from os import system
from pickletools import long1
import sys
import time
import pybase
import rpc
import sys
import os

class CaseMintProposal:
    def __init__(self, configObj):
        self.config = configObj
        self.okcli = rpc.OKCli("exchaind", "exchaincli", self.config["chainId"], self.config["rpc"])
        return

    def format_decimal(self, num):
        str_num = str(num)
        if "." in str_num:
            a, b = str(str_num).split('.')
            return int(a)
        else:
            return int(str_num)

    def auto(self):
        # 阶段一，初始化账户信息
        self.init_chain_before()
        self.init_chain()

        # 阶段二 初始状态
        # 查询默认的出块奖励，时间参数是否符合预期
        # 发送新提案失败
        self.check_init_before()
        self.check_init()

        # 阶段三，升级2个节点程序
        # 查询默认的出块奖励，时间参数是否符合预期
        # 向节点发送提案失败，向老节点发送提案失败
        self.upgrade_2nodes_before()
        self.upgrade_2nodes()

        # 阶段四，升级所有程序，达到高度隔离前
        # 查询默认的出块奖励，时间参数是否符合预期
        # 向新节点发送提案失败
        self.upgrade_all_nodes_before()
        self.upgrade_all_nodes()

        # 阶段五，达到高度隔离，发送提案 BlocksPerYear 变更为 120 变量
        # 查询默认的出块奖励，时间参数是否符合预期
        self.update_BlocksPerYear_before()
        self.update_BlocksPerYear()

        # 阶段六，达到高度隔离，发送提案 DeflationEpoch 变更为 9
        # 查询默认的出块奖励，时间参数是否符合预期
        self.update_DeflationEpoch_before()
        self.update_DeflationEpoch()

        # 阶段七，发送提案 NextBlockUpdate 失败提案， block 为 0，当前区块高度+1，普通用户提案，提案失败
        # 查询默认的出块奖励，时间参数是否符合预期
        self.update_NextBlockUpdate_error_before()
        self.update_NextBlockUpdate_error()

        # 阶段八，发送提案 NextBlockUpdate 100 个区块后减半，0.5->0.25
        # 查询默认的出块奖励，时间参数是否符合预期
        self.update_NextBlockUpdate_025_before()
        self.update_NextBlockUpdate_025()

        # 阶段九，发送提案 NextBlockUpdate 100 个区块后减半，0.25->0.125
        # 查询默认的出块奖励，时间参数是否符合预期
        self.update_NextBlockUpdate_0125_before()
        self.update_NextBlockUpdate_0125()

        # 阶段十，本地观察是否循环减半
        self.loop()

    def test(self):
        result = self.okcli.query_block_supply()
        logging.info("result: " + str(result))

        logging.info("result: " + str(self.okcli.get_ledger_seq()))

        # result = self.okcli.query_mint_param_value("deflation_epoch")
        # assert result == "3", result
        # logging.info("result: " + str(result))
        # result = self.okcli.query_mint_param_value("blocks_per_year")
        # assert result == "10519200", result
        # logging.info("result: " + str(result))

        return

    def init_chain_before(self):
        logging.info("------------------------initChainBefore start--------------------------------")

        # 老版本编译
        result = self.okcli.run_cmd("cd " + self.config["oldGitPath"] + "/dev/testnet/;./run4v1r.sh")
        time.sleep(5)
        result = self.okcli.wait_ledger(1)
        result = self.okcli.kill_all_process()
        self.okcli.copy_node("exchaind-dev", self.config["goBin"])
        result = self.okcli.version("exchaind-dev") 
        assert result == self.config["oldVersion"], result

        self.okcli.copy_node_cli("exchaincli-dev", self.config["goBin"])
        result = self.okcli.version("exchaincli-dev") 
        assert result == self.config["oldVersion"], result

        # 迁移命令行和迁移文件夹，重新启动
        if len(self.config["nodes"]) <= 0:
            assert False
        
        if self.config["nodes"] == "/":
            assert False

        result = self.okcli.run_cmd("rm -rf " + self.config["nodes"] + "; mkdir " + self.config["nodes"] + ";  cp -rf " + self.config["oldGitPath"] + "/dev/testnet/cache/* " + self.config["nodes"])

        # 新版本编译
        result = self.okcli.run_cmd("cd " + self.config["newGitPath"] + "/dev/testnet/;./run4v1r.sh")
        time.sleep(5)
        result = self.okcli.wait_ledger(1)
        result = self.okcli.kill_all_process()

        self.okcli.copy_node("exchaind-my", self.config["goBin"])
        result = self.okcli.version("exchaind-my") 
        assert result == self.config["newVersion"], result

        self.okcli.copy_node_cli("exchaincli-my", self.config["goBin"])
        result = self.okcli.version("exchaincli-my") 
        assert result == self.config["newVersion"], result
        

        result = self.okcli.run_all_node(self.config["nodeCount"], self.config["ledgerTime"], 0, self.config["nodes"])
        
        logging.info("------------------------initChainBefore end--------------------------------")

    def init_chain(self):
        logging.info("------------------------initChain start--------------------------------")

        # 导入委托人账户和代理人账户
        for d in self.config["delegators"]:
            self.okcli.recover(d[0], d[2])

        for v in self.config["vals"]:
            if self.config["val_recover_996"]:
                self.okcli.recover_val(v[0], v[2])
            else:
                self.okcli.recover(v[0], v[2])

        self.okcli.recover("captain",  self.config["captain-mnemonic"])

        for v in self.config["delegators"]:
            assert self.okcli.transfer(self.config["captain"], v[1], self.config["initCoin"]) != -1

        def do(account):
            result = self.okcli.query_account(account)
            assert self.format_decimal(result) > 0, result

        for v in self.config["delegators"]:
            do(v[1])
    
        logging.info("------------------------initChain end--------------------------------")
        return
    def check_init_before(self):
        logging.info("------------------------check_init_before start--------------------------------")
        logging.info("------------------------check_init_before end--------------------------------")
        return
    
    def check_init(self):
        logging.info("------------------------check_init start--------------------------------")
        # 查询默认的出块奖励，时间参数是否符合预期
        result = self.okcli.query_block_supply()
        logging.info("result: " + str(result))
        assert str(result) == "0.5", str(result)

        result = self.okcli.query_mint_param_value("deflation_epoch")
        assert result == "3", result
        result = self.okcli.query_mint_param_value("blocks_per_year")
        assert result == "10519200", result
        

        # 发送新提案失败
        assert self.okcli.submit_ext_block_update(self.config["vals"][0][1], "proposal-NextBlockUpdate_025.json", False) == -1
        assert self.okcli.submit_ext_block_update(self.config["delegators"][0][1], "proposal-NextBlockUpdate_025.json", False) == -1

        logging.info("------------------------check_init end--------------------------------")
        return
    
    def upgrade_2nodes_before(self):
        # 关闭两个节点并升级，2个新节点、2个旧节点
        logging.info("------------------------upgrade_2nodes_before start--------------------------------")
        self.okcli.kill_all_process()
        self.okcli.run_all_node(self.config["nodeCount"], self.config["ledgerTime"], 2, self.config["nodes"])
        self.okcli.wait_ledger_than(10)
        logging.info("------------------------upgrade_2nodes_before end--------------------------------")
        return
    
    def upgrade_2nodes(self):
        logging.info("------------------------upgrade_2nodes start--------------------------------")
        # 查询默认的出块奖励，时间参数是否符合预期
        result = self.okcli.query_block_supply()
        logging.info("result: " + str(result))
        assert str(result) == "0.5", str(result)

        # 向新节点发送提案失败
        assert self.okcli.submit_ext_block_update(self.config["vals"][0][1], "proposal-NextBlockUpdate_025.json", False) == -1
        assert self.okcli.submit_ext_block_update(self.config["delegators"][0][1], "proposal-NextBlockUpdate_025.json", False) == -1
        

        logging.info("------------------------upgrade_2nodes end--------------------------------")
        return
    
    def upgrade_all_nodes_before(self):
        # 升级所有程序，达到高度隔离前
        logging.info("------------------------upgrade_all_nodes_before start--------------------------------")
        logging.info("------------------------upgrate_bin_staking_step2_before start--------------------------------")
        self.okcli.kill_all_process()
        self.okcli.run_all_node(self.config["nodeCount"], self.config["ledgerTime"], self.config["nodeCount"], self.config["nodes"])
        time.sleep(10)
        logging.info("------------------------upgrade_all_nodes_before end--------------------------------")
        return
    
    def upgrade_all_nodes(self):
        logging.info("------------------------upgrade_all_nodes start--------------------------------")
        assert self.okcli.get_ledger_seq() <= self.config["upgradeLedger"], str(self.okcli.get_ledger_seq())

        # 查询默认的出块奖励，时间参数是否符合预期
        result = self.okcli.query_block_supply()
        logging.info("result: " + str(result))
        assert str(result) == "0.5", str(result)

        result = self.okcli.query_mint_param_value("deflation_epoch")
        assert result == "3", result
        result = self.okcli.query_mint_param_value("blocks_per_year")
        assert result == "10519200", result

        # 向新节点发送提案失败，没有达到区块高度，无法进交易池
        assert self.okcli.submit_ext_block_update(self.config["vals"][0][1], "proposal-NextBlockUpdate_025.json", False) == -1
        assert self.okcli.submit_ext_block_update(self.config["delegators"][0][1], "proposal-NextBlockUpdate_025.json", False) == -1


        logging.info("------------------------upgrade_all_nodes end--------------------------------")
        return
    

    def update_BlocksPerYear_before(self):
        logging.info("------------------------update_BlocksPerYear_block start--------------------------------")
    

        logging.info("------------------------update_BlocksPerYear_block end--------------------------------")
        return
    
    def update_BlocksPerYear(self):
        logging.info("------------------------update_BlocksPerYear start--------------------------------")
        self.okcli.wait_ledger(self.config["upgradeLedger"])

        # 达到高度隔离，发送提案 BlocksPerYear 变更为 120 变量
        proposal_num = self.okcli.submit_change_param_change(self.config["vals"][0][1], "param-chanage-BlocksPerYear.json", False)
        logging.info("result:" + proposal_num)

        self.okcli.query_proposal(proposal_num)
        
        for v in self.config["vals"]:
            self.okcli.vote(v[1], proposal_num)

        self.okcli.query_proposal(proposal_num)
        self.okcli.wait_ledger(self.config["upgradeLedger"] + 60)

        # 查询默认的出块奖励，时间参数是否符合预期
        result = self.okcli.query_block_supply()
        logging.info("result: " + str(result))
        assert str(result) == "0.5", str(result)

        result = self.okcli.query_mint_param_value("deflation_epoch")
        assert result == "3", result
        result = self.okcli.query_mint_param_value("blocks_per_year")
        assert result == "264", result

        logging.info("------------------------update_BlocksPerYear end--------------------------------")
        return
    
    def update_DeflationEpoch_before(self):
        logging.info("------------------------update_DeflationEpoch start--------------------------------")
        logging.info("------------------------update_DeflationEpoch end--------------------------------")
        return
    
    def update_DeflationEpoch(self):
        logging.info("------------------------update_DeflationEpoch start--------------------------------")
        # 阶段六，达到高度隔离，发送提案 DeflationEpoch 变更为 9
        proposal_num = self.okcli.submit_change_param_change(self.config["vals"][0][1], "param-chanage-DeflationEpoch.json", False)
        logging.info("result:" + proposal_num)

        self.okcli.query_proposal(proposal_num)
        
        for v in self.config["vals"]:
            self.okcli.vote(v[1], proposal_num)

        self.okcli.query_proposal(proposal_num)
        self.okcli.wait_ledger(self.config["upgradeLedger"] + 110)
        # 查询默认的出块奖励，时间参数是否符合预期
        result = self.okcli.query_block_supply()
        logging.info("result: " + str(result))
        assert str(result) == "0.5", str(result)

        result = self.okcli.query_mint_param_value("deflation_epoch")
        assert result == "9", result
        result = self.okcli.query_mint_param_value("blocks_per_year")
        assert result == "264", result

        logging.info("------------------------update_DeflationEpoch end--------------------------------")
        return
    
    def update_NextBlockUpdate_error_before(self):
        logging.info("------------------------update_NextBlockUpdate_error_before start--------------------------------")
        logging.info("------------------------update_NextBlockUpdate_error_before end--------------------------------")
        return
    
    def update_NextBlockUpdate_error(self):
        logging.info("------------------------update_NextBlockUpdate_error start--------------------------------")
        # 发送提案 NextBlockUpdate 失败提案， block 为 0，当前区块高度+1，普通用户提案，提案失败
        proposal_num = self.okcli.submit_ext_block_update(self.config["vals"][0][1], "proposal-NextBlockUpdate_0.json", False)
        logging.info("result:" + proposal_num)

        self.okcli.query_proposal(proposal_num)
        
        for v in self.config["vals"]:
            self.okcli.vote(v[1], proposal_num)

        self.okcli.query_proposal(proposal_num)
        self.okcli.wait_ledger_than(2)

        # 发送提案 NextBlockUpdate 失败提案，普通用户提案，提案失败
        assert self.okcli.submit_ext_block_update(self.config["delegators"][0][1], "proposal-NextBlockUpdate_025.json", False) == 100005

        # 查询默认的出块奖励，时间参数是否符合预期
        result = self.okcli.query_block_supply()
        logging.info("result: " + str(result))
        assert str(result) == "0.5", str(result)

        logging.info("------------------------update_NextBlockUpdate_error end--------------------------------")
        return
    
    def update_NextBlockUpdate_025_before(self):
        logging.info("------------------------update_NextBlockUpdate_025_before start--------------------------------")
        logging.info("------------------------update_NextBlockUpdate_025_before end--------------------------------")
        return
    
    def update_NextBlockUpdate_025(self):
        logging.info("------------------------update_NextBlockUpdate_025 start--------------------------------")
        # 阶段八，发送提案 NextBlockUpdate 100 个区块后减半，0.5->0.25
        proposal_num = self.okcli.submit_ext_block_update(self.config["vals"][0][1], "proposal-NextBlockUpdate_025.json", False)
        logging.info("result:" + proposal_num)

        self.okcli.query_proposal(proposal_num)
        
        for v in self.config["vals"]:
            self.okcli.vote(v[1], proposal_num)

        self.okcli.query_proposal(proposal_num)
        self.okcli.wait_ledger_than(2)

        # 查询默认的出块奖励，时间参数是否符合预期
        self.okcli.wait_ledger(self.config["upgradeLedger"] + 210)
        result = self.okcli.query_block_supply()
        logging.info("result: " + str(result))
        assert str(result) == "0.25", str(result)

        logging.info("------------------------update_NextBlockUpdate_025 end--------------------------------")
        return
    
    def update_NextBlockUpdate_0125_before(self):
        logging.info("------------------------update_NextBlockUpdate_0125_before start--------------------------------")
        logging.info("------------------------update_NextBlockUpdate_0125_before end--------------------------------")
        return
    
    def update_NextBlockUpdate_0125(self):
        logging.info("------------------------update_NextBlockUpdate_0125 start--------------------------------")
        # 发送提案 NextBlockUpdate 100 个区块后减半，0.25->0.125
        proposal_num = self.okcli.submit_ext_block_update(self.config["vals"][0][1], "proposal-NextBlockUpdate_0125.json", False)
        logging.info("result:" + proposal_num)

        self.okcli.query_proposal(proposal_num)
        
        for v in self.config["vals"]:
            self.okcli.vote(v[1], proposal_num)

        self.okcli.query_proposal(proposal_num)
        self.okcli.wait_ledger(self.config["upgradeLedger"] + 410)

        # 查询默认的出块奖励，时间参数是否符合预期
        result = self.okcli.query_block_supply()
        logging.info("result: " + str(result))
        assert str(result) == "0.125", str(result)

        result = self.okcli.query_mint_param_value("deflation_epoch")
        assert result == "9", result
        result = self.okcli.query_mint_param_value("blocks_per_year")
        assert result == "264", result

        logging.info("------------------------update_NextBlockUpdate_0125 end--------------------------------")
        return

    def loop(self):
        self.okcli.wait_ledger(self.config["upgradeLedger"] + 610)
        result = self.okcli.query_block_supply()
        logging.info("result: " + str(result))
        assert str(result) == "0.0625", str(result)

        return
    
    def exit(self, stop = True):
        #if stop:
            #case.okcli.kill_all_process()
        logging.info("Please use arg eg:  auto")
        sys.exit()

if __name__ == '__main__':
    pybase = pybase.Pybase()
    strlist = os.path.basename(__file__).split('.') 
    file = open('config/' + strlist[0] + '.json', 'r', encoding='UTF-8')
    moduleConfig = json.loads(file.read())
    file.close()
    case = CaseMintProposal(moduleConfig)

    if len(sys.argv) < 2:
        case.exit()
    opt = sys.argv[1]

    if opt == "test":
        case.test()

    elif opt == "auto":
        case.auto()

    elif opt == "init_chain_before":
        case.init_chain_before()
    elif opt == "init_chain":
        case.init_chain()
    
    elif opt == "start":
        case.okcli.run_all_node(case.config["nodeCount"], case.config["ledgerTime"], case.config["nodeCount"], case.config["nodes"])
    elif opt == "stop":
        case.okcli.kill_all_process()
    elif opt == "ps":
        case.okcli.ps("exchaind")
        case.okcli.ps("exchaind-dev")
        case.okcli.ps("exchaind-my")
    elif opt == "ledger":
        logging.info(str(case.okcli.get_ledger_seq()))
    else:
        case.exit()
