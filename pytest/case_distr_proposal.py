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

class CaseDistrProposal:
    def __init__(self, configObj):
        self.config = configObj
        self.okcli = rpc.OKCli("exchaind", "exchaincli", self.config["chainId"], self.config["rpc"])
        self.vals1 = self.config["vals"][0][3]
        self.vals2 = self.config["vals"][0][3] + "," + self.config["vals"][1][3]
        self.vals3 = self.config["vals"][0][3] + "," + self.config["vals"][1][3] + "," + self.config["vals"][2][3]
        self.vals4 = self.config["vals"][0][3] + "," + self.config["vals"][1][3] + "," + self.config["vals"][2][3] + "," + self.config["vals"][3][3] 
        self.valsall = self.config["vals"][0][3] + "," + self.config["vals"][1][3] + "," + self.config["vals"][2][3] + "," + self.config["vals"][3][3] + "," + self.config["vaadmin16"]
        self.valsDeafultAll = ""
        for v in self.config["vals"]:
            self.valsDeafultAll += v[3] + ","
        self.valsDeafultAll = self.valsDeafultAll.strip(',')

        self.vals3 = self.config["vals"][0][3] + "," + self.config["vals"][1][3] + "," + self.config["vals"][2][3]
        self.single_debug = self.config["singleDebug"]

        return

    def format_decimal(self, num):
        str_num = str(num)
        if "." in str_num:
            a, b = str(str_num).split('.')
            return int(a)
        else:
            return int(str_num)

    def format_decimal_precision(self, num, precision):
        precision = precision + 1
        str_num = str(num)
        if "." in str_num:
            return float(str_num[0:(str_num.index('.')+precision)])
        else:
            return float(str_num)

    def assert_compare_near(self, num1, num2):
        a = self.format_decimal(num1)
        b = self.format_decimal(num2)
        result = str(num1) + ", " + str(num2)
        assert abs(a - b) <= 1, result

    def assert_compare_gt(self, num1, num2):
        a = self.format_decimal(num1)
        b = self.format_decimal(num2)
        result = str(num1) + ", " + str(num2)
        assert a > b, result

    def assert_compare_same(self, num1, num2):
        a = self.format_decimal(num1)
        b = self.format_decimal(num2)
        result = str(num1) + ", " + str(num2)
        assert abs(a - b) <= 0, result

    def auto(self):
        # 阶段一，初始化账户信息
        self.init_chain_before()
        self.init_chain()

        # 阶段二，构建初始化投票交易，注意要投票给V节点
        self.init_staking_before()
        self.init_staking()

        # 阶段三-1，升级2个节点程序，继续初始化投票交易
        self.upgrate_bin_staking_step1_before()
        self.upgrate_bin_staking_step1()

        # 阶段三-2，升级所有程序，继续初始化投票交易
        self.upgrate_bin_staking_step2_before()
        self.upgrate_bin_staking_step2()

        # 阶段四，达到高度隔离，验证新增接口在提前前无效，继续初始化投票交易
        self.upgrate_ledger_staking_before()
        self.upgrate_ledger_staking()
        
        # 阶段五， 投票链上分红提案，验证分红和抽成正常，继续初始化投票
        self.after_distr_proposal_before()
        self.after_distr_proposal()

        # 阶段六，投票为链下分红提案，验证分红为0抽成正常，继续初始化投票
        self.change_to_off_chain_before()
        self.change_to_off_chain()

        # 阶段七，投票为链上分红提案，验证委托人、代理人、被代理人操作投票分红，验证节点销毁不再分红
        self.change_to_on_chain_before()
        self.change_to_on_chain()

        # 阶段八，禁用启用提取分红
        self.enabled_withdraw_reward_before()
        self.enabled_withdraw_reward()

        # 阶段九，分红精度截断提案
        self.reward_truncate_before()
        self.reward_truncate()

        # 阶段十，补充测试用例
        # self.extension_before()
        # self.extension()

    def all_add_shares(self):
        for d in self.config["delegators"]:
            result = self.okcli.query_shares(d[1])
            if "tokens" in result:
                self.okcli.withdraw(self.format_decimal(result["tokens"]), d[0], False)

            assert self.okcli.deposit(self.config["depoistCoin"], d[1]) != -1
            assert self.okcli.add_shares(self.valsall, d[1]) != -1
        

        for d in self.config["proxydelegators"]:
            result = self.okcli.query_shares(d[1])
            if "tokens" in result:
                self.okcli.withdraw(self.format_decimal(result["tokens"]), d[0], False)

            assert self.okcli.deposit(self.config["depoistCoin"], d[1]) != -1
            assert self.okcli.add_shares(self.valsall, d[1]) != -1
        
        for d in self.config["proxys"]:
            result = self.okcli.query_shares(d[1])
            if "tokens" in result:
                self.okcli.withdraw(self.format_decimal(result["tokens"]), d[0], False)

            assert self.okcli.deposit(self.config["depoistCoin"], d[1]) != -1
            assert self.okcli.add_shares(self.valsall, d[1]) != -1

    
    def test(self):
        # proposal_num = self.okcli.submit_reward_truncate_2(self.config["vals"][0][1])
        # proposal_num = self.okcli.submit_change_type_proposal_onchain(self.config["vals"][1][1])
        # self.okcli.query_proposal(proposal_num)
        
        # for n in self.config["delegators"]:
        #     self.okcli.vote(n[1], proposal_num)

        # for n in self.config["proxys"]:
        #     self.okcli.vote(n[1], proposal_num)

        # for v in self.config["vals"]:
        #     self.okcli.vote(v[1], proposal_num)
        # self.okcli.query_proposal(proposal_num)

        # self.okcli.wait_ledger_than(2)
        # result = self.okcli.query_distr_params()
        # assert result["reward_truncate_precision"] == "0", result
        # return
        

        # assert self.okcli.add_shares(self.vals2, self.config["proxys"][2][1]) != -1
        # self.okcli.query_total_rewards_gt(self.config["proxys"][2][1], self.config["vals"][0][3], 1)
        # assert len(self.okcli.query_rewards(self.config["proxys"][2][1], self.config["vals"][1][3])) == 0

        # ## 取出所有质押
        # for d in self.config["delegators"]:
        #     result = self.okcli.query_shares(d[1])
        #     if "tokens" in result:
        #         self.okcli.withdraw(self.format_decimal(result["tokens"]), d[0], False)
        # for p in self.config["proxydelegators"]:
        #     result = self.okcli.query_shares(p[1])
        #     if "tokens" in result:
        #         self.okcli.withdraw(self.format_decimal(result["tokens"]), p[0], False)
        # for p in self.config["proxys"]:
        #     self.okcli.unreg(p[1], False)
        # for p in self.config["proxys"]:
        #     result = self.okcli.query_shares(p[1])
        #     if "tokens" in result:
        #         self.okcli.withdraw(self.format_decimal(result["tokens"]), p[0], False)
        # for v in self.config["vals"]:
        #     result = self.okcli.query_shares(v[1])
        #     if "tokens" in result:
        #         self.okcli.withdraw(self.format_decimal(result["tokens"]), v[0], False)

        # # 查询节点区块高度是否一致
        # splitArray = self.config["rpc"].split(":")
        # url = splitArray[0] + ":" + splitArray[1]
        # ledger = int(self.okcli.get_ledger_seq())
        # for i in range(self.config["nodeCount"]):
        #     port = 26657 + i * 100
        #     rpc = url + ":" + str(port)
        #     other_ledger = int(self.okcli.get_ledger_seq(rpc))
        #     assert (other_ledger - ledger) <= 5
        #     logging.info("ledger:" + str(ledger) + ", other ledger:" + str(other_ledger))
        
        # assert self.okcli.edit_validator_rate('"1.0001"', "va2", False) == -1
        # assert self.okcli.edit_validator_rate("0", "va1", False) != -1
        # assert self.okcli.edit_validator_rate("1", "va2", False) != -1
        # assert self.okcli.edit_validator_rate("1", "va3", False) != -1
        # assert self.okcli.edit_validator_rate("1", "va4", False) != -1

        # assert self.okcli.withdraw_commission(self.config["vals"][0][3], "va1") != -1
        # assert self.okcli.withdraw_commission(self.config["vals"][1][3], "va2") != -1
        # assert self.okcli.withdraw_commission(self.config["vals"][2][3], "va3") != -1
        # assert self.okcli.withdraw_commission(self.config["vals"][3][3], "va4") != -1


        # 注册代理成功
        # assert self.okcli.deposit(self.config["depoistCoin"], self.config["delegators"][5][1]) != -1 
        # assert self.okcli.add_shares(self.vals4, self.config["delegators"][5][1]) != -1  
        # assert self.okcli.deposit(self.config["depoistCoin"], self.config["proxydelegators"][5][1]) != -1
        # assert self.okcli.deposit(self.config["depoistCoin"], self.config["proxys"][5][1]) != -1
        # assert self.okcli.add_shares(self.vals4, self.config["proxys"][5][1]) != -1
        # self.okcli.query_total_rewards_gt_precision(self.config["proxys"][5][1], self.config["vals"][1][3], 0, self.PRECISION)
        assert self.okcli.unreg(self.config["proxys"][5][1]) != -1
        # self.okcli.query_total_rewards_gt_precision(self.config["proxys"][5][1], self.config["vals"][0][3], 0, self.PRECISION)
        assert self.okcli.proxy_reg(self.config["proxys"][5][1]) != -1
        # return

        # bind也会进行分红
        self.okcli.set_withdraw_addr(self.config["withdrawaddress"], self.config["proxys"][5][1])
        before = self.okcli.query_account(self.config["withdrawaddress"])
        self.okcli.query_total_rewards_gt_precision(self.config["proxys"][5][1], self.config["vals"][0][3], 0, self.PRECISION)
        assert self.okcli.proxy_bind(self.config["proxys"][5][1], self.config["proxydelegators"][5][1]) != -1
        after = self.okcli.query_account(self.config["withdrawaddress"])
        addValue = self.format_decimal_precision(after, self.PRECISION) - self.format_decimal_precision(before, self.PRECISION)
        logging.info("str addValue:" + str(addValue))
        assert addValue >= self.PRECISION_REWARDS_DIFF, str(addValue)

        # proxy5 取出va2的分红
        self.okcli.query_total_rewards_gt_precision(self.config["proxys"][5][1], self.config["vals"][1][3], 0, self.PRECISION)
        rewards = self.okcli.query_rewards(self.config["proxys"][5][1], self.config["vals"][1][3])[0]["amount"]
        beforeAmount = self.okcli.query_account(self.config["withdrawaddress"])
        assert self.okcli.withdraw_rewards(self.config["vals"][1][3], self.config["proxys"][5][1]) != -1
        afterAmount = self.okcli.query_account(self.config["withdrawaddress"])
        logging.info("afterAmount:" + str(afterAmount) + ", beforeAmount:" + str(beforeAmount) + ", rewards:" + str(rewards))
        assert float(rewards) > self.PRECISION_REWARDS, rewards
        diff = self.format_decimal_precision(afterAmount, self.PRECISION) - (self.format_decimal_precision(beforeAmount, self.PRECISION)) 
        assert float(diff) >= self.PRECISION_REWARDS_DIFF, str(diff)

        # proxy5 unbind 分红
        self.okcli.query_total_rewards_gt_precision(self.config["proxys"][5][1], self.config["vals"][1][3], 0, self.PRECISION)
        rewards = self.okcli.query_rewards(self.config["proxys"][5][1], self.config["vals"][1][3])[0]["amount"]
        beforeAmount = self.okcli.query_account(self.config["withdrawaddress"])
        assert self.okcli.proxy_unbind(self.config["proxydelegators"][5][1]) != -1
        afterAmount = self.okcli.query_account(self.config["withdrawaddress"])
        logging.info("afterAmount:" + str(afterAmount) + ", beforeAmount:" + str(beforeAmount) + ", rewards:" + str(rewards))
        assert float(rewards) > self.PRECISION_REWARDS, rewards
        diff = self.format_decimal_precision(afterAmount, self.PRECISION) - (self.format_decimal_precision(beforeAmount, self.PRECISION)) 
        logging.info("str diff:" + str(diff))
        assert diff >= self.PRECISION_REWARDS_DIFF, str(diff)

        # assert self.okcli.submit_withdraw_reward_disabled(self.config["delegators"][0][1], False) == -1

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

        for p in self.config["proxys"]:
            self.okcli.recover(p[0], p[2])

        for p in self.config["proxydelegators"]:
            self.okcli.recover(p[0], p[2])

        for v in self.config["vals"]:
            if self.config["val_recover_996"]:
                self.okcli.recover_val(v[0], v[2])
            else:
                self.okcli.recover(v[0], v[2])

        self.okcli.recover("captain",  self.config["captain-mnemonic"])
        self.okcli.recover("delegator-ex0",  self.config["exaccounts"]["delegator-ex0"][1])
        self.okcli.recover("delegator-ex1",  self.config["exaccounts"]["delegator-ex1"][1])
        self.okcli.recover("delegator-ex2",  self.config["exaccounts"]["delegator-ex2"][1])
        self.okcli.recover("proxydelegator-ex0",  self.config["exaccounts"]["proxydelegator-ex0"][1])
        self.okcli.recover("proxydelegator-ex1",  self.config["exaccounts"]["proxydelegator-ex1"][1])
        self.okcli.recover("proxydelegator-ex2",  self.config["exaccounts"]["proxydelegator-ex2"][1])
        self.okcli.recover("proxy-ex0",  self.config["exaccounts"]["proxy-ex0"][1])
        self.okcli.recover("proxy-ex1",  self.config["exaccounts"]["proxy-ex1"][1])
        self.okcli.recover("proxy-ex2",  self.config["exaccounts"]["proxy-ex2"][1])

        for v in self.config["delegators"]:
            assert self.okcli.transfer(self.config["captain"], v[1], self.config["initCoin"]) != -1
        for v in self.config["proxys"]:
            assert self.okcli.transfer(self.config["captain"], v[1], self.config["initCoin"]) != -1
        for v in self.config["proxydelegators"]:
            assert self.okcli.transfer(self.config["captain"], v[1], self.config["initCoin"]) != -1
        assert self.okcli.transfer(self.config["captain"], self.config["vaAddadmin16"], self.config["initCoin"]) != -1
        
        assert self.okcli.transfer(self.config["captain"], self.config["exaccounts"]["delegator-ex0"][0], self.config["initCoin"]) != -1
        assert self.okcli.transfer(self.config["captain"], self.config["exaccounts"]["delegator-ex1"][0], self.config["initCoin"]) != -1
        assert self.okcli.transfer(self.config["captain"], self.config["exaccounts"]["delegator-ex2"][0], self.config["initCoin"]) != -1
        assert self.okcli.transfer(self.config["captain"], self.config["exaccounts"]["proxydelegator-ex0"][0], self.config["initCoin"]) != -1
        assert self.okcli.transfer(self.config["captain"], self.config["exaccounts"]["proxydelegator-ex1"][0], self.config["initCoin"]) != -1
        assert self.okcli.transfer(self.config["captain"], self.config["exaccounts"]["proxydelegator-ex2"][0], self.config["initCoin"]) != -1
        assert self.okcli.transfer(self.config["captain"], self.config["exaccounts"]["proxy-ex0"][0], self.config["initCoin"]) != -1
        assert self.okcli.transfer(self.config["captain"], self.config["exaccounts"]["proxy-ex1"][0], self.config["initCoin"]) != -1
        assert self.okcli.transfer(self.config["captain"], self.config["exaccounts"]["proxy-ex2"][0], self.config["initCoin"]) != -1

        def do(account):
            result = self.okcli.query_account(account)
            assert self.format_decimal(result) > 0, result

        for v in self.config["delegators"]:
            do(v[1])
    
        for v in self.config["proxys"]:
            do(v[1])

        for v in self.config["proxydelegators"]:
            do(v[1])
        
        do(self.config["vaAddadmin16"])

        logging.info("------------------------initChain end--------------------------------")
        return
    
    def init_staking_before(self):
        logging.info("------------------------initStakingBefore start--------------------------------")
        if self.single_debug:
            self.okcli.kill_all_process()
            self.okcli.run_all_node(self.config["nodeCount"], self.config["ledgerTime"], 0, self.config["nodes"])
            time.sleep(5)
        logging.info("------------------------initStakingBefore end--------------------------------")

    def init_staking(self):
        logging.info("------------------------initStaking start--------------------------------")
        
        # 质押delegator1 10000 okt
        assert self.okcli.deposit(self.config["depoistCoin"], self.config["delegators"][0][1]) != -1
        assert self.okcli.add_shares(self.vals1, self.config["delegators"][0][1]) != -1
        result = self.okcli.query_shares(self.config["delegators"][0][1])
        assert self.format_decimal(result["tokens"]) == self.config["depoistCoin"], result
        assert self.format_decimal(result["shares"]) > 0, result

        # 质押 proxydelegator1 10000 okt
        assert self.okcli.deposit(self.config["depoistCoin"], self.config["proxydelegators"][0][1]) != -1
        result = self.okcli.query_shares(self.config["proxydelegators"][0][1])
        assert self.format_decimal(result["tokens"]) == self.config["depoistCoin"], result
        assert self.format_decimal(result["shares"]) == 0, result

        # 质押proxy1 10000 okt，注册代理 proxy1, proxydelegator1 绑定 proxy1
        assert self.okcli.deposit(self.config["depoistCoin"], self.config["proxys"][0][1]) != -1
        assert self.okcli.add_shares(self.vals1, self.config["proxys"][0][1]) != -1
        assert self.okcli.proxy_reg(self.config["proxys"][0][1]) != -1
        assert self.okcli.proxy_bind(self.config["proxys"][0][1], self.config["proxydelegators"][0][1]) != -1

        # proxydelegator1 有 tokens，shares 为 0
        resultProxydelegator1 = self.okcli.query_shares(self.config["proxydelegators"][0][1])
        assert self.format_decimal(resultProxydelegator1["tokens"]) == self.config["depoistCoin"], resultProxydelegator1
        assert self.format_decimal(resultProxydelegator1["shares"]) == 0, resultProxydelegator1
        assert resultProxydelegator1["proxy_address"] == self.config["proxys"][0][1], resultProxydelegator1

        # proxy1 的 total_delegated_tokens 等于 proxydelegator1 的 shares
        result = self.okcli.query_shares(self.config["proxys"][0][1])
        assert result["is_proxy"] == True, result
        assert self.format_decimal(result["tokens"]) == self.config["depoistCoin"], result
        assert self.format_decimal(result["total_delegated_tokens"]) == self.format_decimal(resultProxydelegator1["tokens"]), result

        # 验证节点 commission 有值
        self.okcli.query_commission_gt(self.config["vals"][0][3], 0)
        result = self.okcli.query_commission(self.config["vals"][0][3])
        assert self.format_decimal(result) > 0, result

        self.okcli.query_commission_gt(self.config["vals"][1][3], 0)
        result = self.okcli.query_commission(self.config["vals"][1][3])
        assert self.format_decimal(result) > 0, result

        self.okcli.query_commission_gt(self.config["vals"][2][3], 0)
        result = self.okcli.query_commission(self.config["vals"][2][3])
        assert self.format_decimal(result) > 0, result

        self.okcli.query_commission_gt(self.config["vals"][3][3], 0)
        result = self.okcli.query_commission(self.config["vals"][3][3])
        assert self.format_decimal(result) > 0, result

        ## delegators 10投票所有人
        assert self.okcli.deposit(self.config["depoistCoin"], self.config["delegators"][9][1]) != -1
        assert self.okcli.add_shares(self.valsDeafultAll, self.config["delegators"][9][1]) != -1

        logging.info("------------------------initStaking end--------------------------------")

    def upgrate_bin_staking_step1_before(self):
        logging.info("------------------------upgrate_bin_staking_step1_before start--------------------------------")

        self.okcli.kill_all_process()
        self.okcli.run_all_node(self.config["nodeCount"], self.config["ledgerTime"], 2, self.config["nodes"])
        time.sleep(10)

        logging.info("------------------------upgrate_bin_staking_step1_before end--------------------------------")

    def upgrate_bin_staking_step1(self):
        logging.info("------------------------upgrate_bin_staking_step1 start--------------------------------")
        # 只升级两个节点，保证新老交易不会产生smb
        # 发送新的交易，确保交易不会上链以及出现smb
        assert self.okcli.withdraw_rewards(self.config["vals"][0][3], self.config["delegators"][0][1], False) == -1
        assert self.okcli.withdraw_all_rewards(self.config["delegators"][0][1], False) == -1
        assert self.okcli.submit_change_type_proposal_offchain(self.config["delegators"][0][1], False) == -1
        assert self.okcli.submit_change_type_proposal_onchain(self.config["delegators"][0][1], False) == -1
        assert self.okcli.submit_change_type_proposal_offchain(self.config["vals"][0][1], False) == -1
        assert self.okcli.submit_change_type_proposal_onchain(self.config["vals"][0][1], False) == -1
        assert self.okcli.submit_withdraw_reward_enabled(self.config["delegators"][0][1], False) == -1
        assert self.okcli.submit_withdraw_reward_disabled(self.config["vals"][0][1], False) == -1
        assert self.okcli.edit_validator_rate("0.5", "va4", False) == -1
        assert self.okcli.submit_reward_truncate_0(self.config["delegators"][0][1], False) == -1
        assert self.okcli.submit_reward_truncate_0(self.config["vals"][0][1], False) == -1

        # 发送老的交易，不会出现smb
        assert self.okcli.transfer(self.config["captain"], self.config["exaccounts"]["delegator-ex0"][0], self.config["initCoin"]) != -1
        assert self.okcli.deposit(10, self.config["exaccounts"]["delegator-ex0"][0]) != -1
        assert self.okcli.deposit(10, self.config["exaccounts"]["proxydelegator-ex0"][0]) != -1
        assert self.okcli.deposit(10, self.config["exaccounts"]["proxy-ex0"][0]) != -1
        assert self.okcli.add_shares(self.vals2, self.config["exaccounts"]["proxy-ex0"][0]) != -1
        assert self.okcli.proxy_reg(self.config["exaccounts"]["proxy-ex0"][0]) != -1
        assert self.okcli.proxy_bind(self.config["exaccounts"]["proxy-ex0"][0], self.config["exaccounts"]["proxydelegator-ex0"][0]) != -1
        assert self.okcli.proxy_unbind(self.config["exaccounts"]["proxydelegator-ex0"][0]) != -1
        assert self.okcli.unreg(self.config["exaccounts"]["proxy-ex0"][0]) != -1
        assert self.okcli.withdraw(10, self.config["exaccounts"]["proxydelegator-ex0"][0]) != -1
        assert self.okcli.set_withdraw_addr(self.config["withdrawaddress"], self.config["exaccounts"]["delegator-ex0"][0]) != -1
        assert self.okcli.withdraw_commission(self.config["vals"][0][3], "va1") != -1
        assert self.okcli.edit_validator("zzzzzzzz", "va2") != -1
        proposal_num = self.okcli.submit_community_pool_spend(self.config["exaccounts"]["delegator-ex0"][0])
        self.okcli.vote_deposit(self.config["exaccounts"]["delegator-ex0"][0], proposal_num, "100")
        assert int(proposal_num) > 0
        for n in self.config["delegators"]:
            self.okcli.vote(n[1], proposal_num)
        for n in self.config["proxys"]:
            self.okcli.vote(n[1], proposal_num)
        for v in self.config["vals"]:
            self.okcli.vote(v[1], proposal_num)
        self.okcli.query_proposal(proposal_num)
        self.okcli.vote(self.config["exaccounts"]["delegator-ex0"][0], proposal_num)
        self.okcli.vote(self.config["exaccounts"]["proxydelegator-ex0"][0], proposal_num)
        self.okcli.vote(self.config["exaccounts"]["proxy-ex0"][0], proposal_num)

        # 质押delegator2 10000 okt，投票给va1
        assert self.okcli.deposit(self.config["depoistCoin"], self.config["delegators"][1][1]) != -1
        assert self.okcli.add_shares(self.vals2, self.config["delegators"][1][1]) != -1

        # proxydelegator2 质押 10000okt
        assert self.okcli.deposit(self.config["depoistCoin"], self.config["proxydelegators"][1][1]) != -1
        result = self.okcli.query_shares(self.config["proxydelegators"][1][1])
        assert self.format_decimal(result["tokens"]) == self.config["depoistCoin"], result
        assert self.format_decimal(result["shares"]) == 0, result

        logging.info("------------------------upgrate_bin_staking_step1 end--------------------------------")

    def upgrate_bin_staking_step2_before(self):
        logging.info("------------------------upgrate_bin_staking_step2_before start--------------------------------")
        self.okcli.kill_all_process()
        self.okcli.run_all_node(self.config["nodeCount"], self.config["ledgerTime"], self.config["nodeCount"], self.config["nodes"])
        time.sleep(10)

        logging.info("------------------------upgrate_bin_staking_step2_before end--------------------------------")

    def upgrate_bin_staking_step2(self):
        logging.info("------------------------upgrate_bin_staking_step2 start--------------------------------")

        # 注册 proxy2， proxydelegator2 绑定 proxy2
        assert self.okcli.deposit(self.config["depoistCoin"], self.config["proxys"][1][1]) != -1
        assert self.okcli.add_shares(self.vals2, self.config["proxys"][1][1]) != -1
        assert self.okcli.proxy_reg(self.config["proxys"][1][1]) != -1
        assert self.okcli.proxy_bind(self.config["proxys"][1][1], self.config["proxydelegators"][1][1]) != -1

        # proxydelegator2 有 tokens，shares 为 0
        resultProxydelegator2 = self.okcli.query_shares(self.config["proxydelegators"][1][1])
        assert self.format_decimal(resultProxydelegator2["tokens"]) == self.config["depoistCoin"], resultProxydelegator2
        assert self.format_decimal(resultProxydelegator2["shares"]) == 0, resultProxydelegator2
        assert resultProxydelegator2["proxy_address"] == self.config["proxys"][1][1], resultProxydelegator2

        # proxy2 的 total_delegated_tokens 等于 proxydelegator2 的 shares
        result = self.okcli.query_shares(self.config["proxys"][1][1])
        assert result["is_proxy"] == True, result
        assert self.format_decimal(result["tokens"]) == self.config["depoistCoin"], result
        assert self.format_decimal(result["total_delegated_tokens"]) == self.format_decimal(resultProxydelegator2["tokens"]), result

        logging.info("------------------------upgrate_bin_staking_step2 end--------------------------------")
        

    def upgrate_ledger_staking_before(self):
        logging.info("------------------------upgrate_ledger_staking_before start--------------------------------")
        if self.single_debug:
            self.okcli.kill_all_process()
            self.okcli.run_all_node(self.config["nodeCount"], self.config["ledgerTime"], self.config["nodeCount"], self.config["nodes"])
            time.sleep(5)

        logging.info("------------------------upgrate_ledger_staking_before end--------------------------------")

    def upgrate_ledger_staking(self):
        logging.info("------------------------upgrate_ledger_staking start--------------------------------")
        # 不支持的操作  withdraw-all-rewards、withdraw-rewards、outstanding-rewards、query_rewards
        assert self.okcli.withdraw_all_rewards(self.config["delegators"][0][1]) == -1
        assert self.okcli.withdraw_rewards(self.config["vals"][0][3], self.config["delegators"][0][1]) == -1
        assert self.okcli.query_outstanding(self.config["vals"][0][3]) == -1
        assert self.okcli.query_rewards(self.config["delegators"][0][1], "") == -1

        # 发送新的交易，确保交易不会上链以及出现smb
        assert self.okcli.withdraw_rewards(self.config["vals"][0][3], self.config["delegators"][0][1], False) == -1
        assert self.okcli.withdraw_all_rewards(self.config["delegators"][0][1], False) == -1
        assert self.okcli.submit_change_type_proposal_offchain(self.config["delegators"][0][1], False) == -1
        assert self.okcli.submit_change_type_proposal_offchain(self.config["vals"][0][1], False) == -1
        assert self.okcli.submit_change_type_proposal_onchain(self.config["delegators"][0][1], False) == -1
        assert self.okcli.submit_change_type_proposal_onchain(self.config["vals"][0][1], False) == -1
        assert self.okcli.submit_withdraw_reward_enabled(self.config["delegators"][0][1], False) == -1
        assert self.okcli.submit_withdraw_reward_enabled(self.config["vals"][0][1], False) == -1
        assert self.okcli.submit_reward_truncate_0(self.config["delegators"][0][1], False) == -1
        assert self.okcli.submit_reward_truncate_0(self.config["vals"][0][1], False) == -1
        assert self.okcli.edit_validator_rate("0.5", "va4", False) == -1

        # 新的程序启动，区块升级之后，没有投票提案，仍然按照佣金100%提成计算，查询验证节点投票仍然可用，验证节点取款仍然有效
        assert self.okcli.get_ledger_seq() <= self.config["upgradeLedger"], str(self.okcli.get_ledger_seq())

        self.okcli.wait_ledger(self.config["upgradeLedger"])
        result = self.okcli.query_commission(self.config["vals"][0][3])
        assert self.format_decimal(result) > 0, result
        result = self.okcli.query_commission(self.config["vals"][1][3])
        assert self.format_decimal(result) > 0, result
        result = self.okcli.query_commission(self.config["vals"][2][3])
        assert self.format_decimal(result) > 0, result
        result = self.okcli.query_commission(self.config["vals"][3][3])
        assert self.format_decimal(result) > 0, result

        # 查询分红参数 distribution_type 为0
        result = self.okcli.query_distr_params()
        assert result["distribution_type"] == 0, result

        # 支持 edit-validator-commission-rate 操作
        assert self.okcli.edit_validator_rate("1.1", "va4") == -1
        assert self.okcli.edit_validator_rate("-0.1", "va4") == -1
        assert self.okcli.edit_validator("zzzzzzzz", "va4") != -1
        assert self.okcli.edit_validator_rate("0.5", "va4") != -1

        # 不支持的操作  withdraw-all-rewards、withdraw-rewards、outstanding-rewards、query_rewards
        assert self.okcli.withdraw_all_rewards(self.config["delegators"][0][1]) == -1
        assert self.okcli.withdraw_rewards(self.config["vals"][0][3], self.config["delegators"][0][1]) == -1
        assert self.okcli.query_outstanding(self.config["vals"][0][3]) == -1
        assert self.okcli.query_rewards(self.config["delegators"][0][1], "") == -1

        # 质押delegator3 10000 okt，投票给va1
        assert self.okcli.deposit(self.config["depoistCoin"], self.config["delegators"][2][1]) != -1
        assert self.okcli.add_shares(self.vals3, self.config["delegators"][2][1]) != -1

        # proxydelegator3 质押 10000okt
        assert self.okcli.deposit(self.config["depoistCoin"], self.config["proxydelegators"][2][1]) != -1
        result = self.okcli.query_shares(self.config["proxydelegators"][2][1])
        assert self.format_decimal(result["tokens"]) == self.config["depoistCoin"], result
        assert self.format_decimal(result["shares"]) == 0, result

        # 注册 proxy3， proxydelegator3 绑定 proxy3
        assert self.okcli.deposit(self.config["depoistCoin"], self.config["proxys"][2][1]) != -1
        assert self.okcli.add_shares(self.vals3, self.config["proxys"][2][1]) != -1
        assert self.okcli.proxy_reg(self.config["proxys"][2][1]) != -1
        assert self.okcli.proxy_bind(self.config["proxys"][2][1], self.config["proxydelegators"][2][1]) != -1

        # proxydelegator3 有 tokens，shares 为 0
        resultProxydelegator3 = self.okcli.query_shares(self.config["proxydelegators"][2][1])
        assert self.format_decimal(resultProxydelegator3["tokens"]) == self.config["depoistCoin"], resultProxydelegator3
        assert self.format_decimal(resultProxydelegator3["shares"]) == 0, resultProxydelegator3
        assert resultProxydelegator3["proxy_address"] == self.config["proxys"][2][1], resultProxydelegator3

        # proxy3 的 total_delegated_tokens 等于 proxydelegator3 的 shares
        result = self.okcli.query_shares(self.config["proxys"][2][1])
        assert result["is_proxy"] == True, result
        assert self.format_decimal(result["tokens"]) == self.config["depoistCoin"], result
        assert self.format_decimal(result["total_delegated_tokens"]) == self.format_decimal(resultProxydelegator3["tokens"]), result

        logging.info("------------------------upgrate_ledger_staking end--------------------------------")

    def after_distr_proposal_before(self):
        logging.info("------------------------after_distr_proposal_before start--------------------------------")
        if self.single_debug:
            self.okcli.kill_all_process()
            self.okcli.run_all_node(self.config["nodeCount"], self.config["ledgerTime"], self.config["nodeCount"], self.config["nodes"])
            time.sleep(5)
        logging.info("------------------------after_distr_proposal_before start--------------------------------")

    def after_distr_proposal(self):
        # 11111
        logging.info("------------------------after_distr_proposal start--------------------------------")
        # 发起投票提案，修改提案，此时分红比例默认为100%，各个接口可以使用，验证节点查询抽成，提取抽成正常；委托人查询分红为0；代理人查询为0，无法提取抽成；
        # 普通人无法申请提案
        assert self.okcli.submit_change_type_proposal_onchain(self.config["delegators"][0][1]) == -1

        # 验证人可以申请提案
        proposal_num = self.okcli.submit_change_type_proposal_onchain(self.config["vals"][0][1])
        for n in self.config["delegators"]:
            self.okcli.vote(n[1], proposal_num)

        for n in self.config["proxys"]:
            self.okcli.vote(n[1], proposal_num)

        for v in self.config["vals"]:
            self.okcli.vote(v[1], proposal_num)
        self.okcli.query_proposal(proposal_num)

        # 发起分红截断提案，精度为 2
        self.set_reword_persion(2)

        # va1～va3查询抽成和outstanking一致，va4由于提前设置，不一致
        ledger = self.okcli.get_ledger_seq()
        commission_va1 = self.okcli.query_commission(self.config["vals"][0][3], ledger)
        outstanding_va1 = self.okcli.query_outstanding(self.config["vals"][0][3], ledger)
        logging.info("commission_va1:" + commission_va1 + ", outstanding_va1:" + outstanding_va1)
        self.assert_compare_same(commission_va1, outstanding_va1)

        ledger = self.okcli.get_ledger_seq()
        commission_va2 = self.okcli.query_commission(self.config["vals"][1][3], ledger)
        outstanding_va2 = self.okcli.query_outstanding(self.config["vals"][1][3], ledger)
        logging.info("commission_va2:" + commission_va2 + ", outstanding_va2:" + outstanding_va2)
        self.assert_compare_same(commission_va2, outstanding_va2)

        ledger = self.okcli.get_ledger_seq()
        commission_va3 = self.okcli.query_commission(self.config["vals"][2][3], ledger)
        outstanding_va3 = self.okcli.query_outstanding(self.config["vals"][2][3], ledger)
        logging.info("commission_va3:" + commission_va3 + ", outstanding_va3:" + outstanding_va3)
        self.assert_compare_same(commission_va3, commission_va3)

        # 等待 outstanding_va4 增加1个奖励
        outstanding_va4 = self.okcli.query_outstanding(self.config["vals"][3][3])
        self.okcli.query_outstanding_gt(self.config["vals"][3][3], self.format_decimal(outstanding_va4))

        ledger = self.okcli.get_ledger_seq()
        commission_va4 = self.okcli.query_commission(self.config["vals"][3][3], ledger)
        outstanding_va4 = self.okcli.query_outstanding(self.config["vals"][3][3], ledger)
        assert outstanding_va4 > commission_va4

        # proxy1~3, delegator1~3 查询分红为空，因为va1~va3抽成比例为100%
        result = self.okcli.query_rewards(self.config["proxys"][0][1], "")
        assert len(result["total"]) == 0, result
        result = self.okcli.query_rewards(self.config["proxys"][1][1], "")
        assert len(result["total"]) == 0, result
        result = self.okcli.query_rewards(self.config["proxys"][2][1], "")
        assert len(result["total"]) == 0, result

        result = self.okcli.query_rewards(self.config["delegators"][0][1], "")
        assert len(result["total"]) == 0, result
        result = self.okcli.query_rewards(self.config["delegators"][1][1], "")
        assert len(result["total"]) == 0, result
        result = self.okcli.query_rewards(self.config["delegators"][2][1], "")
        assert len(result["total"]) == 0, result

        # 取出va1的抽成，预期va1增加commission_va1，commission_va1 和 outstanding_va1为0
        # 保证va1增加1个奖励
        outstanding_va1 = self.okcli.query_outstanding(self.config["vals"][0][3])
        self.okcli.query_outstanding_gt(self.config["vals"][0][3], self.format_decimal(outstanding_va1))
        ledger = self.okcli.get_ledger_seq()
        beforeAmountVa1 = self.okcli.query_account(self.config["vals"][0][1])
        commission_va1 = self.okcli.query_commission(self.config["vals"][0][3], ledger)
        outstanding_va1 = self.okcli.query_outstanding(self.config["vals"][0][3], ledger)
        logging.info("commission_va1:" + str(commission_va1) + ", outstanding_va1:" + str(outstanding_va1))
        self.assert_compare_same(commission_va1, outstanding_va1)
        assert self.okcli.withdraw_commission(self.config["vals"][0][3], "va1") != -1
        ledger = self.okcli.get_ledger_seq()
        afterAmountVa1 = self.okcli.query_account(self.config["vals"][0][1])
        logging.info("afterAmountVa1:" + str(afterAmountVa1) + ", beforeAmountVa1:" + str(beforeAmountVa1))
        result = "afterAmountVa1:" + str(afterAmountVa1) + ", beforeAmountVa1:" + str(beforeAmountVa1)
        self.assert_compare_near(self.format_decimal(beforeAmountVa1) + self.format_decimal(commission_va1), self.format_decimal(afterAmountVa1))
        commission_va1 = self.okcli.query_commission(self.config["vals"][0][3], ledger)
        outstanding_va1 = self.okcli.query_outstanding(self.config["vals"][0][3], ledger)
        logging.info("commission_va1:" + str(commission_va1) + ", outstanding_va1:" + str(outstanding_va1))
        self.assert_compare_near(commission_va1, outstanding_va1)

        # 22222222
        # 查询所有人的分红，为空
        result = self.okcli.query_rewards(self.config["proxys"][0][1], "")
        assert len(result["total"]) == 0, result

        result = self.okcli.query_rewards(self.config["proxys"][1][1], "")
        assert len(result["total"]) == 0, result

        result = self.okcli.query_rewards(self.config["proxys"][2][1], "")
        assert len(result["total"]) == 0, result

        result = self.okcli.query_rewards(self.config["delegators"][0][1], "")
        assert len(result["total"]) == 0, result

        result = self.okcli.query_rewards(self.config["delegators"][1][1], "")
        assert len(result["total"]) == 0, result

        result = self.okcli.query_rewards(self.config["delegators"][2][1], "")
        assert len(result["total"]) == 0, result
        
        # 代理人提取分红，无法取出
        beforeAmountvaProxy1 = self.okcli.query_account(self.config["proxys"][0][1])
        beforeAmountvaDelegator1 = self.okcli.query_account(self.config["delegators"][0][1])
        assert self.okcli.withdraw_rewards(self.config["vals"][0][3], self.config["proxys"][0][1]) != -1
        assert self.okcli.withdraw_rewards(self.config["vals"][0][3], self.config["delegators"][0][1]) != -1
        self.okcli.wait_ledger_than(2)
        afterAmountvaProxy1 = self.okcli.query_account(self.config["proxys"][0][1])
        afterAmountvaDelegator1 = self.okcli.query_account(self.config["delegators"][0][1])
        self.assert_compare_same(beforeAmountvaProxy1, afterAmountvaProxy1)
        self.assert_compare_same(beforeAmountvaDelegator1, afterAmountvaDelegator1)

        # 验证节点2 设置分红比例1%，代理2查询奖励有值，委托人2查询奖励有值，其他人查询为空
        assert self.okcli.edit_validator("zzzzzzzz", "va2") != -1
        assert self.okcli.edit_validator_rate("0.5", "va2") != -1
        self.okcli.wait_ledger_than(20)
        result = self.okcli.query_rewards(self.config["proxys"][1][1], "")
        assert len(result["rewards"]) == 2, result
        assert len(result["rewards"][0]["reward"]) == 0, result
        assert len(result["rewards"][1]["reward"]) == 1, result

        result = self.okcli.query_rewards(self.config["delegators"][1][1], "")
        assert len(result["rewards"]) == 2, result
        assert len(result["rewards"][0]["reward"]) == 0, result
        assert len(result["rewards"][1]["reward"]) == 1, result

        result = self.okcli.query_rewards(self.config["proxys"][2][1], "")
        assert len(result["rewards"]) == 3, result
        assert len(result["rewards"][0]["reward"]) == 0, result
        assert len(result["rewards"][1]["reward"]) == 1, result
        assert len(result["rewards"][2]["reward"]) == 0, result

        result = self.okcli.query_rewards(self.config["delegators"][2][1], "")
        assert len(result["rewards"]) == 3, result
        assert len(result["rewards"][0]["reward"]) == 0, result
        assert len(result["rewards"][1]["reward"]) == 1, result
        assert len(result["rewards"][2]["reward"]) == 0, result

        result = self.okcli.query_rewards(self.config["proxydelegators"][0][1], "")
        assert len(result["total"]) == 0, result

        result = self.okcli.query_rewards(self.config["proxydelegators"][1][1], "")
        assert len(result["total"]) == 0, result

        result = self.okcli.query_rewards(self.config["proxydelegators"][2][1], "")
        assert len(result["total"]) == 0, result

        result = self.okcli.query_rewards(self.config["proxys"][0][1], "")
        assert len(result["total"]) == 0, result

        result = self.okcli.query_rewards(self.config["delegators"][0][1], "")
        assert len(result["total"]) == 0, result

        # 333333
        # 取出va1的抽成，预期va1增加commission_va1，commission_va1 和 outstanding_va1为0
        outstanding_va1 = self.okcli.query_outstanding(self.config["vals"][0][3])
        self.okcli.query_outstanding_gt(self.config["vals"][0][3], self.format_decimal(outstanding_va1))
        ledger = self.okcli.get_ledger_seq()
        beforeAmountVa1 = self.okcli.query_account(self.config["vals"][0][1])
        commission_va1 = self.okcli.query_commission(self.config["vals"][0][3], ledger)
        outstanding_va1 = self.okcli.query_outstanding(self.config["vals"][0][3], ledger)
        logging.info("commission_va1:" + str(commission_va1) + ", outstanding_va1:" + str(outstanding_va1))
        self.assert_compare_near(commission_va1, outstanding_va1)
        assert self.okcli.withdraw_commission(self.config["vals"][0][3], "va1") != -1
        ledger = self.okcli.get_ledger_seq()
        afterAmountVa1 = self.okcli.query_account(self.config["vals"][0][1])
        logging.info("afterAmountVa1:" + str(afterAmountVa1) + ", beforeAmountVa1:" + str(beforeAmountVa1))
        result = "afterAmountVa1:" + str(afterAmountVa1) + ", beforeAmountVa1:" + str(beforeAmountVa1)
        afterAmountVa1 = self.format_decimal(afterAmountVa1)
        beforeAmountVa1 = self.format_decimal(beforeAmountVa1)
        assert afterAmountVa1 >= beforeAmountVa1
        commission_va1 = self.okcli.query_commission(self.config["vals"][0][3], ledger)
        outstanding_va1 = self.okcli.query_outstanding(self.config["vals"][0][3], ledger)
        logging.info("commission_va1:" + str(commission_va1) + ", outstanding_va1:" + str(outstanding_va1))
        self.assert_compare_near(commission_va1, outstanding_va1)

        # 取出va2的抽成，预期va2增加commission_va2，commission_va2 和 outstanding_va2为0
        outstanding_va2 = self.okcli.query_outstanding(self.config["vals"][1][3])
        self.okcli.query_outstanding_gt(self.config["vals"][1][3], self.format_decimal(outstanding_va2))
        ledger = self.okcli.get_ledger_seq()
        beforeAmountVa2 = self.okcli.query_account(self.config["vals"][1][1])
        commission_va2 = self.okcli.query_commission(self.config["vals"][1][3], ledger)
        outstanding_va2 = self.okcli.query_outstanding(self.config["vals"][1][3], ledger)
        logging.info("commission_va2:" + str(commission_va2) + ", outstanding_va2:" + str(outstanding_va2))
        self.assert_compare_gt(outstanding_va2, commission_va2)
        assert self.okcli.withdraw_commission(self.config["vals"][1][3], "va2") != -1
        ledger = self.okcli.get_ledger_seq()
        afterAmountVa2 = self.okcli.query_account(self.config["vals"][1][1])
        logging.info("afterAmountVa2:" + str(afterAmountVa2) + ", beforeAmountVa2:" + str(beforeAmountVa2))
        result = "afterAmountVa2:" + str(afterAmountVa2) + ", beforeAmountVa2:" + str(beforeAmountVa2)
        self.assert_compare_near(self.format_decimal(beforeAmountVa2) + self.format_decimal(commission_va2), self.format_decimal(afterAmountVa2))
        commission_va2 = self.okcli.query_commission(self.config["vals"][1][3], ledger)
        outstanding_va2 = self.okcli.query_outstanding(self.config["vals"][1][3], ledger)
        logging.info("commission_va2:" + str(commission_va2) + ", outstanding_va2:" + str(outstanding_va2))
        self.assert_compare_gt(outstanding_va2, commission_va2)
        
        # 取出va4的抽成，预期va4增加commission_va4，commission_va4 和 outstanding_va4为0
        outstanding_va4 = self.okcli.query_outstanding(self.config["vals"][3][3])
        self.okcli.query_outstanding_gt(self.config["vals"][3][3], self.format_decimal(outstanding_va4))
        ledger = self.okcli.get_ledger_seq()
        beforeAmountVa4 = self.okcli.query_account(self.config["vals"][3][1])
        commission_va4 = self.okcli.query_commission(self.config["vals"][3][3], ledger)
        outstanding_va4 = self.okcli.query_outstanding(self.config["vals"][3][3], ledger)
        logging.info("commission_va4:" + str(commission_va4) + ", outstanding_va4:" + str(outstanding_va4))
        self.assert_compare_gt(outstanding_va4, commission_va4)
        result = self.okcli.withdraw_commission(self.config["vals"][3][3], "va4")
        afterAmountVa4 = self.okcli.query_account(self.config["vals"][3][1])
        logging.info("afterAmountVa4:" + str(afterAmountVa4) + ", beforeAmountVa4:" + str(beforeAmountVa4))
        result = "afterAmountVa4:" + str(afterAmountVa4) + ", beforeAmountVa4:" + str(beforeAmountVa4)
        self.assert_compare_near(self.format_decimal(beforeAmountVa4) + self.format_decimal(commission_va4), self.format_decimal(afterAmountVa4))
        ledger = self.okcli.get_ledger_seq()
        commission_va4 = self.okcli.query_commission(self.config["vals"][3][3], ledger)
        outstanding_va4 = self.okcli.query_outstanding(self.config["vals"][3][3], ledger)
        logging.info("commission_va4:" + str(commission_va4) + ", outstanding_va4:" + str(outstanding_va4))
        self.assert_compare_gt(outstanding_va4, commission_va4)

        # delegator1无法取出va1的分红，因为验证节点va1没有设置比例
        beforeAmount = self.okcli.query_account(self.config["proxys"][0][1])
        assert self.okcli.withdraw_rewards(self.config["vals"][0][3], self.config["proxys"][0][1]) != -1
        afterAmount = self.okcli.query_account(self.config["proxys"][0][1])
        self.assert_compare_same(beforeAmount, afterAmount)
        beforeAmount = self.okcli.query_account(self.config["delegators"][0][1])
        assert self.okcli.withdraw_rewards(self.config["vals"][0][3], self.config["delegators"][0][1]) != -1
        afterAmount = self.okcli.query_account(self.config["delegators"][0][1])
        self.assert_compare_same(beforeAmount, afterAmount)

        # proxy2 取出va2的分红
        self.okcli.query_total_rewards_gt_precision(self.config["proxys"][1][1], self.config["vals"][1][3], 0, self.PRECISION)
        rewards = self.okcli.query_rewards(self.config["proxys"][1][1], self.config["vals"][1][3])[0]["amount"]
        beforeAmount = self.okcli.query_account(self.config["proxys"][1][1])
        assert self.okcli.withdraw_rewards(self.config["vals"][1][3], self.config["proxys"][1][1]) != -1
        afterAmount = self.okcli.query_account(self.config["proxys"][1][1])
        assert float(rewards) > self.PRECISION_REWARDS, rewards
        diff = self.format_decimal_precision(afterAmount, self.PRECISION + 1) - (self.format_decimal_precision(beforeAmount, self.PRECISION + 1)) 
        assert diff > self.PRECISION_REWARDS_DIFF, str(diff)

        # delegator3 取出所有的分红
        rewards = self.okcli.query_rewards(self.config["delegators"][2][1], "")["total"][0]["amount"]
        beforeAmount = self.okcli.query_account(self.config["delegators"][2][1])
        assert self.okcli.withdraw_all_rewards(self.config["delegators"][2][1]) != -1
        afterAmount = self.okcli.query_account(self.config["delegators"][2][1])
        diff = self.format_decimal_precision(afterAmount, self.PRECISION + 1) - (self.format_decimal_precision(beforeAmount, self.PRECISION + 1)) 
        assert diff > self.PRECISION_REWARDS_DIFF, str(diff)

        # 新增验证节点，进行质押
        assert self.okcli.create_validator(self.config["vaAddadmin16"]) != -1
        assert self.okcli.edit_validator("zzzzzzzz", self.config["vaAddadmin16"]) != -1
        assert self.okcli.edit_validator_rate("0.5", self.config["vaAddadmin16"]) != -1
        assert self.okcli.deposit(self.config["depoistCoin"], self.config["proxys"][3][1]) != -1
        assert self.okcli.add_shares(self.valsall, self.config["proxys"][3][1]) != -1
        assert self.okcli.deposit(self.config["depoistCoin"], self.config["delegators"][3][1]) != -1
        assert self.okcli.add_shares(self.valsall, self.config["delegators"][3][1]) != -1
        assert self.okcli.deposit(self.config["depoistCoin"], self.config["proxydelegators"][3][1]) != -1
        assert self.okcli.proxy_reg(self.config["proxys"][3][1]) != -1
        assert self.okcli.proxy_bind(self.config["proxys"][3][1], self.config["proxydelegators"][3][1]) != -1

        # proxydelegator4 有 tokens，shares 为 0
        resultProxydelegator4 = self.okcli.query_shares(self.config["proxydelegators"][3][1])
        assert self.format_decimal(resultProxydelegator4["tokens"]) == self.config["depoistCoin"], resultProxydelegator4
        assert self.format_decimal(resultProxydelegator4["shares"]) == 0, resultProxydelegator4
        assert resultProxydelegator4["proxy_address"] == self.config["proxys"][3][1], resultProxydelegator4

        # proxy4 的 total_delegated_tokens 等于 proxydelegator4 的 shares
        result = self.okcli.query_shares(self.config["proxys"][3][1])
        assert result["is_proxy"] == True, result
        assert self.format_decimal(result["tokens"]) == self.config["depoistCoin"], result
        assert self.format_decimal(result["total_delegated_tokens"]) == self.format_decimal(resultProxydelegator4["tokens"]), result
        

        # 等待 proxy2 和 proxy4 的奖励大于0
        self.okcli.query_total_rewards_gt_precision(self.config["proxys"][1][1], "", 0, self.PRECISION)
        self.okcli.query_total_rewards_gt_precision(self.config["proxys"][3][1], "", 0, self.PRECISION)

        logging.info("------------------------after_distr_proposal end--------------------------------")

    def change_to_off_chain_before(self):
        logging.info("------------------------change_to_off_chain_before start--------------------------------")
        if self.single_debug:
            self.okcli.kill_all_process()
            self.okcli.run_all_node(self.config["nodeCount"], self.config["ledgerTime"], self.config["nodeCount"], self.config["nodes"])
            time.sleep(5)
        logging.info("------------------------change_to_off_chain_before end--------------------------------")


    def change_to_off_chain(self):
        logging.info("------------------------change_to_off_chain start--------------------------------")
        # 11111111
        # 普通人无法发起提案
        assert self.okcli.submit_change_type_proposal_offchain(self.config["delegators"][0][1]) == -1

        # 修改成链下分红
        proposal_num = self.okcli.submit_change_type_proposal_offchain(self.config["vals"][0][1])
        for n in self.config["delegators"]:
            self.okcli.vote(n[1], proposal_num)

        for n in self.config["proxys"]:
            self.okcli.vote(n[1], proposal_num)

        for v in self.config["vals"]:
            self.okcli.vote(v[1], proposal_num)
        self.okcli.query_proposal(proposal_num)

        # delegator1无法取出va1的分红，因为验证节点va1没有设置比例
        beforeAmount = self.okcli.query_account(self.config["proxys"][0][1])
        assert self.okcli.withdraw_rewards(self.config["vals"][0][3], self.config["proxys"][0][1]) != -1
        afterAmount = self.okcli.query_account(self.config["proxys"][0][1])
        self.assert_compare_same(beforeAmount, afterAmount)

        # proxy2 取出之前的所有的分红，仍可取出
        rewards = self.okcli.query_rewards(self.config["proxys"][1][1], "")["total"][0]["amount"]
        beforeAmount = self.okcli.query_account(self.config["proxys"][1][1])
        assert self.okcli.withdraw_all_rewards(self.config["proxys"][1][1]) != -1
        afterAmount = self.okcli.query_account(self.config["proxys"][1][1])
        assert float(rewards) > self.PRECISION_REWARDS, rewards
        diff = self.format_decimal_precision(afterAmount, self.PRECISION + 1) - (self.format_decimal_precision(beforeAmount, self.PRECISION + 1)) 
        assert diff > self.PRECISION_REWARDS_DIFF, str(diff)

        # 等待n个出块周期，确保proxy2不再接受分红
        self.okcli.wait_ledger_than(20)
        result = self.okcli.query_rewards(self.config["proxys"][1][1], "")
        assert len(result["total"]) == 0, result

        # 22222222
        # 验证节点1 设置分红比例1%
        assert self.okcli.edit_validator("zzzzzzzz", "va1") != -1
        assert self.okcli.edit_validator_rate("0.5", "va1") != -1
        self.okcli.wait_ledger_than(20)

        # proxy1 的分红仍然为0
        result = self.okcli.query_rewards(self.config["proxys"][0][1], "")
        assert len(result["total"]) == 0, result

        # delegator1 的分红仍然为0
        result = self.okcli.query_rewards(self.config["delegators"][0][1], "")
        assert len(result["total"]) == 0, result

        # proxy4 取出所有的分红，仍可取出
        rewards = self.okcli.query_rewards(self.config["proxys"][3][1], "")["total"][0]["amount"]
        assert float(rewards) > self.PRECISION_REWARDS, rewards
        beforeAmount = self.okcli.query_account(self.config["proxys"][3][1])
        assert self.okcli.withdraw_all_rewards(self.config["proxys"][3][1]) != -1
        afterAmount = self.okcli.query_account(self.config["proxys"][3][1])
        assert float(rewards) > self.PRECISION_REWARDS, rewards
        diff = self.format_decimal_precision(afterAmount, self.PRECISION + 1) - (self.format_decimal_precision(beforeAmount, self.PRECISION + 1)) 
        assert diff > self.PRECISION_REWARDS_DIFF, str(diff)

        # 新增质押人5
        assert self.okcli.deposit(self.config["depoistCoin"], self.config["proxys"][4][1]) != -1
        assert self.okcli.add_shares(self.valsall, self.config["proxys"][4][1]) != -1

        assert self.okcli.deposit(self.config["depoistCoin"], self.config["delegators"][4][1]) != -1
        assert self.okcli.add_shares(self.valsall, self.config["delegators"][4][1]) != -1
        assert self.okcli.deposit(self.config["depoistCoin"], self.config["proxydelegators"][4][1]) != -1

        assert self.okcli.proxy_reg(self.config["proxys"][4][1]) != -1
        assert self.okcli.proxy_bind(self.config["proxys"][4][1], self.config["proxydelegators"][4][1]) != -1

        # 333333333
        # 取出v1的分红，预期正常
        outstanding_va1 = self.okcli.query_outstanding(self.config["vals"][0][3])
        self.okcli.query_outstanding_gt(self.config["vals"][0][3], self.format_decimal(outstanding_va1))
        ledger = self.okcli.get_ledger_seq()
        beforeAmountVa1 = self.okcli.query_account(self.config["vals"][0][1])
        commission_va1 = self.okcli.query_commission(self.config["vals"][0][3], ledger)
        outstanding_va1 = self.okcli.query_outstanding(self.config["vals"][0][3], ledger)
        logging.info("commission_va1:" + str(commission_va1) + ", outstanding_va1:" + str(outstanding_va1))
        self.assert_compare_same(outstanding_va1, commission_va1)
        assert self.okcli.withdraw_commission(self.config["vals"][0][3], "va1") != -1
        ledger = self.okcli.get_ledger_seq()
        afterAmountVa1 = self.okcli.query_account(self.config["vals"][0][1])
        logging.info("afterAmountVa1:" + str(afterAmountVa1) + ", beforeAmountVa1:" + str(beforeAmountVa1))
        result = "afterAmountVa1:" + str(afterAmountVa1) + ", beforeAmountVa1:" + str(beforeAmountVa1)
        self.assert_compare_near(self.format_decimal(beforeAmountVa1) + self.format_decimal(commission_va1), self.format_decimal(afterAmountVa1))
        commission_va1 = self.okcli.query_commission(self.config["vals"][0][3], ledger)
        outstanding_va1 = self.okcli.query_outstanding(self.config["vals"][0][3], ledger)
        logging.info("commission_va1:" + str(commission_va1) + ", outstanding_va1:" + str(outstanding_va1))
        self.assert_compare_same(outstanding_va1, commission_va1)

        # 查询正常
        result = self.okcli.query_commission(self.config["vals"][1][3])
        result = self.okcli.query_commission(self.config["vals"][2][3])
        result = self.okcli.query_commission(self.config["vals"][3][3])
        result = self.okcli.query_commission(self.config["vaadmin16"])

        ledger = self.okcli.get_ledger_seq()
        result = self.okcli.query_outstanding(self.config["vals"][1][3], ledger)
        result = self.okcli.query_outstanding(self.config["vals"][2][3], ledger)
        result = self.okcli.query_outstanding(self.config["vals"][3][3], ledger)
        result = self.okcli.query_outstanding(self.config["vaadmin16"], ledger)

        # 查询分红正常
        result = self.okcli.query_rewards(self.config["proxys"][0][1], "")
        assert len(result["total"]) == 0, result
        result = self.okcli.query_rewards(self.config["proxys"][1][1], "")
        assert len(result["total"]) == 0, result
        result = self.okcli.query_rewards(self.config["proxys"][2][1], "")
        assert len(result["total"]) > 0, result
        result = self.okcli.query_rewards(self.config["proxys"][3][1], "")
        assert len(result["total"]) == 0, result
        result = self.okcli.query_rewards(self.config["proxys"][4][1], "")
        assert len(result["total"]) == 0, result

        result = self.okcli.query_rewards(self.config["delegators"][0][1], "")
        assert len(result["total"]) == 0, result
        result = self.okcli.query_rewards(self.config["delegators"][1][1], "")
        assert len(result["total"]) > 0, result
        result = self.okcli.query_rewards(self.config["delegators"][2][1], "")
        assert len(result["total"]) > 0, result
        result = self.okcli.query_rewards(self.config["delegators"][3][1], "")
        assert len(result["total"]) > 0, result
        result = self.okcli.query_rewards(self.config["delegators"][4][1], "")
        assert len(result["total"]) == 0, result

        # 再次尝试取出 proxy4 所有分红，失败
        self.okcli.wait_ledger_than(20)
        beforeAmount = self.okcli.query_account(self.config["proxys"][3][1])
        assert self.okcli.withdraw_all_rewards(self.config["proxys"][3][1]) != -1
        afterAmount = self.okcli.query_account(self.config["proxys"][3][1])
        diff = self.format_decimal_precision(afterAmount, self.PRECISION + 1) - (self.format_decimal_precision(beforeAmount, self.PRECISION + 1)) 
        assert diff <= 0, str(diff)

        # 尝试取出 proxy5 所有分红，失败
        beforeAmount = self.okcli.query_account(self.config["proxys"][4][1])
        assert self.okcli.withdraw_all_rewards(self.config["proxys"][4][1]) != -1
        afterAmount = self.okcli.query_account(self.config["proxys"][4][1])
        diff = self.format_decimal_precision(afterAmount, self.PRECISION + 1) - (self.format_decimal_precision(beforeAmount, self.PRECISION + 1)) 
        assert diff <= 0, str(diff)

        # 参数为0
        result = self.okcli.query_distr_params()
        assert result["distribution_type"] == 0, result

        logging.info("------------------------change_to_off_chain end--------------------------------")

    def change_to_on_chain_before(self):
        logging.info("------------------------change_to_on_chain_before start--------------------------------")
        if self.single_debug:
            self.okcli.run_all_node(self.config["nodeCount"], self.config["ledgerTime"], self.config["nodeCount"], self.config["nodes"])
            time.sleep(5)
        
        logging.info("------------------------change_to_on_chain_before end--------------------------------")

    def change_to_on_chain(self):
        logging.info("------------------------change_to_on_chain start--------------------------------")
        # 1111111111
        # 普通人无法申请提案
        assert self.okcli.submit_change_type_proposal_onchain(self.config["delegators"][0][1]) == -1

        # 发起投票提案，修改提案链上分红
        proposal_num = self.okcli.submit_change_type_proposal_onchain(self.config["vals"][1][1])
        self.okcli.query_proposal(proposal_num)
        
        for n in self.config["delegators"]:
            self.okcli.vote(n[1], proposal_num)

        for n in self.config["proxys"]:
            self.okcli.vote(n[1], proposal_num)

        for v in self.config["vals"]:
            self.okcli.vote(v[1], proposal_num)

        self.okcli.query_proposal(proposal_num)
        self.okcli.wait_ledger_than(20)

        # 222222222
        # 查询 delegator 所有奖励
        result = self.okcli.query_rewards(self.config["delegators"][0][1], "")
        assert len(result["total"]) > 0, result
        result = self.okcli.query_rewards(self.config["delegators"][1][1], "")
        assert len(result["total"]) > 0, result
        result = self.okcli.query_rewards(self.config["delegators"][2][1], "")
        assert len(result["total"]) > 0, result
        result = self.okcli.query_rewards(self.config["delegators"][3][1], "")
        assert len(result["total"]) > 0, result
        result = self.okcli.query_rewards(self.config["delegators"][4][1], "")
        assert len(result["total"]) > 0, result

        # 查询 delegator1 、proxy1 的 v1 分红正常，proxydelegator1 不存在质押关系
        result = self.okcli.query_rewards(self.config["proxys"][0][1], self.config["vals"][0][3])
        assert len(result) > 0, result
        result = self.okcli.query_rewards(self.config["delegators"][0][1], self.config["vals"][0][3])
        assert len(result) > 0, result
        result = self.okcli.query_rewards(self.config["proxydelegators"][0][1], self.config["vals"][0][3])
        assert result == -1, result

        # 查询 delegator3 、proxy3的 v3 分红为空， proxydelegator3 不存在质押关系
        result = self.okcli.query_rewards(self.config["proxys"][2][1], self.config["vals"][2][3])
        assert len(result) == 0, result
        result = self.okcli.query_rewards(self.config["delegators"][2][1], self.config["vals"][2][3])
        assert len(result) == 0, result
        result = self.okcli.query_rewards(self.config["proxydelegators"][2][1], self.config["vals"][2][3])
        assert result == -1, result

        # 设置 proxy3 的取款人地址
        assert self.okcli.set_withdraw_addr(self.config["withdrawaddress"], self.config["proxys"][2][1]) != -1
        assert self.okcli.set_withdraw_addr(self.config["withdrawaddress"], self.config["delegators"][2][1]) != -1    
        assert self.okcli.set_withdraw_addr(self.config["withdrawaddress"], self.config["delegators"][3][1]) != -1
        assert self.okcli.set_withdraw_addr(self.config["withdrawaddress"], self.config["delegators"][4][1]) != -1

        # 验证节点3 设置分红比例50%
        assert self.okcli.edit_validator("zzzzzzzz", "va3") != -1
        assert self.okcli.edit_validator_rate("0.5", "va3") != -1

        assert self.okcli.deposit(self.config["addDepoistCoin"], self.config["proxys"][2][1]) != -1
        self.okcli.wait_ledger_than(20)
        # 查询 delegator3 、proxy3的 v3 分红正常， proxydelegator3 不存在质押关系
        result = self.okcli.query_rewards(self.config["proxys"][2][1], self.config["vals"][2][3])
        assert len(result) > 0, result
        result = self.okcli.query_rewards(self.config["proxys"][2][1], "")
        result = self.okcli.query_rewards(self.config["delegators"][2][1], self.config["vals"][2][3])
        assert len(result) > 0, result
        result = self.okcli.query_rewards(self.config["proxydelegators"][2][1], self.config["vals"][2][3])
        assert result == -1, result

        # 33333
        # 增加 proxy3 自身投票，预期分红到账
        result = self.okcli.query_rewards(self.config["proxys"][2][1], "")
        rewards = result["total"][0]["amount"]
        result = self.okcli.query_rewards(self.config["proxys"][2][1], self.config["vals"][2][3])
        assert len(result) > 0, result
        beforeAmount = self.okcli.query_account(self.config["withdrawaddress"])
        self.okcli.query_total_rewards_gt_precision(self.config["proxys"][2][1], self.config["vals"][2][3], 0, self.PRECISION)
        result = self.okcli.deposit(self.config["addDepoistCoin"], self.config["proxys"][2][1])
        self.okcli.wait_ledger_than(2)
        result = self.okcli.query_rewards(self.config["proxys"][2][1], "")
        self.assert_compare_near(result["total"][0]["amount"], 1)
        afterAmount = self.okcli.query_account(self.config["withdrawaddress"])
        assert float(rewards) > self.PRECISION_REWARDS, rewards
        diff = self.format_decimal_precision(afterAmount, self.PRECISION + 1) - (self.format_decimal_precision(beforeAmount, self.PRECISION + 1)) 
        assert diff > self.PRECISION_REWARDS_DIFF, str(diff)

        # 减少 proxy3 自身投票，预期分红到账
        self.okcli.wait_ledger_than(20)
        result = self.okcli.query_rewards(self.config["proxys"][2][1], "")
        rewards = result["total"][0]["amount"]
        result = self.okcli.query_rewards(self.config["proxys"][2][1], self.config["vals"][2][3])
        assert len(result) > 0, result
        beforeAmount = self.okcli.query_account(self.config["withdrawaddress"])
        assert self.okcli.withdraw(self.config["addDepoistCoin"], self.config["proxys"][2][1]) != -1
        self.okcli.wait_ledger_than(2)
        result = self.okcli.query_rewards(self.config["proxys"][2][1], "")
        self.assert_compare_near(result["total"][0]["amount"], 1)
        afterAmount = self.okcli.query_account(self.config["withdrawaddress"])
        assert float(rewards) > self.PRECISION_REWARDS, rewards
        diff = self.format_decimal_precision(afterAmount, self.PRECISION + 1) - (self.format_decimal_precision(beforeAmount, self.PRECISION + 1)) 
        assert diff > self.PRECISION_REWARDS_DIFF, str(diff)

        # 增加 proxy3 的代理投票，预期分红到账
        self.okcli.wait_ledger_than(20)
        result = self.okcli.query_rewards(self.config["proxys"][2][1], "")
        rewards = result["total"][0]["amount"]
        result = self.okcli.query_rewards(self.config["proxys"][2][1], self.config["vals"][2][3])
        assert len(result) > 0, result
        beforeAmount = self.okcli.query_account(self.config["withdrawaddress"])
        assert self.okcli.deposit(self.config["depoistCoin"], self.config["proxydelegators"][2][1]) != -1
        self.okcli.wait_ledger_than(2)
        result = self.okcli.query_rewards(self.config["proxys"][2][1], "")
        self.assert_compare_near(result["total"][0]["amount"], 1)
        afterAmount = self.okcli.query_account(self.config["withdrawaddress"])
        assert float(rewards) > self.PRECISION_REWARDS, rewards
        diff = self.format_decimal_precision(afterAmount, self.PRECISION + 1) - (self.format_decimal_precision(beforeAmount, self.PRECISION + 1)) 
        assert diff > self.PRECISION_REWARDS_DIFF, str(diff)

        # 减少 proxy3 的代理投票，预期分红到账
        self.okcli.wait_ledger_than(20)
        self.okcli.query_total_rewards_gt_precision(self.config["proxys"][2][1], self.config["vals"][2][3], 0, self.PRECISION)
        result = self.okcli.query_rewards(self.config["proxys"][2][1], "")
        rewards = result["total"][0]["amount"]
        result = self.okcli.query_rewards(self.config["proxys"][2][1], self.config["vals"][2][3])
        assert len(result) > 0, result
        beforeAmount = self.okcli.query_account(self.config["withdrawaddress"])
        assert self.okcli.withdraw(self.config["depoistCoin"], self.config["proxydelegators"][2][1]) != -1
        self.okcli.wait_ledger_than(2)
        result = self.okcli.query_rewards(self.config["proxys"][2][1], "")
        self.assert_compare_near(result["total"][0]["amount"], 1)
        afterAmount = self.okcli.query_account(self.config["withdrawaddress"])
        assert float(rewards) > self.PRECISION_REWARDS, rewards
        diff = self.format_decimal_precision(afterAmount, self.PRECISION + 1) - (self.format_decimal_precision(beforeAmount, self.PRECISION + 1)) 
        assert diff > self.PRECISION_REWARDS_DIFF, str(diff)

        # 解绑 proxy3 代理，预期分红到账
        self.okcli.query_total_rewards_gt_precision(self.config["proxys"][2][1], self.config["vals"][2][3], 0, self.PRECISION)
        result = self.okcli.query_rewards(self.config["proxys"][2][1], "")
        rewards = result["total"][0]["amount"]
        result = self.okcli.query_rewards(self.config["proxys"][2][1], self.config["vals"][2][3])
        assert len(result) > 0, result

        # unreg 也会分红
        self.okcli.set_withdraw_addr(self.config["withdrawaddress"], self.config["proxys"][2][1])
        beforeAmount = self.okcli.query_account(self.config["withdrawaddress"])
        self.okcli.query_total_rewards_gt_precision(self.config["proxys"][2][1], self.config["vals"][0][3], 0, self.PRECISION)
        assert self.okcli.unreg(self.config["proxys"][2][1]) != -1
        after = self.okcli.query_account(self.config["withdrawaddress"])
        self.okcli.wait_ledger_than(2)
        result = self.okcli.query_rewards(self.config["proxys"][2][1], "")
        self.assert_compare_near(result["total"][0]["amount"], 1)
        afterAmount = self.okcli.query_account(self.config["withdrawaddress"])
        assert float(rewards) > self.PRECISION_REWARDS, rewards
        diff = self.format_decimal_precision(afterAmount, self.PRECISION + 1) - (self.format_decimal_precision(beforeAmount, self.PRECISION + 1)) 
        assert diff > self.PRECISION_REWARDS_DIFF, str(diff)

        # 重新注册 proxy3 代理，分红仍然正常
        assert self.okcli.deposit(self.config["depoistCoin"], self.config["proxys"][2][1]) != -1
        assert self.okcli.add_shares(self.vals3, self.config["proxys"][2][1]) != -1
        # reg也会分红
        self.okcli.query_total_rewards_gt_precision(self.config["proxys"][2][1], self.config["vals"][2][3], 0, self.PRECISION)
        self.okcli.set_withdraw_addr(self.config["withdrawaddress"], self.config["proxys"][2][1])
        before = self.okcli.query_account(self.config["withdrawaddress"])
        self.okcli.query_total_rewards_gt_precision(self.config["proxys"][2][1], self.config["vals"][2][3], 0, self.PRECISION)
        assert self.okcli.proxy_reg(self.config["proxys"][2][1]) != -1
        after = self.okcli.query_account(self.config["withdrawaddress"])
        self.okcli.query_total_rewards_gt_precision(self.config["proxys"][2][1], self.config["vals"][2][3], 0, self.PRECISION)
        assert self.okcli.proxy_bind(self.config["proxys"][2][1], self.config["proxydelegators"][2][1]) != -1
        self.okcli.wait_ledger_than(2)
        resultProxydelegator3 = self.okcli.query_shares(self.config["proxydelegators"][2][1])
        assert self.format_decimal(resultProxydelegator3["tokens"]) == self.config["depoistCoin"], resultProxydelegator3
        assert self.format_decimal(resultProxydelegator3["shares"]) == 0, resultProxydelegator3
        assert resultProxydelegator3["proxy_address"] == self.config["proxys"][2][1], resultProxydelegator3

        result = self.okcli.query_shares(self.config["proxys"][2][1])
        assert result["is_proxy"] == True, result
        assert self.format_decimal(result["total_delegated_tokens"]) == self.format_decimal(resultProxydelegator3["tokens"]), result

        444444
        # 增加 delegator3 的投票，预期分红到账
        self.okcli.wait_ledger_than(20)
        result = self.okcli.query_rewards(self.config["delegators"][2][1], "")
        rewards = result["total"][0]["amount"]
        result = self.okcli.query_rewards(self.config["delegators"][2][1], self.config["vals"][2][3])
        assert len(result) > 0, result
        self.okcli.query_total_rewards_gt_precision(self.config["proxys"][2][1], self.config["vals"][2][3], 0, self.PRECISION)
        beforeAmount = self.okcli.query_account(self.config["withdrawaddress"])
        assert self.okcli.deposit(self.config["addDepoistCoin"], self.config["delegators"][2][1]) != -1
        self.okcli.wait_ledger_than(2)
        result = self.okcli.query_rewards(self.config["delegators"][2][1], "")
        self.assert_compare_near(result["total"][0]["amount"], 1)
        afterAmount = self.okcli.query_account(self.config["withdrawaddress"])
        assert float(rewards) > self.PRECISION_REWARDS, rewards
        diff = self.format_decimal_precision(afterAmount, self.PRECISION + 1) - (self.format_decimal_precision(beforeAmount, self.PRECISION + 1)) 
        assert diff > self.PRECISION_REWARDS_DIFF, str(diff)

        # 取出 delegator3 的所有投票，预期分红到账
        self.okcli.wait_ledger_than(20)
        result = self.okcli.query_rewards(self.config["delegators"][2][1], self.config["vals"][2][3])
        assert len(result) > 0, result
        beforeAmount = self.okcli.query_account(self.config["withdrawaddress"])
        result = self.okcli.query_rewards(self.config["delegators"][2][1], "")
        rewards = 0
        for v in result["rewards"]:
            if len(v["reward"]) > 0:
                rewards += self.format_decimal_precision(v["reward"][0]["amount"], self.PRECISION + 1)
        logging.info("rewards:" + str(rewards))
        
        self.okcli.query_total_rewards_gt_precision(self.config["proxys"][2][1], self.config["vals"][2][3], 0, self.PRECISION)
        result = self.okcli.query_shares(self.config["delegators"][2][1])
        result = self.okcli.withdraw(self.format_decimal(result["tokens"]), self.config["delegators"][2][1])
        self.okcli.wait_ledger_than(2)
        result = self.okcli.query_rewards(self.config["delegators"][2][1], "")
        assert result == -1, result
        afterAmount = self.okcli.query_account(self.config["withdrawaddress"])
        assert float(rewards) > self.PRECISION_REWARDS, rewards
        diff = self.format_decimal_precision(afterAmount, self.PRECISION + 1) - (self.format_decimal_precision(beforeAmount, self.PRECISION + 1)) 
        assert diff > self.PRECISION_REWARDS_DIFF, str(diff)

        # 取出 delegator3 的投票，等待30秒，再次取出分红为0
        self.okcli.wait_ledger_than(20)
        result = self.okcli.query_rewards(self.config["delegators"][2][1], "")
        assert result == -1, result
        result = self.okcli.query_rewards(self.config["delegators"][2][1], self.config["vals"][2][3])
        assert result == -1, result
        beforeAmount = self.okcli.query_account(self.config["withdrawaddress"])
        self.okcli.withdraw_all_rewards(self.config["delegators"][2][1])
        self.okcli.wait_ledger_than(2)
        afterAmount = self.okcli.query_account(self.config["withdrawaddress"])
        diff = self.format_decimal_precision(afterAmount, self.PRECISION + 1) - (self.format_decimal_precision(beforeAmount, self.PRECISION + 1)) 
        assert diff == 0, str(diff)

        # delegator3 再次质押，30秒后仍有奖励
        assert self.okcli.deposit(self.config["depoistCoin"], self.config["delegators"][2][1]) != -1
        assert self.okcli.add_shares(self.vals3, self.config["delegators"][2][1]) != -1
        self.okcli.wait_ledger_than(20)
        self.okcli.query_total_rewards_gt_precision(self.config["delegators"][2][1], self.config["vals"][2][3], 0, self.PRECISION)
        result = self.okcli.query_rewards(self.config["delegators"][2][1], "")
        rewards = result["total"][0]["amount"]
        assert len(result["total"]) == 1
        assert len(result["rewards"]) == 3
        beforeAmount = self.okcli.query_account(self.config["withdrawaddress"])
        assert self.okcli.withdraw(self.config["depoistCoin"], self.config["delegators"][2][1]) != -1
        afterAmount = self.okcli.query_account(self.config["withdrawaddress"])
        assert float(rewards) > self.PRECISION_REWARDS, rewards
        diff = self.format_decimal_precision(afterAmount, self.PRECISION + 1) - (self.format_decimal_precision(beforeAmount, self.PRECISION + 1)) 
        assert diff > self.PRECISION_REWARDS_DIFF, str(diff)

        # 555555
        # 销毁验证节点
        result = self.okcli.query_validator(self.config["vaadmin16"])
        assert result["jailed"] == False, result
        assert self.okcli.destroy_validator(self.config["vaAddadmin16"]) != -1
        result = self.okcli.query_validator(self.config["vaadmin16"])
        assert result["jailed"] == True, result

        # 销毁验证节点，取出自己抽成
        ledger = self.okcli.get_ledger_seq()
        beforeAmount = self.okcli.query_account(self.config["vaAddadmin16"])
        commission = self.okcli.query_commission(self.config["vaadmin16"], ledger)
        outstanding = self.okcli.query_outstanding(self.config["vaadmin16"], ledger)
        logging.info("commission:" + str(commission) + ", outstanding:" + str(outstanding))
        self.assert_compare_gt(outstanding, commission)
        assert self.okcli.withdraw_commission(self.config["vaadmin16"], self.config["vaAddadmin16"]) != -1
        afterAmount = self.okcli.query_account(self.config["vaAddadmin16"])
        logging.info("afterAmount:" + str(afterAmount) + ", beforeAmount:" + str(beforeAmount))
        result = "afterAmount:" + str(afterAmount) + ", beforeAmount:" + str(beforeAmount)
        self.assert_compare_near(self.format_decimal(beforeAmount) + self.format_decimal(commission), self.format_decimal(afterAmount))
        ledger = self.okcli.get_ledger_seq()
        commission = self.okcli.query_commission(self.config["vaadmin16"], ledger)
        outstanding = self.okcli.query_outstanding(self.config["vaadmin16"], ledger)
        logging.info("commission:" + str(commission) + ", outstanding:" + str(outstanding))
        self.assert_compare_gt(outstanding, commission)
        assert self.format_decimal(commission) == 0

        # delegator4 取出质押
        self.okcli.wait_ledger_than(20)
        self.okcli.query_total_rewards_gt_precision(self.config["delegators"][3][1], self.config["vaadmin16"], 0, self.PRECISION)
        self.okcli.withdraw_rewards(self.config["vaadmin16"], self.config["delegators"][3][1])

        result = self.okcli.query_rewards(self.config["delegators"][3][1], "")
        rewards = 0
        for v in result["rewards"]:
            if len(v["reward"]) > 0:
                rewards += self.format_decimal_precision(v["reward"][0]["amount"], self.PRECISION + 1)
        logging.info("rewards:" + str(rewards))

        self.okcli.query_total_rewards_gt_precision(self.config["delegators"][3][1], self.config["vals"][2][3], 0, self.PRECISION)
        beforeAmount = self.okcli.query_account(self.config["withdrawaddress"])
        result = self.okcli.query_shares(self.config["delegators"][3][1])
        assert self.okcli.withdraw(self.format_decimal(result["tokens"]), self.config["delegators"][3][1]) != -1
        self.okcli.wait_ledger_than(2)
        result = self.okcli.query_rewards(self.config["delegators"][3][1], self.config["vaadmin16"])
        assert result == -1, result
        afterAmount = self.okcli.query_account(self.config["withdrawaddress"])
        assert float(rewards) > self.PRECISION_REWARDS, rewards
        diff = self.format_decimal_precision(afterAmount, self.PRECISION + 1) - (self.format_decimal_precision(beforeAmount, self.PRECISION + 1)) 
        assert diff > self.PRECISION_REWARDS_DIFF, str(diff)

        # 30秒后，验证节点不再有抽成
        self.okcli.wait_ledger_than(20)
        ledger = self.okcli.get_ledger_seq()
        beforeAmount = self.okcli.query_account(self.config["vaAddadmin16"])
        commission = self.okcli.query_commission(self.config["vaadmin16"], ledger)
        outstanding = self.okcli.query_outstanding(self.config["vaadmin16"], ledger)
        logging.info("commission:" + str(commission) + ", outstanding:" + str(outstanding))
        self.assert_compare_gt(outstanding, commission)
        assert self.okcli.withdraw_commission(self.config["vaadmin16"], self.config["vaAddadmin16"]) != -1
        afterAmount = self.okcli.query_account(self.config["vaAddadmin16"])
        logging.info("afterAmount:" + str(afterAmount) + ", beforeAmount:" + str(beforeAmount))
        result = "afterAmount:" + str(afterAmount) + ", beforeAmount:" + str(beforeAmount)
        self.assert_compare_same(beforeAmount, afterAmount)

        # delegator4 不再有分红
        result = self.okcli.query_rewards(self.config["delegators"][3][1], self.config["vaadmin16"])
        assert result == -1, result
        self.okcli.query_total_rewards_gt_precision(self.config["delegators"][3][1], self.config["vals"][2][3], 0, self.PRECISION)
        beforeAmount = self.okcli.query_account(self.config["withdrawaddress"])
        self.okcli.withdraw_all_rewards(self.config["delegators"][3][1])
        self.okcli.wait_ledger_than(2)
        afterAmount = self.okcli.query_account(self.config["withdrawaddress"])
        self.assert_compare_same(beforeAmount, afterAmount)
        diff = self.format_decimal_precision(afterAmount, self.PRECISION + 1) - (self.format_decimal_precision(beforeAmount, self.PRECISION + 1)) 
        assert diff <= 0, str(diff)

        # 666666
        # 再次申请验证节点
        ledger = self.okcli.get_ledger_seq()
        assert self.okcli.create_validator(self.config["vaAddadmin16"]) == -1
        assert self.okcli.edit_validator("zzzzzzzz", self.config["vaAddadmin16"]) != -1
        assert self.okcli.edit_validator_rate("0.5", self.config["vaAddadmin16"]) == -1
        result = self.okcli.query_commission(self.config["vaadmin16"])
        logging.info("query_commission:" + result)
        result = self.okcli.query_outstanding(self.config["vaadmin16"], ledger)
        logging.info("query_outstanding:" + result)
        result = self.okcli.query_validator(self.config["vaadmin16"])
        assert result["jailed"] == True, result

        # 质押人取出后，不再有分红
        self.okcli.wait_ledger_than(20)
        self.okcli.query_total_rewards_gt_precision(self.config["delegators"][4][1], self.config["vals"][2][3], 0, self.PRECISION)
        result = self.okcli.query_validator(self.config["vaadmin16"])
        assert result["jailed"] == True, result
        result = self.okcli.query_rewards(self.config["delegators"][4][1], self.config["vaadmin16"])
        assert len(result) > 0, result
        assert self.okcli.withdraw_rewards(self.config["vaadmin16"], self.config["delegators"][4][1]) != -1
        self.okcli.wait_ledger_than(5)
        result = self.okcli.query_rewards(self.config["delegators"][4][1], self.config["vaadmin16"])
        assert len(result) == 0, result

        # add shares会进行分红
        self.okcli.set_withdraw_addr(self.config["withdrawaddress"], self.config["proxys"][0][1])
        before = self.okcli.query_account(self.config["withdrawaddress"])
        self.okcli.query_total_rewards_gt_precision(self.config["proxys"][0][1], self.config["vals"][0][3], 0, self.PRECISION)
        assert self.okcli.add_shares(self.vals3, self.config["proxys"][0][1]) != -1
        after = self.okcli.query_account(self.config["withdrawaddress"])
        diff = self.format_decimal_precision(after, self.PRECISION + 1) - (self.format_decimal_precision(before, self.PRECISION + 1)) 
        assert diff > self.PRECISION_REWARDS, str(diff)

        # 查询抽成正常
        ledger = self.okcli.get_ledger_seq()
        result = self.okcli.query_commission(self.config["vals"][0][3], ledger)
        result = self.okcli.query_commission(self.config["vals"][1][3], ledger)
        result = self.okcli.query_commission(self.config["vals"][2][3], ledger)
        result = self.okcli.query_commission(self.config["vals"][3][3], ledger)
        result = self.okcli.query_commission(self.config["vaadmin16"], ledger)

        result = self.okcli.query_outstanding(self.config["vals"][0][3], ledger)
        result = self.okcli.query_outstanding(self.config["vals"][1][3], ledger)
        result = self.okcli.query_outstanding(self.config["vals"][2][3], ledger)
        result = self.okcli.query_outstanding(self.config["vals"][3][3], ledger)
        result = self.okcli.query_outstanding(self.config["vaadmin16"], ledger)

        result = self.okcli.query_rewards(self.config["proxys"][0][1], "")
        result = self.okcli.query_rewards(self.config["proxys"][1][1], "")
        result = self.okcli.query_rewards(self.config["proxys"][2][1], "")
        result = self.okcli.query_rewards(self.config["proxys"][3][1], "")
        result = self.okcli.query_rewards(self.config["proxys"][4][1], "")

        result = self.okcli.query_rewards(self.config["delegators"][0][1], "")
        result = self.okcli.query_rewards(self.config["delegators"][1][1], "")
        result = self.okcli.query_rewards(self.config["delegators"][2][1], "")
        result = self.okcli.query_rewards(self.config["delegators"][3][1], "")
        result = self.okcli.query_rewards(self.config["delegators"][4][1], "")

        # 取出分红分红正常
        assert self.okcli.withdraw_all_rewards(self.config["delegators"][0][1]) != -1
        assert self.okcli.withdraw_all_rewards(self.config["delegators"][1][1]) != -1
        assert self.okcli.withdraw_all_rewards(self.config["delegators"][2][1]) == -1 # 无法取出分红，因为已经取出押金
        assert self.okcli.withdraw_all_rewards(self.config["delegators"][3][1]) == -1 # 无法取出分红，因为已经取出押金
        assert self.okcli.withdraw_all_rewards(self.config["delegators"][4][1]) != -1

        assert self.okcli.withdraw_rewards(self.config["vals"][0][3], self.config["proxys"][0][1]) != -1
        assert self.okcli.withdraw_rewards(self.config["vals"][0][3], self.config["proxys"][1][1]) != -1
        assert self.okcli.withdraw_rewards(self.config["vals"][0][3], self.config["proxys"][2][1]) != -1
        assert self.okcli.withdraw_rewards(self.config["vals"][0][3], self.config["proxys"][3][1]) != -1
        assert self.okcli.withdraw_rewards(self.config["vals"][0][3], self.config["proxys"][4][1]) != -1
        assert self.okcli.withdraw_rewards(self.config["vaadmin16"], self.config["proxys"][0][1]) == -1
        assert self.okcli.withdraw_rewards(self.config["vaadmin16"], self.config["proxys"][1][1])== -1
        assert self.okcli.withdraw_rewards(self.config["vaadmin16"], self.config["proxys"][2][1])== -1
        assert self.okcli.withdraw_rewards(self.config["vaadmin16"], self.config["proxys"][3][1]) != -1
        assert self.okcli.withdraw_rewards(self.config["vaadmin16"], self.config["proxys"][4][1]) != -1

        result = self.okcli.query_distr_params()
        assert result["distribution_type"] == 1, result

        self.okcli.query_commission(self.config["vals"][0][3])
        self.okcli.query_commission(self.config["vals"][1][3])
        self.okcli.query_commission(self.config["vals"][2][3])
        self.okcli.query_commission(self.config["vals"][3][3])

        self.okcli.withdraw_commission(self.config["vals"][0][3], "va1")
        self.okcli.withdraw_commission(self.config["vals"][1][3], "va1")
        self.okcli.withdraw_commission(self.config["vals"][2][3], "va1")
        self.okcli.withdraw_commission(self.config["vals"][3][3], "va1")

        logging.info("------------------------change_to_on_chain end--------------------------------")

    def enabled_withdraw_reward_before(self):
        logging.info("------------------------enabled_withdraw_reward_before start--------------------------------")
        if self.single_debug:
            self.okcli.run_all_node(self.config["nodeCount"], self.config["ledgerTime"], self.config["nodeCount"], self.config["nodes"])
            time.sleep(5)
        
        logging.info("------------------------enabled_withdraw_reward_before end--------------------------------")

    def enabled_withdraw_reward(self):
        logging.info("------------------------enabled_withdraw_reward start--------------------------------")

        # 普通人无法发起提案
        assert self.okcli.submit_withdraw_reward_disabled(self.config["delegators"][0][1]) == -1

        # 发起投票提案，禁止链上提取分红
        proposal_num = self.okcli.submit_withdraw_reward_disabled(self.config["vals"][0][1])
        self.okcli.query_proposal(proposal_num)
        
        for n in self.config["delegators"]:
            self.okcli.vote(n[1], proposal_num)

        for n in self.config["proxys"]:
            self.okcli.vote(n[1], proposal_num)

        for v in self.config["vals"]:
            self.okcli.vote(v[1], proposal_num)
        self.okcli.query_proposal(proposal_num)

        self.okcli.wait_ledger_than(2)
        result = self.okcli.query_distr_params()
        assert result["withdraw_reward_enabled"] == False, result

        # 禁止分红相关操作
        assert self.okcli.withdraw_all_rewards(self.config["delegators"][0][1]) == -1

        # 禁止代理相关操作
        assert self.okcli.deposit(self.config["depoistCoin"], self.config["delegators"][5][1]) == -1
        assert self.okcli.add_shares(self.vals4, self.config["delegators"][5][1]) == -1  
        self.okcli.wait_ledger_than(2)
        assert self.okcli.add_shares(self.vals4, self.config["delegators"][5][1]) == -1 
        assert self.okcli.deposit(self.config["depoistCoin"], self.config["proxydelegators"][5][1]) == -1
        assert self.okcli.deposit(self.config["depoistCoin"], self.config["proxys"][5][1]) == -1
        assert self.okcli.add_shares(self.vals4, self.config["proxys"][5][1]) == -1
        assert self.okcli.add_shares(self.vals4, self.config["proxys"][5][1]) == -1 
        assert self.okcli.proxy_reg(self.config["proxys"][5][1]) == -1
        assert self.okcli.proxy_bind(self.config["proxys"][5][1], self.config["proxydelegators"][5][1]) == -1

        # 禁止代理相关操作
        assert self.okcli.query_tx(self.okcli.withdraw_rewards(self.config["vals"][0][3], self.config["proxys"][0][1], False)) == 167826
        assert self.okcli.query_tx(self.okcli.withdraw_all_rewards(self.config["delegators"][0][1], False)) == 167826
        assert self.okcli.query_tx(self.okcli.add_shares(self.vals4, self.config["delegators"][5][1], False)) == 167049
        assert self.okcli.query_tx(self.okcli.add_shares(self.vals4, self.config["proxys"][5][1], False)) == 167049
        assert self.okcli.query_tx(self.okcli.proxy_bind(self.config["proxys"][4][1], self.config["proxydelegators"][5][1], False)) == 167049

        # 普通人无法发起提案
        assert self.okcli.submit_withdraw_reward_enabled(self.config["delegators"][0][1]) == -1
        assert self.okcli.submit_withdraw_reward_enabled(self.config["delegators"][0][1], False) == 167828

        # 发起投票提案，启用链上提取分红
        proposal_num = self.okcli.submit_withdraw_reward_enabled(self.config["vals"][0][1])
        self.okcli.query_proposal(proposal_num)
        for n in self.config["delegators"]:
            self.okcli.vote(n[1], proposal_num)

        for n in self.config["proxys"]:
            self.okcli.vote(n[1], proposal_num)

        for v in self.config["vals"]:
            self.okcli.vote(v[1], proposal_num)

        self.okcli.query_proposal(proposal_num)

        self.okcli.wait_ledger_than(2)
        result = self.okcli.query_distr_params()
        assert result["withdraw_reward_enabled"] == True, result

        # 普通转账成功
        assert self.okcli.transfer(self.config["captain"], self.config["delegators"][1][1], self.config["initCoin"]) != -1

        # 注册代理成功
        assert self.okcli.deposit(self.config["depoistCoin"], self.config["delegators"][5][1]) != -1 
        assert self.okcli.add_shares(self.vals4, self.config["delegators"][5][1]) != -1  
        assert self.okcli.deposit(self.config["depoistCoin"], self.config["proxydelegators"][5][1]) != -1
        assert self.okcli.deposit(self.config["depoistCoin"], self.config["proxys"][5][1]) != -1
        assert self.okcli.add_shares(self.vals4, self.config["proxys"][5][1]) != -1
        assert self.okcli.proxy_reg(self.config["proxys"][5][1]) != -1

        # bind也会进行分红
        self.okcli.set_withdraw_addr(self.config["withdrawaddress"], self.config["proxys"][5][1])
        before = self.okcli.query_account(self.config["withdrawaddress"])
        self.okcli.query_total_rewards_gt_precision(self.config["proxys"][5][1], self.config["vals"][0][3], 0, self.PRECISION)
        assert self.okcli.proxy_bind(self.config["proxys"][5][1], self.config["proxydelegators"][5][1]) != -1
        after = self.okcli.query_account(self.config["withdrawaddress"])
        addValue = self.format_decimal_precision(after, self.PRECISION + 1) - self.format_decimal_precision(before, self.PRECISION + 1)
        assert addValue >= self.PRECISION_REWARDS, str(addValue)

        # proxy5 取出va2的分红
        self.okcli.query_total_rewards_gt_precision(self.config["proxys"][5][1], self.config["vals"][1][3], 0, self.PRECISION)
        rewards = self.okcli.query_rewards(self.config["proxys"][5][1], self.config["vals"][1][3])[0]["amount"]
        beforeAmount = self.okcli.query_account(self.config["withdrawaddress"])
        assert self.okcli.withdraw_rewards(self.config["vals"][1][3], self.config["proxys"][5][1]) != -1
        afterAmount = self.okcli.query_account(self.config["withdrawaddress"])
        logging.info("afterAmount:" + str(afterAmount) + ", beforeAmount:" + str(beforeAmount) + ", rewards:" + str(rewards))
        assert float(rewards) > self.PRECISION_REWARDS, rewards
        diff = self.format_decimal_precision(afterAmount, self.PRECISION + 1) - (self.format_decimal_precision(beforeAmount, self.PRECISION + 1)) 
        assert diff >= self.PRECISION_REWARDS, str(diff)

        # proxy5 unbind 分红
        self.okcli.query_total_rewards_gt_precision(self.config["proxys"][5][1], self.config["vals"][1][3], 0, self.PRECISION)
        rewards = self.okcli.query_rewards(self.config["proxys"][5][1], self.config["vals"][1][3])[0]["amount"]
        beforeAmount = self.okcli.query_account(self.config["withdrawaddress"])
        assert self.okcli.proxy_unbind(self.config["proxydelegators"][5][1]) != -1
        afterAmount = self.okcli.query_account(self.config["withdrawaddress"])
        logging.info("afterAmount:" + str(afterAmount) + ", beforeAmount:" + str(beforeAmount) + ", rewards:" + str(rewards))
        assert float(rewards) > self.PRECISION_REWARDS, rewards
        diff = self.format_decimal_precision(afterAmount, self.PRECISION + 1) - (self.format_decimal_precision(beforeAmount, self.PRECISION + 1)) 
        assert diff >= self.PRECISION_REWARDS, str(diff)
        
        logging.info("------------------------enabled_withdraw_reward end--------------------------------")

    def reward_truncate_before(self):
        logging.info("------------------------reward_truncate_before start--------------------------------")
        if self.single_debug:
            self.okcli.run_all_node(self.config["nodeCount"], self.config["ledgerTime"], self.config["nodeCount"], self.config["nodes"])
            time.sleep(5)
        
        logging.info("------------------------reward_truncate_before end--------------------------------")

    def reward_truncate(self):
        logging.info("------------------------reward_truncate start--------------------------------")

        # 普通人无法发起提案
        assert self.okcli.submit_reward_truncate_2(self.config["delegators"][0][1]) == -1

        # 发起分红截断提案，精度为 4
        self.set_reword_persion(4)
        
        # 先取出分红
        assert self.okcli.withdraw_rewards(self.config["vals"][1][3], self.config["proxys"][5][1]) != -1

        # bind也会进行分红
        self.okcli.set_withdraw_addr(self.config["withdrawaddress"], self.config["proxys"][5][1])
        before = self.okcli.query_account(self.config["withdrawaddress"])
        self.okcli.query_total_rewards_gt_precision(self.config["proxys"][5][1], self.config["vals"][0][3], 0, self.PRECISION)
        result = self.okcli.query_rewards(self.config["proxys"][5][1], "")
        rewards = result["total"][0]["amount"]
        assert self.okcli.proxy_bind(self.config["proxys"][5][1], self.config["proxydelegators"][5][1]) != -1
        after = self.okcli.query_account(self.config["withdrawaddress"])
        assert float(rewards) > self.PRECISION_REWARDS, rewards
        diff = self.format_decimal_precision(after, self.PRECISION + 1) - (self.format_decimal_precision(before, self.PRECISION + 1)) 
        assert diff > self.PRECISION_REWARDS_DIFF, str(diff)

        # proxy5 取出va2的分红
        self.okcli.query_total_rewards_gt_precision(self.config["proxys"][5][1], self.config["vals"][1][3], 0, self.PRECISION)
        rewards = self.okcli.query_rewards(self.config["proxys"][5][1], self.config["vals"][1][3])[0]["amount"]
        beforeAmount = self.okcli.query_account(self.config["withdrawaddress"])
        assert self.okcli.withdraw_rewards(self.config["vals"][1][3], self.config["proxys"][5][1]) != -1
        afterAmount = self.okcli.query_account(self.config["withdrawaddress"])
        logging.info("afterAmount:" + str(afterAmount) + ", beforeAmount:" + str(beforeAmount) + ", rewards:" + str(rewards))
        assert float(rewards) > self.PRECISION_REWARDS, rewards
        diff = self.format_decimal_precision(afterAmount, self.PRECISION + 1) - (self.format_decimal_precision(beforeAmount, self.PRECISION + 1)) 
        assert diff > self.PRECISION_REWARDS, str(diff)

        # proxy5 unbind 分红
        self.okcli.query_total_rewards_gt_precision(self.config["proxys"][5][1], self.config["vals"][1][3], 0, self.PRECISION)
        rewards = self.okcli.query_rewards(self.config["proxys"][5][1], self.config["vals"][1][3])[0]["amount"]
        beforeAmount = self.okcli.query_account(self.config["withdrawaddress"])
        assert self.okcli.proxy_unbind(self.config["proxydelegators"][5][1]) != -1
        afterAmount = self.okcli.query_account(self.config["withdrawaddress"])
        logging.info("afterAmount:" + str(afterAmount) + ", beforeAmount:" + str(beforeAmount) + ", rewards:" + str(rewards))
        addValue = self.format_decimal_precision(afterAmount, self.PRECISION) - self.format_decimal_precision(beforeAmount, self.PRECISION)

        # 发起分红截断提案，精度为 0
        self.set_reword_persion(0)

        # 先取出分红
        assert self.okcli.withdraw_rewards(self.config["vals"][1][3], self.config["proxys"][5][1]) != -1

        # bind也会进行分红
        self.okcli.set_withdraw_addr(self.config["withdrawaddress"], self.config["proxys"][5][1])
        rewards = self.okcli.query_rewards(self.config["proxys"][5][1], self.config["vals"][1][3])[0]["amount"]
        before = self.okcli.query_account(self.config["withdrawaddress"])
        self.okcli.query_total_rewards_gt_precision(self.config["proxys"][5][1], self.config["vals"][0][3], 0, self.PRECISION)
        assert self.okcli.proxy_bind(self.config["proxys"][5][1], self.config["proxydelegators"][5][1]) != -1
        after = self.okcli.query_account(self.config["withdrawaddress"])
        assert float(rewards) > self.PRECISION_REWARDS, rewards
        diff = self.format_decimal_precision(after, self.PRECISION + 1) - (self.format_decimal_precision(before, self.PRECISION + 1)) 
        assert diff > self.PRECISION_REWARDS, str(diff)
        
        # # proxy5 取出va2的分红
        self.okcli.query_rewards(self.config["proxys"][5][1], "")
        self.okcli.query_total_rewards_gt_precision(self.config["proxys"][5][1], self.config["vals"][1][3], 0, self.PRECISION)
        rewards = self.okcli.query_rewards(self.config["proxys"][5][1], self.config["vals"][1][3])[0]["amount"]
        beforeAmount = self.okcli.query_account(self.config["withdrawaddress"])
        assert self.okcli.withdraw_rewards(self.config["vals"][1][3], self.config["proxys"][5][1]) != -1
        afterAmount = self.okcli.query_account(self.config["withdrawaddress"])
        logging.info("afterAmount:" + str(afterAmount) + ", beforeAmount:" + str(beforeAmount) + ", rewards:" + str(rewards))
        assert float(rewards) > self.PRECISION_REWARDS, rewards
        diff = self.format_decimal_precision(afterAmount, self.PRECISION + 1) - (self.format_decimal_precision(beforeAmount, self.PRECISION + 1)) 
        assert diff > self.PRECISION_REWARDS, str(diff)
        self.okcli.query_rewards(self.config["proxys"][5][1], "")

        # # proxy5 unbind 分红
        self.okcli.query_total_rewards_gt_precision(self.config["proxys"][5][1], self.config["vals"][2][3], 0, self.PRECISION)
        rewards = self.okcli.query_rewards(self.config["proxys"][5][1], self.config["vals"][1][3])[0]["amount"]
        beforeAmount = self.okcli.query_account(self.config["withdrawaddress"])
        assert self.okcli.proxy_unbind(self.config["proxydelegators"][5][1]) != -1
        afterAmount = self.okcli.query_account(self.config["withdrawaddress"])
        logging.info("afterAmount:" + str(afterAmount) + ", beforeAmount:" + str(beforeAmount) + ", rewards:" + str(rewards))
        assert float(rewards) > self.PRECISION_REWARDS, rewards
        diff = self.format_decimal_precision(afterAmount, self.PRECISION + 1) - (self.format_decimal_precision(beforeAmount, self.PRECISION + 1)) 
        assert diff > self.PRECISION_REWARDS, str(diff)

        ## 小于1无法取出
        # 先取出分红
        assert self.okcli.withdraw_rewards(self.config["vals"][1][3], self.config["proxys"][5][1]) != -1
        self.okcli.query_total_rewards_gt_precision(self.config["proxys"][5][1], self.config["vals"][1][3], 0, self.PRECISION)
        rewards = self.okcli.query_rewards(self.config["proxys"][5][1], self.config["vals"][1][3])[0]["amount"]
        beforeAmount = self.okcli.query_account(self.config["withdrawaddress"])
        assert self.okcli.withdraw_rewards(self.config["vals"][1][3], self.config["proxys"][5][1]) != -1
        afterAmount = self.okcli.query_account(self.config["withdrawaddress"])
        logging.info("afterAmount:" + str(afterAmount) + ", beforeAmount:" + str(beforeAmount) + ", rewards:" + str(rewards))
        addValue = self.format_decimal_precision(afterAmount, self.PRECISION) - self.format_decimal_precision(beforeAmount, self.PRECISION)
        assert addValue <= 0, str(addValue)
        
        logging.info("------------------------reward_truncate end--------------------------------")

    def extension_before(self):
        logging.info("------------------------extension_before start--------------------------------")
        if self.single_debug:
            self.okcli.run_all_node(self.config["nodeCount"], self.config["ledgerTime"], self.config["nodeCount"], self.config["nodes"])
            time.sleep(5)
        
        logging.info("------------------------extension_before end--------------------------------")

    def extension(self):
        logging.info("------------------------extension start--------------------------------")

        proposal_num = self.okcli.submit_community_pool_spend(self.config["delegators"][0][1])
        assert int(proposal_num) > 0

        # 使用deledator取出代理分红
        dictDV = {}
        for p in self.config["proxys"]:
            # 设置代理人的取款地址
            self.okcli.set_withdraw_addr(self.config["withdrawaddress"], p[1])
            for v in self.config["vals"]:
                result = self.okcli.query_rewards(p[1], v[3])
                if result != -1:
                    dictDV[p[1]] = v[3]

        # self.exit()
        count = 0
        while True:
            logging.info("total:" + str(len(dictDV)))
            time.sleep(1)
            for k in dictDV:
                result = self.okcli.query_rewards(k, dictDV[k])
                if len(result) <= 0:
                    continue
                if self.format_decimal(result[0]["amount"]) < 1:
                    continue

                before = self.okcli.query_account(self.config["withdrawaddress"])
                hash = self.okcli.withdraw_rewards(dictDV[k], k)
                after = self.okcli.query_account(self.config["withdrawaddress"])

                seq = self.okcli.get_ledger_seq_from_hash(hash)
                result = self.okcli.query_rewards(k, dictDV[k], seq-1)
                reward = 0
                if len(result) > 0:
                    reward = self.format_decimal(result[0]["amount"])

                addValue = self.format_decimal(after) - self.format_decimal(before)
                logging.info("d:" + k + ", v:" + dictDV[k] + ", before:" + str(before) + ", after:" + str(after) + ", reward:" + str(reward))
                # assert addValue >= 1
                self.assert_compare_near(addValue, reward)

            count += 1
            if count >= 100:
                break

        # 所有节点高度一致
        splitArray = self.config["rpc"].split(":")
        url = splitArray[0] + ":" + splitArray[1]
        
        ledger = int(self.okcli.get_ledger_seq())
        for i in range(self.config["nodeCount"]):
            port = 26657 + i * 100
            rpc = url + ":" + str(port)
            other_ledger = int(self.okcli.get_ledger_seq(rpc))
            assert (other_ledger - ledger) <= 5

        logging.info("------------------------extension end--------------------------------")

    def exit(self, stop = True):
        #if stop:
            #case.okcli.kill_all_process()
        logging.info("Please use arg eg:  auto")
        sys.exit()
    def set_reword_persion(self, persion):
        # 发起分红截断提案，精度为 persion
        proposal_num = self.okcli.submit_reward_truncate(self.config["vals"][0][1], persion)
        if persion == 0:
            self.PRECISION = 0
            self.PRECISION_REWARDS = 1
            self.PRECISION_REWARDS_DIFF = 0.9
        elif persion == 2:
            self.PRECISION = 2
            self.PRECISION_REWARDS = 0.01
            self.PRECISION_REWARDS_DIFF = 0.009
        elif persion == 4:
            self.PRECISION = 4
            self.PRECISION_REWARDS = 0.0001
            self.PRECISION_REWARDS_DIFF = 0.00009
        elif persion == 8:
            self.PRECISION = 8
            self.PRECISION_REWARDS = 0.00000001
            self.PRECISION_REWARDS_DIFF = 0.000000009
        
        self.okcli.query_proposal(proposal_num)
        
        for n in self.config["delegators"]:
            self.okcli.vote(n[1], proposal_num)

        for n in self.config["proxys"]:
            self.okcli.vote(n[1], proposal_num)

        for v in self.config["vals"]:
            self.okcli.vote(v[1], proposal_num)
        self.okcli.query_proposal(proposal_num)

        self.okcli.wait_ledger_than(2)
        result = self.okcli.query_distr_params()
        assert result["reward_truncate_precision"] == str(persion), result

if __name__ == '__main__':
    pybase = pybase.Pybase()
    strlist = os.path.basename(__file__).split('.') 
    file = open('config/' + strlist[0] + '.json', 'r', encoding='UTF-8')
    moduleConfig = json.loads(file.read())
    file.close()
    case = CaseDistrProposal(moduleConfig)

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
    
    elif opt == "init_staking_before":
        case.init_staking_before()
    elif opt == "init_staking":
        case.init_staking()
    
    elif opt == "upgrate_bin_staking_step1_before":
        case.upgrate_bin_staking_step1_before()
    elif opt == "upgrate_bin_staking_step1":
        case.upgrate_bin_staking_step1()

    elif opt == "upgrate_bin_staking_step2_before":
        case.upgrate_bin_staking_step2_before()
    elif opt == "upgrate_bin_staking_step2":
        case.upgrate_bin_staking_step2()

    elif opt == "upgrate_ledger_staking_before":
        case.upgrate_ledger_staking_before()
    elif opt == "upgrate_ledger_staking":
        case.upgrate_ledger_staking()

    elif opt == "after_distr_proposal_before":
        case.after_distr_proposal_before()
    elif opt == "after_distr_proposal":
        case.after_distr_proposal()

    elif opt == "change_to_off_chain_before":
        case.change_to_off_chain_before()
    elif opt == "change_to_off_chain":
        case.change_to_off_chain()

    elif opt == "change_to_on_chain_before":
        case.change_to_on_chain_before()
    elif opt == "change_to_on_chain":
        case.change_to_on_chain()

    elif opt == "enabled_withdraw_reward_before":
        case.enabled_withdraw_reward_before()
    elif opt == "enabled_withdraw_reward":
        case.enabled_withdraw_reward()

    elif opt == "reward_truncate_before":
        case.reward_truncate_before()
    elif opt == "reward_truncate":
        case.reward_truncate()

    elif opt == "extension_before":
        case.extension_before()
    elif opt == "extension":
        case.extension()

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
