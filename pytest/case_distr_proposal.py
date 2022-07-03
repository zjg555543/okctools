# /usr/bin/env python3
# --coding:utf-8 --
import json
import logging
from os import system
from pickletools import long1
import sys
import time
import pybase
import rpc

class CaseDistrProposal:
    def __init__(self, configObj):
        self.config = configObj
        self.okcli = rpc.OKCli("exchaind", "exchaincli")
        self.vals1 = self.config["va1"]
        self.vals2 = self.config["va1"] + "," + self.config["va2"]
        self.vals3 = self.config["va1"] + "," + self.config["va2"] + "," + self.config["va3"]
        self.valsall = self.config["va1"] + "," + self.config["va2"] + "," + self.config["va3"] + "," + self.config["va4"] + "," + self.config["vaadmin16"]
        self.single_debug = False
        return

    def format_decimal(self, num):
        str_num = str(num)
        if "." in str_num:
            a, b = str(str_num).split('.')
            return int(a)
        else:
            return int(str_num)

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

    def test(self):
        # result = self.okcli.query_staking_validators()
        # for value in result:
        #     assert self.format_decimal(value["delegator_shares"]) == "1", value
        # result = self.okcli.query_account(self.config["delegator4"])
        # logging.info(result)
        # assert self.format_decimal(result) == self.config["initCoin"], self.format_decimal(result)

        # def do():
        #     logging.info("1111")
        # do()

        # result = self.okcli.query_commission(self.config["va1"])
        # logging.info(result)
        # assert self.format_decimal(result) > 0, result

        # result = self.okcli.query_outstanding(self.config["va1"])
        # assert result == -1, result

        # result = self.okcli.query_shares(self.config["delegator1"])
        # assert self.format_decimal(result["tokens"]) == 0, result
        # assert self.format_decimal(result["shares"]) == 0, result

        # result = self.okcli.query_staking_validators()
        # result = self.okcli.query_outstanding(self.config["va4"])
        # assert result == -1, result

        # result = self.okcli.query_rewards(self.config["delegator1"], "")
        # assert result == -1, result

        # # 查询分红参数 distribution_type 为0
        # result = self.okcli.query_distr_params()
        # assert result["distribution_type"] == 0, result

        # 支持 edit-validator-commission-rate 操作
        # result = self.okcli.edit_validator("0.1", "va4")
        # assert result != -1, result

        # # 不支持的操作  withdraw-all-rewards、withdraw-rewards outstanding-rewards
        # result = self.okcli.withdraw_all_rewards(self.config["delegator1"])
        # assert result == -1, result
        # result = self.okcli.withdraw_rewards(self.config["va1"], self.config["delegator1"])
        # assert result == -1, result
        # result = self.okcli.query_outstanding(self.config["va1"])
        # assert result == -1, result

        # result = self.okcli.query_commission(self.config["va1"])
        # assert self.format_decimal(result) > 1, result
        # result = self.okcli.query_commission(self.config["va2"])
        # assert self.format_decimal(result) > 1, result
        # result = self.okcli.query_commission(self.config["va3"])
        # assert self.format_decimal(result) > 1, result
        # result = self.okcli.query_commission(self.config["va4"])
        # assert self.format_decimal(result) > 1, result
        # logging.info(result)

        # commission_va2 = self.okcli.query_commission(self.config["va2"])
        # outstanding_va2 = self.okcli.query_outstanding(self.config["va2"])
        # logging.info("commission_va2:" + commission_va2 + ", outstanding_va2:" + outstanding_va2)
        # assert self.format_decimal(commission_va2) == self.format_decimal(outstanding_va2)

        # # proxy1 查询分红为空，因为v1抽成比例为100%
        # result = self.okcli.query_rewards(self.config["proxy1"], "")
        # assert len(result["total"]) == 0, result

        # # delegator1  查询分红为空，因为v1抽成比例为100%
        # result = self.okcli.query_rewards(self.config["delegator1"], "")
        # assert len(result["total"]) == 0, result

        
        logging.info(self.format_decimal("111.1"))
        logging.info(self.format_decimal(111.1))
        logging.info(self.assert_compare_near(1, 2))
        logging.info(self.assert_compare_near("1.1", 2))

        return
        

        

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
        result = self.okcli.run_cmd("cd /Users/oker/workspace/exchain-raw/dev/testnet/;./run4v1r.sh")
        time.sleep(5)
        result = self.okcli.wait_ledger(1)
        result = self.okcli.kill_process("exchaind")

        # 迁移命令行和迁移文件夹，重新启动
        result = self.okcli.run_cmd("rm -rf /Users/oker/workspace/nodes/*; cp -rf /Users/oker/workspace/exchain-raw/dev/testnet/cache/* /Users/oker/workspace/nodes/")
        result = self.okcli.run_all_node()
        result = self.okcli.version("exchaind") 
        assert result == "v1.6.0", result

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
        self.okcli.recover("proxydelegator1", self.config["mnemonicproxydelegator1"])
        self.okcli.recover("proxydelegator2", self.config["mnemonicproxydelegator2"])
        self.okcli.recover("proxydelegator3", self.config["mnemonicproxydelegator3"])
        self.okcli.recover("proxydelegator4", self.config["mnemonicproxydelegator4"])
        self.okcli.recover("proxydelegator5", self.config["mnemonicproxydelegator5"])
        self.okcli.recover("proxydelegator6", self.config["mnemonicproxydelegator6"])

        self.okcli.recover_val("va1", self.config["mnemonicva1"])
        self.okcli.recover_val("va2", self.config["mnemonicva2"])
        self.okcli.recover_val("va3", self.config["mnemonicva3"])
        self.okcli.recover_val("va4", self.config["mnemonicva4"])

        self.okcli.transfer(self.config["captain"], self.config["delegator1"], self.config["initCoin"])
        self.okcli.transfer(self.config["captain"], self.config["delegator2"], self.config["initCoin"])
        self.okcli.transfer(self.config["captain"], self.config["delegator3"], self.config["initCoin"])
        self.okcli.transfer(self.config["captain"], self.config["delegator4"], self.config["initCoin"])
        self.okcli.transfer(self.config["captain"], self.config["delegator5"], self.config["initCoin"])
        self.okcli.transfer(self.config["captain"], self.config["delegator6"], self.config["initCoin"])
        self.okcli.transfer(self.config["captain"], self.config["delegator7"], self.config["initCoin"])
        self.okcli.transfer(self.config["captain"], self.config["delegator8"], self.config["initCoin"])
        self.okcli.transfer(self.config["captain"], self.config["delegator9"], self.config["initCoin"])
        self.okcli.transfer(self.config["captain"], self.config["delegator10"], self.config["initCoin"])
        self.okcli.transfer(self.config["captain"], self.config["proxy1"], self.config["initCoin"])
        self.okcli.transfer(self.config["captain"], self.config["proxy2"], self.config["initCoin"])
        self.okcli.transfer(self.config["captain"], self.config["proxy3"], self.config["initCoin"])
        self.okcli.transfer(self.config["captain"], self.config["proxy4"], self.config["initCoin"])
        self.okcli.transfer(self.config["captain"], self.config["proxy5"], self.config["initCoin"])
        self.okcli.transfer(self.config["captain"], self.config["proxy6"], self.config["initCoin"])
        self.okcli.transfer(self.config["captain"], self.config["proxydelegator1"], self.config["initCoin"])
        self.okcli.transfer(self.config["captain"], self.config["proxydelegator2"], self.config["initCoin"])
        self.okcli.transfer(self.config["captain"], self.config["proxydelegator3"], self.config["initCoin"])
        self.okcli.transfer(self.config["captain"], self.config["proxydelegator4"], self.config["initCoin"])
        self.okcli.transfer(self.config["captain"], self.config["proxydelegator5"], self.config["initCoin"])
        self.okcli.transfer(self.config["captain"], self.config["proxydelegator6"], self.config["initCoin"])
        
        
        def do(account):
            result = self.okcli.query_account(account)
            assert self.format_decimal(result) == self.config["initCoin"], result
        do(self.config["delegator1"])
        do(self.config["delegator2"])
        do(self.config["delegator3"])
        do(self.config["delegator4"])
        do(self.config["delegator5"])
        do(self.config["delegator6"])
        do(self.config["delegator7"])
        do(self.config["delegator8"])
        do(self.config["delegator9"])
        do(self.config["delegator10"])

        do(self.config["proxy1"])
        do(self.config["proxy2"])
        do(self.config["proxy3"])
        do(self.config["proxy4"])
        do(self.config["proxy5"])
        do(self.config["proxy6"])

        do(self.config["proxydelegator1"])
        do(self.config["proxydelegator2"])
        do(self.config["proxydelegator3"])
        do(self.config["proxydelegator4"])
        do(self.config["proxydelegator5"])
        do(self.config["proxydelegator6"])

        logging.info("------------------------initChain end--------------------------------")
        return
    def init_staking(self):
        if self.single_debug:
            result = self.okcli.kill_process("exchaind")
            result = self.okcli.run_all_node()
            time.sleep(5)
            result = self.okcli.version("exchaind") 
            assert result == "v1.6.0", result

        logging.info("------------------------initStaking start--------------------------------")
        result = self.okcli.query_staking_validators()
        assert len(result) == 4, result
        for value in result:
            assert self.format_decimal(value["delegator_shares"]) == 1, value
        # 质押delegator1 10000 okt
        self.okcli.deposit(self.config["depoistCoin"], self.config["delegator1"])
        self.okcli.add_shares(self.vals1, self.config["delegator1"])
        result = self.okcli.query_shares(self.config["delegator1"])
        assert self.format_decimal(result["tokens"]) == self.config["depoistCoin"], result
        assert self.format_decimal(result["shares"]) > 0, result

        # 质押 proxydelegator1 10000 okt
        self.okcli.deposit(self.config["depoistCoin"], self.config["proxydelegator1"])
        result = self.okcli.query_shares(self.config["proxydelegator1"])
        assert self.format_decimal(result["tokens"]) == self.config["depoistCoin"], result
        assert self.format_decimal(result["shares"]) == 0, result

        # 质押proxy1 10000 okt，注册代理 proxy1, proxydelegator1 绑定 proxy1
        self.okcli.deposit(self.config["depoistCoin"], self.config["proxy1"])
        self.okcli.add_shares(self.vals1, self.config["proxy1"])
        self.okcli.proxy_reg(self.config["proxy1"])
        self.okcli.proxy_bind(self.config["proxy1"], self.config["proxydelegator1"])

        # proxydelegator1 有 tokens，shares 为 0
        resultProxydelegator1 = self.okcli.query_shares(self.config["proxydelegator1"])
        assert self.format_decimal(resultProxydelegator1["tokens"]) == self.config["depoistCoin"], resultProxydelegator1
        assert self.format_decimal(resultProxydelegator1["shares"]) == 0, resultProxydelegator1
        assert resultProxydelegator1["proxy_address"] == self.config["proxy1"], resultProxydelegator1

        # proxy1 的 total_delegated_tokens 等于 proxydelegator1 的 shares
        result = self.okcli.query_shares(self.config["proxy1"])
        assert result["is_proxy"] == True, result
        assert self.format_decimal(result["tokens"]) == self.config["depoistCoin"], result
        assert self.format_decimal(result["total_delegated_tokens"]) == self.format_decimal(resultProxydelegator1["tokens"]), result

        # 验证节点 commission 有值
        result = self.okcli.query_commission(self.config["va1"])
        assert self.format_decimal(result) > 0, result
        result = self.okcli.query_commission(self.config["va2"])
        assert self.format_decimal(result) > 0, result
        result = self.okcli.query_commission(self.config["va3"])
        assert self.format_decimal(result) > 0, result
        result = self.okcli.query_commission(self.config["va4"])
        assert self.format_decimal(result) > 0, result

        logging.info("------------------------initStaking end--------------------------------")

    def upgrate_bin_staking(self):
        if self.single_debug:
            result = self.okcli.kill_process("exchaind")
            result = self.okcli.run_all_node()
            time.sleep(5)

        logging.info("------------------------upgrate_bin_staking start--------------------------------")

        # 编译新的的4个节点，运行
        result = self.okcli.run_cmd("cd /Users/oker/workspace/exchain/dev/testnet/;./run4v1r.sh")
        time.sleep(5)
        result = self.okcli.wait_ledger(1)
        result = self.okcli.kill_process("exchaind")

        result = self.okcli.run_all_node()
        result = self.okcli.version("exchaind") 
        assert result == "v1.6.1", result
        time.sleep(5)
        # 质押delegator2 10000 okt，投票给va1
        result = self.okcli.query_staking_validators()
        result = self.okcli.deposit(self.config["depoistCoin"], self.config["delegator2"])
        result = self.okcli.add_shares(self.vals2, self.config["delegator2"])

        # proxydelegator2 质押 10000okt
        result = self.okcli.deposit(self.config["depoistCoin"], self.config["proxydelegator2"])
        result = self.okcli.query_shares(self.config["proxydelegator2"])
        assert self.format_decimal(result["tokens"]) == self.config["depoistCoin"], result
        assert self.format_decimal(result["shares"]) == 0, result

        # 注册 proxy2， proxydelegator2 绑定 proxy2
        result = self.okcli.deposit(self.config["depoistCoin"], self.config["proxy2"])
        result = self.okcli.add_shares(self.vals2, self.config["proxy2"])
        result = self.okcli.proxy_reg(self.config["proxy2"])
        result = self.okcli.proxy_bind(self.config["proxy2"], self.config["proxydelegator2"])

        # proxydelegator2 有 tokens，shares 为 0
        resultProxydelegator2 = self.okcli.query_shares(self.config["proxydelegator2"])
        assert self.format_decimal(resultProxydelegator2["tokens"]) == self.config["depoistCoin"], resultProxydelegator2
        assert self.format_decimal(resultProxydelegator2["shares"]) == 0, resultProxydelegator2
        assert resultProxydelegator2["proxy_address"] == self.config["proxy2"], resultProxydelegator2

        # proxy2 的 total_delegated_tokens 等于 proxydelegator2 的 shares
        result = self.okcli.query_shares(self.config["proxy2"])
        assert result["is_proxy"] == True, result
        assert self.format_decimal(result["tokens"]) == self.config["depoistCoin"], result
        assert self.format_decimal(result["total_delegated_tokens"]) == self.format_decimal(resultProxydelegator2["tokens"]), result

        logging.info("------------------------upgrate_bin_staking end--------------------------------")

    def upgrate_ledger_staking(self):
        if self.single_debug:
            result = self.okcli.kill_process("exchaind")
            result = self.okcli.run_all_node()
            time.sleep(5)
            result = self.okcli.version("exchaind") 
            assert result == "v1.6.1", result

        logging.info("------------------------upgrate_ledger_staking start--------------------------------")
        # 新的程序启动，区块升级之后，没有投票提案，仍然按照佣金100%提成计算，查询验证节点投票仍然可用，验证节点取款仍然有效
        result = self.okcli.wait_ledger(50)
        result = self.okcli.query_commission(self.config["va1"])
        assert self.format_decimal(result) > 0, result
        result = self.okcli.query_commission(self.config["va2"])
        assert self.format_decimal(result) > 0, result
        result = self.okcli.query_commission(self.config["va3"])
        assert self.format_decimal(result) > 0, result
        result = self.okcli.query_commission(self.config["va4"])
        assert self.format_decimal(result) > 0, result

         # 查询分红参数 distribution_type 为0
        result = self.okcli.query_distr_params()
        assert result["distribution_type"] == 0, result

        # 支持 edit-validator-commission-rate 操作
        result = self.okcli.edit_validator("0.1", "va4")
        assert result != -1, result

        # 不支持的操作  withdraw-all-rewards、withdraw-rewards、outstanding-rewards、query_rewards
        result = self.okcli.withdraw_all_rewards(self.config["delegator1"])
        assert result == -1, result
        result = self.okcli.withdraw_rewards(self.config["va1"], self.config["delegator1"])
        assert result == -1, result
        result = self.okcli.query_outstanding(self.config["va1"])
        assert result == -1, result
        result = self.okcli.query_rewards(self.config["delegator1"], "")
        assert result == -1, result

        # 质押delegator3 10000 okt，投票给va1
        result = self.okcli.deposit(self.config["depoistCoin"], self.config["delegator3"])
        result = self.okcli.add_shares(self.vals3, self.config["delegator3"])

        # proxydelegator3 质押 10000okt
        result = self.okcli.deposit(self.config["depoistCoin"], self.config["proxydelegator3"])
        result = self.okcli.query_shares(self.config["proxydelegator3"])
        assert self.format_decimal(result["tokens"]) == self.config["depoistCoin"], result
        assert self.format_decimal(result["shares"]) == 0, result

        # 注册 proxy3， proxydelegator3 绑定 proxy3
        result = self.okcli.deposit(self.config["depoistCoin"], self.config["proxy3"])
        result = self.okcli.add_shares(self.vals3, self.config["proxy3"])
        result = self.okcli.proxy_reg(self.config["proxy3"])
        result = self.okcli.proxy_bind(self.config["proxy3"], self.config["proxydelegator3"])

        # proxydelegator3 有 tokens，shares 为 0
        resultProxydelegator3 = self.okcli.query_shares(self.config["proxydelegator3"])
        assert self.format_decimal(resultProxydelegator3["tokens"]) == self.config["depoistCoin"], resultProxydelegator3
        assert self.format_decimal(resultProxydelegator3["shares"]) == 0, resultProxydelegator3
        assert resultProxydelegator3["proxy_address"] == self.config["proxy3"], resultProxydelegator3

        # proxy3 的 total_delegated_tokens 等于 proxydelegator3 的 shares
        result = self.okcli.query_shares(self.config["proxy3"])
        assert result["is_proxy"] == True, result
        assert self.format_decimal(result["tokens"]) == self.config["depoistCoin"], result
        assert self.format_decimal(result["total_delegated_tokens"]) == self.format_decimal(resultProxydelegator3["tokens"]), result

        logging.info("------------------------upgrate_ledger_staking end--------------------------------")

    def after_distr_proposal(self):
        if self.single_debug:
            result = self.okcli.kill_process("exchaind")
            result = self.okcli.run_all_node()
            result = self.okcli.version("exchaind") 
            assert result == "v1.6.1", result
            time.sleep(5)
        # 11111
        logging.info("------------------------after_distr_proposal start--------------------------------")
        # 发起投票提案，修改提案，此时分红比例默认为100%，各个接口可以使用，验证节点查询抽成，提取抽成正常；委托人查询分红为0；代理人查询为0，无法提取抽成；
        result = self.okcli.wait_ledger(65)
        result = self.okcli.submit_change_type_proposal_onchain(self.config["delegator1"])
        proposal_num=1
        result = self.okcli.query_proposal(proposal_num)
        result = self.okcli.vote(self.config["delegator1"], proposal_num)
        result = self.okcli.vote(self.config["delegator2"], proposal_num)
        result = self.okcli.vote(self.config["delegator3"], proposal_num)
        result = self.okcli.vote(self.config["proxy1"], proposal_num)
        result = self.okcli.vote(self.config["proxy2"], proposal_num)
        result = self.okcli.vote(self.config["proxy3"], proposal_num)
        result = self.okcli.query_proposal(proposal_num)
        time.sleep(15)

        # va1～va3查询抽成和outstanking一致，va4由于提前设置，不一致
        commission_va1 = self.okcli.query_commission(self.config["va1"])
        outstanding_va1 = self.okcli.query_outstanding(self.config["va1"])
        logging.info("commission_va1:" + commission_va1 + ", outstanding_va1:" + outstanding_va1)
        self.assert_compare_near(commission_va1, outstanding_va1)

        commission_va2 = self.okcli.query_commission(self.config["va2"])
        outstanding_va2 = self.okcli.query_outstanding(self.config["va2"])
        logging.info("commission_va2:" + commission_va2 + ", outstanding_va2:" + outstanding_va2)
        self.assert_compare_near(commission_va2, outstanding_va2)

        commission_va3 = self.okcli.query_commission(self.config["va3"])
        outstanding_va3 = self.okcli.query_outstanding(self.config["va3"])
        logging.info("commission_va3:" + commission_va3 + ", outstanding_va3:" + outstanding_va3)
        self.assert_compare_near(commission_va3, commission_va3)

        commission_va4 = self.okcli.query_commission(self.config["va4"])
        outstanding_va4 = self.okcli.query_outstanding(self.config["va4"])
        assert outstanding_va4 > commission_va4

        # proxy1~3, delegator1~3 查询分红为空，因为va1~va3抽成比例为100%
        result = self.okcli.query_rewards(self.config["proxy1"], "")
        assert len(result["total"]) == 0, result
        result = self.okcli.query_rewards(self.config["proxy2"], "")
        assert len(result["total"]) == 0, result
        result = self.okcli.query_rewards(self.config["proxy3"], "")
        assert len(result["total"]) == 0, result

        result = self.okcli.query_rewards(self.config["delegator1"], "")
        assert len(result["total"]) == 0, result
        result = self.okcli.query_rewards(self.config["delegator2"], "")
        assert len(result["total"]) == 0, result
        result = self.okcli.query_rewards(self.config["delegator3"], "")
        assert len(result["total"]) == 0, result

        # 取出va1的抽成，预期va1增加commission_va1，commission_va1 和 outstanding_va1为0
        beforeAmountVa1 = self.okcli.query_account(self.config["vaAdd1"])
        commission_va1 = self.okcli.query_commission(self.config["va1"])
        outstanding_va1 = self.okcli.query_outstanding(self.config["va1"])
        logging.info("commission_va1:" + str(commission_va1) + ", outstanding_va1:" + str(outstanding_va1))
        self.assert_compare_near(commission_va1, outstanding_va1)
        result = self.okcli.withdraw_commission(self.config["va1"], "va1")
        afterAmountVa1 = self.okcli.query_account(self.config["vaAdd1"])
        logging.info("afterAmountVa1:" + str(afterAmountVa1) + ", beforeAmountVa1:" + str(beforeAmountVa1))
        result = "afterAmountVa1:" + str(afterAmountVa1) + ", beforeAmountVa1:" + str(beforeAmountVa1)
        self.assert_compare_near(self.format_decimal(beforeAmountVa1) + self.format_decimal(commission_va1), self.format_decimal(afterAmountVa1))
        commission_va1 = self.okcli.query_commission(self.config["va1"])
        outstanding_va1 = self.okcli.query_outstanding(self.config["va1"])
        logging.info("commission_va1:" + str(commission_va1) + ", outstanding_va1:" + str(outstanding_va1))
        self.assert_compare_near(commission_va1, outstanding_va1)
        assert self.format_decimal(commission_va1) == 0

        # 22222222
        # 查询所有人的分红，为空
        result = self.okcli.query_rewards(self.config["proxy1"], "")
        assert len(result["total"]) == 0, result

        result = self.okcli.query_rewards(self.config["proxy2"], "")
        assert len(result["total"]) == 0, result

        result = self.okcli.query_rewards(self.config["proxy3"], "")
        assert len(result["total"]) == 0, result

        result = self.okcli.query_rewards(self.config["delegator1"], "")
        assert len(result["total"]) == 0, result

        result = self.okcli.query_rewards(self.config["delegator2"], "")
        assert len(result["total"]) == 0, result

        result = self.okcli.query_rewards(self.config["delegator3"], "")
        assert len(result["total"]) == 0, result
        
        # 代理人提取分红，无法取出
        beforeAmountvaProxy1 = self.okcli.query_account(self.config["proxy1"])
        beforeAmountvaDelegator1 = self.okcli.query_account(self.config["delegator1"])
        result = self.okcli.withdraw_rewards(self.config["va1"], self.config["proxy1"])
        logging.info(result)
        result = self.okcli.withdraw_rewards(self.config["va1"], self.config["delegator1"])
        logging.info(result)
        self.okcli.wait_ledger_than(2)
        afterAmountvaProxy1 = self.okcli.query_account(self.config["proxy1"])
        afterAmountvaDelegator1 = self.okcli.query_account(self.config["delegator1"])
        self.assert_compare_same(beforeAmountvaProxy1, afterAmountvaProxy1)
        self.assert_compare_same(beforeAmountvaDelegator1, afterAmountvaDelegator1)

        # 验证节点2 设置分红比例1%，代理2查询奖励有值，委托人2查询奖励有值，其他人查询为空
        result = self.okcli.edit_validator("0.01", "va2")
        self.okcli.wait_ledger_than(20)
        result = self.okcli.query_rewards(self.config["proxy2"], "")
        assert len(result["rewards"]) == 2, result
        assert len(result["rewards"][0]["reward"]) == 0, result
        assert len(result["rewards"][1]["reward"]) == 1, result

        result = self.okcli.query_rewards(self.config["delegator2"], "")
        assert len(result["rewards"]) == 2, result
        assert len(result["rewards"][0]["reward"]) == 0, result
        assert len(result["rewards"][1]["reward"]) == 1, result

        result = self.okcli.query_rewards(self.config["proxy3"], "")
        assert len(result["rewards"]) == 3, result
        assert len(result["rewards"][0]["reward"]) == 0, result
        assert len(result["rewards"][1]["reward"]) == 1, result
        assert len(result["rewards"][2]["reward"]) == 0, result

        result = self.okcli.query_rewards(self.config["delegator3"], "")
        assert len(result["rewards"]) == 3, result
        assert len(result["rewards"][0]["reward"]) == 0, result
        assert len(result["rewards"][1]["reward"]) == 1, result
        assert len(result["rewards"][2]["reward"]) == 0, result

        result = self.okcli.query_rewards(self.config["proxydelegator1"], "")
        assert len(result["total"]) == 0, result

        result = self.okcli.query_rewards(self.config["proxydelegator2"], "")
        assert len(result["total"]) == 0, result

        result = self.okcli.query_rewards(self.config["proxydelegator3"], "")
        assert len(result["total"]) == 0, result

        result = self.okcli.query_rewards(self.config["proxy1"], "")
        assert len(result["total"]) == 0, result

        result = self.okcli.query_rewards(self.config["delegator1"], "")
        assert len(result["total"]) == 0, result

        # 333333
        # 取出va1的抽成，预期va1增加commission_va1，commission_va1 和 outstanding_va1为0
        beforeAmountVa1 = self.okcli.query_account(self.config["vaAdd1"])
        commission_va1 = self.okcli.query_commission(self.config["va1"])
        outstanding_va1 = self.okcli.query_outstanding(self.config["va1"])
        logging.info("commission_va1:" + str(commission_va1) + ", outstanding_va1:" + str(outstanding_va1))
        self.assert_compare_near(commission_va1, outstanding_va1)
        result = self.okcli.withdraw_commission(self.config["va1"], "va1")
        afterAmountVa1 = self.okcli.query_account(self.config["vaAdd1"])
        logging.info("afterAmountVa1:" + str(afterAmountVa1) + ", beforeAmountVa1:" + str(beforeAmountVa1))
        result = "afterAmountVa1:" + str(afterAmountVa1) + ", beforeAmountVa1:" + str(beforeAmountVa1)
        self.assert_compare_near(self.format_decimal(beforeAmountVa1) + self.format_decimal(commission_va1), self.format_decimal(afterAmountVa1))
        commission_va1 = self.okcli.query_commission(self.config["va1"])
        outstanding_va1 = self.okcli.query_outstanding(self.config["va1"])
        logging.info("commission_va1:" + str(commission_va1) + ", outstanding_va1:" + str(outstanding_va1))
        self.assert_compare_near(commission_va1, outstanding_va1)
        assert self.format_decimal(commission_va1) == 0

        # 取出va2的抽成，预期va2增加commission_va2，commission_va2 和 outstanding_va2为0
        beforeAmountVa2 = self.okcli.query_account(self.config["vaAdd2"])
        commission_va2 = self.okcli.query_commission(self.config["va2"])
        outstanding_va2 = self.okcli.query_outstanding(self.config["va2"])
        logging.info("commission_va2:" + str(commission_va2) + ", outstanding_va2:" + str(outstanding_va2))
        self.assert_compare_gt(outstanding_va2, commission_va2)
        result = self.okcli.withdraw_commission(self.config["va2"], "va2")
        afterAmountVa2 = self.okcli.query_account(self.config["vaAdd2"])
        logging.info("afterAmountVa2:" + str(afterAmountVa2) + ", beforeAmountVa2:" + str(beforeAmountVa2))
        result = "afterAmountVa2:" + str(afterAmountVa2) + ", beforeAmountVa2:" + str(beforeAmountVa2)
        self.assert_compare_near(self.format_decimal(beforeAmountVa2) + self.format_decimal(commission_va2), self.format_decimal(afterAmountVa2))
        commission_va2 = self.okcli.query_commission(self.config["va2"])
        outstanding_va2 = self.okcli.query_outstanding(self.config["va2"])
        logging.info("commission_va2:" + str(commission_va2) + ", outstanding_va2:" + str(outstanding_va2))
        self.assert_compare_gt(outstanding_va2, commission_va2)
        assert self.format_decimal(commission_va2) == 0
        
        # 取出va4的抽成，预期va4增加commission_va4，commission_va4 和 outstanding_va4为0
        beforeAmountVa4 = self.okcli.query_account(self.config["vaAdd4"])
        commission_va4 = self.okcli.query_commission(self.config["va4"])
        outstanding_va4 = self.okcli.query_outstanding(self.config["va4"])
        logging.info("commission_va4:" + str(commission_va4) + ", outstanding_va4:" + str(outstanding_va4))
        self.assert_compare_gt(outstanding_va4, commission_va4)
        result = self.okcli.withdraw_commission(self.config["va4"], "va4")
        afterAmountVa4 = self.okcli.query_account(self.config["vaAdd4"])
        logging.info("afterAmountVa4:" + str(afterAmountVa4) + ", beforeAmountVa4:" + str(beforeAmountVa4))
        result = "afterAmountVa4:" + str(afterAmountVa4) + ", beforeAmountVa4:" + str(beforeAmountVa4)
        self.assert_compare_near(self.format_decimal(beforeAmountVa4) + self.format_decimal(commission_va4), self.format_decimal(afterAmountVa4))
        commission_va4 = self.okcli.query_commission(self.config["va4"])
        outstanding_va4 = self.okcli.query_outstanding(self.config["va4"])
        logging.info("commission_va4:" + str(commission_va4) + ", outstanding_va4:" + str(outstanding_va4))
        self.assert_compare_gt(outstanding_va4, commission_va4)
        assert self.format_decimal(commission_va4) == 0

        # delegator1无法取出va1的分红，因为验证节点va1没有设置比例
        beforeAmount = self.okcli.query_account(self.config["proxy1"])
        result = self.okcli.withdraw_rewards(self.config["va1"], self.config["proxy1"])
        afterAmount = self.okcli.query_account(self.config["proxy1"])
        self.assert_compare_same(beforeAmount, afterAmount)

        beforeAmount = self.okcli.query_account(self.config["delegator1"])
        result = self.okcli.withdraw_rewards(self.config["va1"], self.config["delegator1"])
        afterAmount = self.okcli.query_account(self.config["delegator1"])
        self.assert_compare_same(beforeAmount, afterAmount)

        # proxy2 取出va2的分红
        rewards = self.okcli.query_rewards(self.config["proxy2"], self.config["va2"])[0]["amount"]
        beforeAmount = self.okcli.query_account(self.config["proxy2"])
        result = self.okcli.withdraw_rewards(self.config["va2"], self.config["proxy2"])
        afterAmount = self.okcli.query_account(self.config["proxy2"])
        self.assert_compare_near(self.format_decimal(beforeAmount) + self.format_decimal(rewards), afterAmount)

        # delegator3 取出所有的分红
        rewards = self.okcli.query_rewards(self.config["delegator3"], "")["total"][0]["amount"]
        beforeAmount = self.okcli.query_account(self.config["delegator3"])
        result = self.okcli.withdraw_all_rewards(self.config["delegator3"])
        afterAmount = self.okcli.query_account(self.config["delegator3"])
        self.assert_compare_same(self.format_decimal(beforeAmount) + self.format_decimal(rewards), afterAmount)

        # 新增验证节点，进行质押
        result = self.okcli.create_validator(self.config["vaAddadmin16"])
        result = self.okcli.edit_validator("0.1", self.config["vaAddadmin16"])
        result = self.okcli.query_staking_validators()

        result = self.okcli.deposit(self.config["depoistCoin"], self.config["proxy4"])
        result = self.okcli.add_shares(self.valsall, self.config["proxy4"])

        result = self.okcli.deposit(self.config["depoistCoin"], self.config["delegator4"])
        result = self.okcli.add_shares(self.valsall, self.config["delegator4"])
        result = self.okcli.deposit(self.config["depoistCoin"], self.config["proxydelegator4"])

        result = self.okcli.proxy_reg(self.config["proxy4"])
        result = self.okcli.proxy_bind(self.config["proxy4"], self.config["proxydelegator4"])

        # proxydelegator4 有 tokens，shares 为 0
        resultProxydelegator4 = self.okcli.query_shares(self.config["proxydelegator4"])
        assert self.format_decimal(resultProxydelegator4["tokens"]) == self.config["depoistCoin"], resultProxydelegator4
        assert self.format_decimal(resultProxydelegator4["shares"]) == 0, resultProxydelegator4
        assert resultProxydelegator4["proxy_address"] == self.config["proxy4"], resultProxydelegator4

        # proxy4 的 total_delegated_tokens 等于 proxydelegator4 的 shares
        result = self.okcli.query_shares(self.config["proxy4"])
        assert result["is_proxy"] == True, result
        assert self.format_decimal(result["tokens"]) == self.config["depoistCoin"], result
        assert self.format_decimal(result["total_delegated_tokens"]) == self.format_decimal(resultProxydelegator4["tokens"]), result

        logging.info("------------------------after_distr_proposal end--------------------------------")

    def change_to_off_chain(self):
        if self.single_debug:
            result = self.okcli.kill_process("exchaind")
            result = self.okcli.run_all_node()
            result = self.okcli.version("exchaind") 
            assert result == "v1.6.1", result
            time.sleep(5)

        logging.info("------------------------change_to_off_chain start--------------------------------")
        # 11111111
        # 修改成链下分红
        result = self.okcli.submit_change_type_proposal_offchain(self.config["delegator1"])
        proposal_num=2
        result = self.okcli.query_proposal(proposal_num)
        result = self.okcli.vote(self.config["delegator1"], proposal_num)
        result = self.okcli.vote(self.config["delegator2"], proposal_num)
        result = self.okcli.vote(self.config["delegator3"], proposal_num)
        result = self.okcli.vote(self.config["delegator4"], proposal_num)
        result = self.okcli.vote(self.config["proxy1"], proposal_num)
        result = self.okcli.vote(self.config["proxy2"], proposal_num)
        result = self.okcli.vote(self.config["proxy3"], proposal_num)
        result = self.okcli.vote(self.config["proxy4"], proposal_num)
        result = self.okcli.query_proposal(proposal_num)

        # delegator1无法取出va1的分红，因为验证节点va1没有设置比例
        beforeAmount = self.okcli.query_account(self.config["proxy1"])
        result = self.okcli.withdraw_rewards(self.config["va1"], self.config["proxy1"])
        afterAmount = self.okcli.query_account(self.config["proxy1"])
        self.assert_compare_same(beforeAmount, afterAmount)

        # proxy2 取出之前的所有的分红，仍可取出
        rewards = self.okcli.query_rewards(self.config["proxy2"], "")["total"][0]["amount"]
        self.assert_compare_gt(rewards, 1)
        beforeAmount = self.okcli.query_account(self.config["proxy2"])
        result = self.okcli.withdraw_all_rewards(self.config["proxy2"])
        afterAmount = self.okcli.query_account(self.config["proxy2"])
        self.assert_compare_same(self.format_decimal(beforeAmount) + self.format_decimal(rewards), afterAmount)

        # 等待n个出块周期，确保proxy2不再接受分红
        self.okcli.wait_ledger_than(20)
        result = self.okcli.query_rewards(self.config["proxy2"], "")
        assert len(result["total"]) == 0, result


        # 22222222
        # 验证节点1 设置分红比例1%
        result = self.okcli.edit_validator("0.01", "va1")
        self.okcli.wait_ledger_than(20)

        # proxy1 的分红仍然为0
        result = self.okcli.query_rewards(self.config["proxy1"], "")
        assert len(result["total"]) == 0, result

        # delegator1 的分红仍然为0
        result = self.okcli.query_rewards(self.config["delegator1"], "")
        assert len(result["total"]) == 0, result

        # proxy4 取出所有的分红，仍可取出
        rewards = self.okcli.query_rewards(self.config["proxy4"], "")["total"][0]["amount"]
        self.assert_compare_gt(rewards, 1)
        beforeAmount = self.okcli.query_account(self.config["proxy4"])
        result = self.okcli.withdraw_all_rewards(self.config["proxy4"])
        afterAmount = self.okcli.query_account(self.config["proxy4"])
        addValue = self.format_decimal(afterAmount) - self.format_decimal(beforeAmount)
        assert addValue >= 0
        assert addValue < self.format_decimal(rewards)

        # 新增质押人5
        result = self.okcli.deposit(self.config["depoistCoin"], self.config["proxy5"])
        result = self.okcli.add_shares(self.valsall, self.config["proxy5"])

        result = self.okcli.deposit(self.config["depoistCoin"], self.config["delegator5"])
        result = self.okcli.add_shares(self.valsall, self.config["delegator5"])
        result = self.okcli.deposit(self.config["depoistCoin"], self.config["proxydelegator5"])

        result = self.okcli.proxy_reg(self.config["proxy5"])
        result = self.okcli.proxy_bind(self.config["proxy5"], self.config["proxydelegator5"])

        # 333333333
        # 取出v1的分红，预期正常
        beforeAmountVa1 = self.okcli.query_account(self.config["vaAdd1"])
        commission_va1 = self.okcli.query_commission(self.config["va1"])
        outstanding_va1 = self.okcli.query_outstanding(self.config["va1"])
        logging.info("commission_va1:" + str(commission_va1) + ", outstanding_va1:" + str(outstanding_va1))
        self.assert_compare_same(outstanding_va1, commission_va1)
        result = self.okcli.withdraw_commission(self.config["va1"], "va1")
        afterAmountVa1 = self.okcli.query_account(self.config["vaAdd1"])
        logging.info("afterAmountVa1:" + str(afterAmountVa1) + ", beforeAmountVa1:" + str(beforeAmountVa1))
        result = "afterAmountVa1:" + str(afterAmountVa1) + ", beforeAmountVa1:" + str(beforeAmountVa1)
        self.assert_compare_near(self.format_decimal(beforeAmountVa1) + self.format_decimal(commission_va1), self.format_decimal(afterAmountVa1))
        commission_va1 = self.okcli.query_commission(self.config["va1"])
        outstanding_va1 = self.okcli.query_outstanding(self.config["va1"])
        logging.info("commission_va1:" + str(commission_va1) + ", outstanding_va1:" + str(outstanding_va1))
        self.assert_compare_same(outstanding_va1, commission_va1)
        assert self.format_decimal(commission_va1) == 0

        # 查询正常
        result = self.okcli.query_commission(self.config["va2"])
        result = self.okcli.query_commission(self.config["va3"])
        result = self.okcli.query_commission(self.config["va4"])
        result = self.okcli.query_commission(self.config["vaadmin16"])

        result = self.okcli.query_outstanding(self.config["va2"])
        result = self.okcli.query_outstanding(self.config["va3"])
        result = self.okcli.query_outstanding(self.config["va4"])
        result = self.okcli.query_outstanding(self.config["vaadmin16"])

        # 查询分红正常
        result = self.okcli.query_rewards(self.config["proxy1"], "")
        assert len(result["total"]) == 0, result
        result = self.okcli.query_rewards(self.config["proxy2"], "")
        assert len(result["total"]) == 0, result
        result = self.okcli.query_rewards(self.config["proxy3"], "")
        assert len(result["total"]) > 0, result
        result = self.okcli.query_rewards(self.config["proxy4"], "")
        assert len(result["total"]) == 0, result
        result = self.okcli.query_rewards(self.config["proxy5"], "")
        assert len(result["total"]) == 0, result

        result = self.okcli.query_rewards(self.config["delegator1"], "")
        assert len(result["total"]) == 0, result
        result = self.okcli.query_rewards(self.config["delegator2"], "")
        assert len(result["total"]) > 0, result
        result = self.okcli.query_rewards(self.config["delegator3"], "")
        assert len(result["total"]) > 0, result
        result = self.okcli.query_rewards(self.config["delegator4"], "")
        assert len(result["total"]) > 0, result
        result = self.okcli.query_rewards(self.config["delegator5"], "")
        assert len(result["total"]) == 0, result

        # 再次尝试取出 proxy4 所有分红，失败
        self.okcli.wait_ledger_than(20)
        beforeAmount = self.okcli.query_account(self.config["proxy4"])
        result = self.okcli.withdraw_all_rewards(self.config["proxy4"])
        afterAmount = self.okcli.query_account(self.config["proxy4"])
        self.assert_compare_near(beforeAmount, afterAmount)

        # 尝试取出 proxy5 所有分红，失败
        beforeAmount = self.okcli.query_account(self.config["proxy5"])
        result = self.okcli.withdraw_all_rewards(self.config["proxy5"])
        afterAmount = self.okcli.query_account(self.config["proxy5"])
        self.assert_compare_near(beforeAmount, afterAmount)

        # 参数为0
        result = self.okcli.query_distr_params()
        assert result["distribution_type"] == 0, result

        logging.info("------------------------change_to_off_chain end--------------------------------")

    def change_to_on_chain(self):
        result = self.okcli.run_all_node()
        result = self.okcli.version("exchaind") 
        assert result == "v1.6.1", result
        time.sleep(5)
        
        logging.info("------------------------change_to_on_chain start--------------------------------")
        # 1111111111
        # 发起投票提案，修改提案链上分红
        result = self.okcli.submit_change_type_proposal_onchain(self.config["delegator1"])
        proposal_num=3
        result = self.okcli.query_proposal(proposal_num)
        result = self.okcli.vote(self.config["delegator1"], proposal_num)
        result = self.okcli.vote(self.config["delegator2"], proposal_num)
        result = self.okcli.vote(self.config["delegator3"], proposal_num)
        result = self.okcli.vote(self.config["delegator4"], proposal_num)
        result = self.okcli.vote(self.config["delegator5"], proposal_num)
        result = self.okcli.vote(self.config["proxy1"], proposal_num)
        result = self.okcli.vote(self.config["proxy2"], proposal_num)
        result = self.okcli.vote(self.config["proxy3"], proposal_num)
        result = self.okcli.vote(self.config["proxy4"], proposal_num)
        # result = self.okcli.vote(self.config["proxy5"], proposal_num)
        result = self.okcli.query_proposal(proposal_num)
        self.okcli.wait_ledger_than(20)

        # 222222222
        # 查询 delegator 所有奖励
        result = self.okcli.query_rewards(self.config["delegator1"], "")
        assert len(result["total"]) > 0, result
        result = self.okcli.query_rewards(self.config["delegator2"], "")
        assert len(result["total"]) > 0, result
        result = self.okcli.query_rewards(self.config["delegator3"], "")
        assert len(result["total"]) > 0, result
        result = self.okcli.query_rewards(self.config["delegator4"], "")
        assert len(result["total"]) > 0, result
        result = self.okcli.query_rewards(self.config["delegator5"], "")
        assert len(result["total"]) > 0, result

        # 查询 delegator1 、proxy1 的 v1 分红正常，proxydelegator1 不存在质押关系
        result = self.okcli.query_rewards(self.config["proxy1"], self.config["va1"])
        assert len(result) > 0, result
        result = self.okcli.query_rewards(self.config["delegator1"], self.config["va1"])
        assert len(result) > 0, result
        result = self.okcli.query_rewards(self.config["proxydelegator1"], self.config["va1"])
        assert result == -1, result

        # 查询 delegator3 、proxy3的 v3 分红为空， proxydelegator3 不存在质押关系
        result = self.okcli.query_rewards(self.config["proxy3"], self.config["va3"])
        assert len(result) == 0, result
        result = self.okcli.query_rewards(self.config["delegator3"], self.config["va3"])
        assert len(result) == 0, result
        result = self.okcli.query_rewards(self.config["proxydelegator3"], self.config["va3"])
        assert result == -1, result

        # 设置 proxy3 的取款人地址
        self.okcli.set_withdraw_addr(self.config["withdrawaddress"], self.config["proxy3"])
        self.okcli.set_withdraw_addr(self.config["withdrawaddress"], self.config["delegator3"])        
        self.okcli.set_withdraw_addr(self.config["withdrawaddress"], self.config["delegator4"])
        self.okcli.set_withdraw_addr(self.config["withdrawaddress"], self.config["delegator5"])

        # 验证节点3 设置分红比例1%
        result = self.okcli.edit_validator("0.01", "va3")

        result = self.okcli.deposit(self.config["addDepoistCoin"], self.config["proxy3"])
        self.okcli.wait_ledger_than(20)
        # 查询 delegator3 、proxy3的 v3 分红正常， proxydelegator3 不存在质押关系
        result = self.okcli.query_rewards(self.config["proxy3"], self.config["va3"])
        assert len(result) > 0, result
        result = self.okcli.query_rewards(self.config["proxy3"], "")
        result = self.okcli.query_rewards(self.config["delegator3"], self.config["va3"])
        assert len(result) > 0, result
        result = self.okcli.query_rewards(self.config["proxydelegator3"], self.config["va3"])
        assert result == -1, result

        # 33333
        # 增加 proxy3 自身投票，预期分红到账
        result = self.okcli.query_rewards(self.config["proxy3"], "")
        rewards = result["total"][0]["amount"]
        result = self.okcli.query_rewards(self.config["proxy3"], self.config["va3"])
        assert len(result) > 0, result
        beforeAmount = self.okcli.query_account(self.config["withdrawaddress"])
        result = self.okcli.deposit(self.config["addDepoistCoin"], self.config["proxy3"])
        self.okcli.wait_ledger_than(2)
        result = self.okcli.query_rewards(self.config["proxy3"], "")
        self.assert_compare_near(result["total"][0]["amount"], 1)
        affertAmount = self.okcli.query_account(self.config["withdrawaddress"])
        self.assert_compare_near(self.format_decimal(rewards) + self.format_decimal(beforeAmount), affertAmount)

        # 减少 proxy3 自身投票，预期分红到账
        self.okcli.wait_ledger_than(20)
        result = self.okcli.query_rewards(self.config["proxy3"], "")
        rewards = result["total"][0]["amount"]
        result = self.okcli.query_rewards(self.config["proxy3"], self.config["va3"])
        assert len(result) > 0, result
        beforeAmount = self.okcli.query_account(self.config["withdrawaddress"])
        result = self.okcli.withdraw(self.config["addDepoistCoin"], self.config["proxy3"])
        self.okcli.wait_ledger_than(2)
        result = self.okcli.query_rewards(self.config["proxy3"], "")
        self.assert_compare_near(result["total"][0]["amount"], 1)
        affertAmount = self.okcli.query_account(self.config["withdrawaddress"])
        self.assert_compare_near(self.format_decimal(rewards) + self.format_decimal(beforeAmount), affertAmount)

        # 增加 proxy3 的代理投票，预期分红到账
        self.okcli.wait_ledger_than(20)
        result = self.okcli.query_rewards(self.config["proxy3"], "")
        rewards = result["total"][0]["amount"]
        result = self.okcli.query_rewards(self.config["proxy3"], self.config["va3"])
        assert len(result) > 0, result
        beforeAmount = self.okcli.query_account(self.config["withdrawaddress"])
        result = self.okcli.deposit(self.config["depoistCoin"], self.config["proxydelegator3"])
        self.okcli.wait_ledger_than(2)
        result = self.okcli.query_rewards(self.config["proxy3"], "")
        self.assert_compare_near(result["total"][0]["amount"], 1)
        affertAmount = self.okcli.query_account(self.config["withdrawaddress"])
        self.assert_compare_near(self.format_decimal(rewards) + self.format_decimal(beforeAmount), affertAmount)

        # 减少 proxy3 的代理投票，预期分红到账
        self.okcli.wait_ledger_than(20)
        result = self.okcli.query_rewards(self.config["proxy3"], "")
        rewards = result["total"][0]["amount"]
        result = self.okcli.query_rewards(self.config["proxy3"], self.config["va3"])
        assert len(result) > 0, result
        beforeAmount = self.okcli.query_account(self.config["withdrawaddress"])
        result = self.okcli.withdraw(self.config["depoistCoin"], self.config["proxydelegator3"])
        self.okcli.wait_ledger_than(2)
        result = self.okcli.query_rewards(self.config["proxy3"], "")
        self.assert_compare_near(result["total"][0]["amount"], 1)
        affertAmount = self.okcli.query_account(self.config["withdrawaddress"])
        self.assert_compare_near(self.format_decimal(rewards) + self.format_decimal(beforeAmount), affertAmount)

        # 解绑 proxy3 代理，预期分红到账
        self.okcli.wait_ledger_than(20)
        result = self.okcli.query_rewards(self.config["proxy3"], "")
        rewards = result["total"][0]["amount"]
        result = self.okcli.query_rewards(self.config["proxy3"], self.config["va3"])
        assert len(result) > 0, result
        beforeAmount = self.okcli.query_account(self.config["withdrawaddress"])
        result = self.okcli.unreg(self.config["proxy3"])
        self.okcli.wait_ledger_than(2)
        result = self.okcli.query_rewards(self.config["proxy3"], "")
        self.assert_compare_near(result["total"][0]["amount"], 1)
        affertAmount = self.okcli.query_account(self.config["withdrawaddress"])
        self.assert_compare_near(self.format_decimal(rewards) + self.format_decimal(beforeAmount), affertAmount)

        # 重新注册 proxy3 代理，分红仍然正常
        result = self.okcli.deposit(self.config["depoistCoin"], self.config["proxy3"])
        result = self.okcli.add_shares(self.vals3, self.config["proxy3"])
        result = self.okcli.proxy_reg(self.config["proxy3"])
        result = self.okcli.proxy_bind(self.config["proxy3"], self.config["proxydelegator3"])

        resultProxydelegator3 = self.okcli.query_shares(self.config["proxydelegator3"])
        assert self.format_decimal(resultProxydelegator3["tokens"]) == self.config["depoistCoin"], resultProxydelegator3
        assert self.format_decimal(resultProxydelegator3["shares"]) == 0, resultProxydelegator3
        assert resultProxydelegator3["proxy_address"] == self.config["proxy3"], resultProxydelegator3

        result = self.okcli.query_shares(self.config["proxy3"])
        assert result["is_proxy"] == True, result
        assert self.format_decimal(result["total_delegated_tokens"]) == self.format_decimal(resultProxydelegator3["tokens"]), result

        # 444444
        # 增加 delegator3 的投票，预期分红到账
        result = self.okcli.deposit(self.config["addDepoistCoin"], self.config["delegator3"])
        self.okcli.wait_ledger_than(20)
        result = self.okcli.query_rewards(self.config["delegator3"], "")
        rewards = result["total"][0]["amount"]
        result = self.okcli.query_rewards(self.config["delegator3"], self.config["va3"])
        assert len(result) > 0, result
        beforeAmount = self.okcli.query_account(self.config["withdrawaddress"])
        result = self.okcli.deposit(self.config["addDepoistCoin"], self.config["delegator3"])
        self.okcli.wait_ledger_than(2)
        result = self.okcli.query_rewards(self.config["delegator3"], "")
        self.assert_compare_near(result["total"][0]["amount"], 1)
        affertAmount = self.okcli.query_account(self.config["withdrawaddress"])
        self.assert_compare_near(self.format_decimal(rewards) + self.format_decimal(beforeAmount), affertAmount)

        # 取出 delegator3 的所有投票，预期分红到账
        self.okcli.wait_ledger_than(20)
        result = self.okcli.query_rewards(self.config["delegator3"], "")
        rewards = result["total"][0]["amount"]
        result = self.okcli.query_rewards(self.config["delegator3"], self.config["va3"])
        assert len(result) > 0, result
        beforeAmount = self.okcli.query_account(self.config["withdrawaddress"])
        result = self.okcli.query_shares(self.config["delegator3"])
        result = self.okcli.withdraw(self.format_decimal(result["tokens"]), self.config["delegator3"])
        self.okcli.wait_ledger_than(2)
        result = self.okcli.query_rewards(self.config["delegator3"], "")
        assert result == -1, result
        affertAmount = self.okcli.query_account(self.config["withdrawaddress"])
        self.assert_compare_near(self.format_decimal(rewards) + self.format_decimal(beforeAmount), affertAmount)

        # 取出 delegator3 的投票，等待30秒，再次取出分红为0
        self.okcli.wait_ledger_than(20)
        result = self.okcli.query_rewards(self.config["delegator3"], "")
        assert result == -1, result
        result = self.okcli.query_rewards(self.config["delegator3"], self.config["va3"])
        assert result == -1, result
        beforeAmount = self.okcli.query_account(self.config["withdrawaddress"])
        self.okcli.withdraw_all_rewards(self.config["delegator3"])
        self.okcli.wait_ledger_than(2)
        affertAmount = self.okcli.query_account(self.config["withdrawaddress"])
        self.assert_compare_same(beforeAmount, affertAmount)

        # delegator3 再次质押，30秒后仍有奖励
        result = self.okcli.deposit(self.config["depoistCoin"], self.config["delegator3"])
        result = self.okcli.add_shares(self.vals3, self.config["delegator3"])
        self.okcli.wait_ledger_than(20)
        result = self.okcli.query_rewards(self.config["delegator3"], "")
        assert len(result["total"]) == 1
        assert len(result["rewards"]) == 3
        result = self.okcli.withdraw(self.config["depoistCoin"], self.config["delegator3"])

        
        # 555555
        # 销毁验证节点
        result = self.okcli.query_validator(self.config["vaadmin16"])
        assert result["jailed"] == False, result
        result = self.okcli.destroy_validator(self.config["vaAddadmin16"])
        result = self.okcli.query_validator(self.config["vaadmin16"])
        assert result["jailed"] == True, result
        
        # 销毁验证节点，取出自己抽成
        beforeAmount = self.okcli.query_account(self.config["vaAddadmin16"])
        commission = self.okcli.query_commission(self.config["vaadmin16"])
        outstanding = self.okcli.query_outstanding(self.config["vaadmin16"])
        logging.info("commission:" + str(commission) + ", outstanding:" + str(outstanding))
        self.assert_compare_gt(outstanding, commission)
        result = self.okcli.withdraw_commission(self.config["vaadmin16"], self.config["vaAddadmin16"])
        afterAmount = self.okcli.query_account(self.config["vaAddadmin16"])
        logging.info("afterAmount:" + str(afterAmount) + ", beforeAmount:" + str(beforeAmount))
        result = "afterAmount:" + str(afterAmount) + ", beforeAmount:" + str(beforeAmount)
        self.assert_compare_near(self.format_decimal(beforeAmount) + self.format_decimal(commission), self.format_decimal(afterAmount))
        commission = self.okcli.query_commission(self.config["vaadmin16"])
        outstanding = self.okcli.query_outstanding(self.config["vaadmin16"])
        logging.info("commission:" + str(commission) + ", outstanding:" + str(outstanding))
        self.assert_compare_gt(outstanding, commission)
        assert self.format_decimal(commission) == 0

        # delegator4 取出质押
        self.okcli.wait_ledger_than(20)
        result = self.okcli.query_rewards(self.config["delegator4"], "")
        rewards = result["total"][0]["amount"]
        beforeAmount = self.okcli.query_account(self.config["withdrawaddress"])
        result = self.okcli.query_shares(self.config["delegator4"])
        result = self.okcli.withdraw(self.format_decimal(result["tokens"]), self.config["delegator4"])
        self.okcli.wait_ledger_than(2)
        result = self.okcli.query_rewards(self.config["delegator4"], self.config["vaadmin16"])
        assert result == -1, result
        affertAmount = self.okcli.query_account(self.config["withdrawaddress"])
        # self.assert_compare_near(self.format_decimal(rewards) + self.format_decimal(beforeAmount), affertAmount)
        addValue = self.format_decimal(affertAmount) - self.format_decimal(beforeAmount)
        assert addValue > 0
        assert addValue < self.format_decimal(rewards)

        # 30秒后，验证节点不再有抽成
        self.okcli.wait_ledger_than(20)
        beforeAmount = self.okcli.query_account(self.config["vaAddadmin16"])
        commission = self.okcli.query_commission(self.config["vaadmin16"])
        outstanding = self.okcli.query_outstanding(self.config["vaadmin16"])
        logging.info("commission:" + str(commission) + ", outstanding:" + str(outstanding))
        self.assert_compare_gt(outstanding, commission)
        result = self.okcli.withdraw_commission(self.config["vaadmin16"], self.config["vaAddadmin16"])
        afterAmount = self.okcli.query_account(self.config["vaAddadmin16"])
        logging.info("afterAmount:" + str(afterAmount) + ", beforeAmount:" + str(beforeAmount))
        result = "afterAmount:" + str(afterAmount) + ", beforeAmount:" + str(beforeAmount)
        self.assert_compare_same(beforeAmount, afterAmount)

        # delegator4 不再有分红
        result = self.okcli.query_rewards(self.config["delegator4"], self.config["vaadmin16"])
        assert result == -1, result
        beforeAmount = self.okcli.query_account(self.config["withdrawaddress"])
        self.okcli.withdraw_all_rewards(self.config["delegator4"])
        self.okcli.wait_ledger_than(2)
        affertAmount = self.okcli.query_account(self.config["withdrawaddress"])
        self.assert_compare_same(beforeAmount, affertAmount)

        #666666
        # 再次申请验证节点
        result = self.okcli.create_validator(self.config["vaAddadmin16"])
        result = self.okcli.edit_validator("0.1", self.config["vaAddadmin16"])
        result = self.okcli.query_staking_validators()
        result = self.okcli.query_commission(self.config["vaadmin16"])
        logging.info("query_commission:" + result)
        result = self.okcli.query_outstanding(self.config["vaadmin16"])
        logging.info("query_outstanding:" + result)
        result = self.okcli.query_validator(self.config["vaadmin16"])
        assert result["jailed"] == True, result

        # 质押人取出后，不再有分红
        self.okcli.wait_ledger_than(20)
        result = self.okcli.query_validator(self.config["vaadmin16"])
        assert result["jailed"] == True, result
        result = self.okcli.query_rewards(self.config["delegator5"], self.config["vaadmin16"])
        assert len(result) > 0, result
        result = self.okcli.withdraw_rewards(self.config["vaadmin16"], self.config["delegator5"])
        time.sleep(10)
        result = self.okcli.query_rewards(self.config["delegator5"], self.config["vaadmin16"])
        assert len(result) == 0, result

        # 新增质押人6
        result = self.okcli.deposit(self.config["depoistCoin"], self.config["proxy6"])
        result = self.okcli.add_shares(self.valsall, self.config["proxy6"])

        result = self.okcli.deposit(self.config["depoistCoin"], self.config["delegator6"])
        result = self.okcli.add_shares(self.valsall, self.config["delegator6"])
        result = self.okcli.deposit(self.config["depoistCoin"], self.config["proxydelegator6"])

        result = self.okcli.proxy_reg(self.config["proxy6"])
        result = self.okcli.proxy_bind(self.config["proxy6"], self.config["proxydelegator6"])

        # 查询抽成正常
        result = self.okcli.query_commission(self.config["va1"])
        result = self.okcli.query_commission(self.config["va2"])
        result = self.okcli.query_commission(self.config["va3"])
        result = self.okcli.query_commission(self.config["va4"])
        result = self.okcli.query_commission(self.config["vaadmin16"])

        result = self.okcli.query_outstanding(self.config["va1"])
        result = self.okcli.query_outstanding(self.config["va2"])
        result = self.okcli.query_outstanding(self.config["va3"])
        result = self.okcli.query_outstanding(self.config["va4"])
        result = self.okcli.query_outstanding(self.config["vaadmin16"])

        result = self.okcli.query_rewards(self.config["proxy1"], "")
        result = self.okcli.query_rewards(self.config["proxy2"], "")
        result = self.okcli.query_rewards(self.config["proxy3"], "")
        result = self.okcli.query_rewards(self.config["proxy4"], "")
        result = self.okcli.query_rewards(self.config["proxy5"], "")
        result = self.okcli.query_rewards(self.config["proxy6"], "")

        result = self.okcli.query_rewards(self.config["delegator1"], "")
        result = self.okcli.query_rewards(self.config["delegator2"], "")
        result = self.okcli.query_rewards(self.config["delegator3"], "")
        result = self.okcli.query_rewards(self.config["delegator4"], "")
        result = self.okcli.query_rewards(self.config["delegator5"], "")
        result = self.okcli.query_rewards(self.config["delegator6"], "")

        # 取出分红分红正常
        result = self.okcli.withdraw_all_rewards(self.config["delegator1"])
        result = self.okcli.withdraw_all_rewards(self.config["delegator2"])
        result = self.okcli.withdraw_all_rewards(self.config["delegator3"])
        result = self.okcli.withdraw_all_rewards(self.config["delegator4"])
        result = self.okcli.withdraw_all_rewards(self.config["delegator5"])
        result = self.okcli.withdraw_all_rewards(self.config["delegator6"])

        result = self.okcli.withdraw_rewards(self.config["va1"], self.config["proxy1"])
        result = self.okcli.withdraw_rewards(self.config["va1"], self.config["proxy2"])
        result = self.okcli.withdraw_rewards(self.config["va1"], self.config["proxy3"])
        result = self.okcli.withdraw_rewards(self.config["va1"], self.config["proxy4"])
        result = self.okcli.withdraw_rewards(self.config["va1"], self.config["proxy5"])
        result = self.okcli.withdraw_rewards(self.config["va1"], self.config["proxy6"])
        result = self.okcli.withdraw_rewards(self.config["vaadmin16"], self.config["proxy1"])
        assert result == -1, result
        result = self.okcli.withdraw_rewards(self.config["vaadmin16"], self.config["proxy2"])
        assert result == -1, result
        result = self.okcli.withdraw_rewards(self.config["vaadmin16"], self.config["proxy3"])
        assert result == -1, result
        result = self.okcli.withdraw_rewards(self.config["vaadmin16"], self.config["proxy4"])
        assert result != -1, result
        result = self.okcli.withdraw_rewards(self.config["vaadmin16"], self.config["proxy5"])
        assert result != -1, result
        result = self.okcli.withdraw_rewards(self.config["vaadmin16"], self.config["proxy6"])
        assert result == -1, result

        result = self.okcli.query_distr_params()
        assert result["distribution_type"] == 1, result

        logging.info("------------------------change_to_on_chain end--------------------------------")

    def exit(self, stop = True):
        if stop:
            case.okcli.kill_process("exchaind")
        logging.info("Please use arg eg:  test | all")
        sys.exit()

if __name__ == '__main__':
    pybase = pybase.Pybase()

    file = open('config/case_distr_proposal.json', 'r', encoding='UTF-8')
    moduleConfig = json.loads(file.read())
    file.close()
    case = CaseDistrProposal(moduleConfig)

    if len(sys.argv) < 2:
        case.exit()
    opt = sys.argv[1]
    if opt == "all":
        case.all()
    elif opt == "test":
        case.test()
    elif opt == "start":
        case.okcli.run_all_node()
    elif opt == "stop":
        case.okcli.kill_process("exchaind")
    elif opt == "ps":
        case.okcli.ps("exchaind")
    elif opt == "ledger":
        logging.info(str(case.okcli.get_ledger_seq()))
    else:
        case.exit()
