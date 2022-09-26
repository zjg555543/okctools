# /usr/bin/env python3
# --coding:utf-8 --
from cmath import log
from distutils.command.config import config
import json
import logging
from os import system
from pickletools import long1
import sys
import time
import pybase
import rpc
import _thread

class CaseDistrProposal:
    def __init__(self, configObj):
        self.config = configObj
        self.okcli = rpc.OKCli("exchaind", "exchaincli", self.config["chainId"], self.config["rpc"])

        self.valsall = ""
        first = True
        for v in self.config["vals"]:
            if first:
                self.valsall = v[3]
                first = False
            else:
                self.valsall = self.valsall + "," + v[3]
        # logging.info(self.valsall)
        return

    def press_proxy(self, threadName, delay):
        while True:
            total = len(self.config["proxys"])
            for i in range(total):
                logging.info("i:" + str(i))
                self.okcli.unreg_press(self.config["proxys"][i][1])
                self.okcli.proxy_reg_press(self.config["proxys"][i][1])
                self.okcli.proxy_bind_press(self.config["proxys"][i][1], self.config["proxydelegators"][i][1])
                self.okcli.withdraw_all_rewards_press(self.config["proxys"][i][1])
                self.okcli.proxy_unbind_press(self.config["proxydelegators"][i][1])

    def press_add_shares(self, threadName, delay):
        while True:
            total = len(self.config["delegators"])
            for i in range(total):
                logging.info("i:" + str(i))
                self.okcli.deposit_press("0.0001", self.config["delegators"][i][1])
                self.okcli.add_shares_press(self.valsall, self.config["delegators"][i][1])
                self.okcli.withdraw_all_rewards_press(self.config["delegators"][i][1])

    def press_add_shares_2(self, threadName, index):
        while True:
            for i in range(len(self.config["press_accounts"])):
                if i <= index:
                    continue

                if i >= index + 10:
                    continue
                # logging.info(str(i))
                # self.okcli.deposit_press("0.0001", v[0])
                self.okcli.add_shares_press(self.valsall, self.config["press_accounts"][i][0])
                self.okcli.withdraw_all_rewards_press(self.config["press_accounts"][i][0])

    def init_press_account(self):
         for v in self.config["press_accounts"]:
            self.okcli.recover(v[0], v[1])
            self.okcli.transfer(self.config["captain"], v[0], 10)
            

    def test(self):
        # self.okcli.create_account(1)
        # self.okcli.recover("123", "burger battle person bronze capable wash wood taxi bike rubber together title")

        # self.init_press_account()
        # return

        # _thread.start_new_thread(self.press_proxy, ("Thread-1", 1))
        # _thread.start_new_thread(self.press_add_shares, ("Thread-2", 2))
        for i in range(10):
             _thread.start_new_thread(self.press_add_shares_2, ("Thread-3", i * 10))
        
        while True:
            time.sleep(10)
            
    def exit(self, stop = True):
        logging.info("Please use arg eg:  auto")
        sys.exit()

if __name__ == '__main__':
    pybase = pybase.Pybase()

    file = open('config/case_distr_proposal_local.json', 'r', encoding='UTF-8')
    moduleConfig = json.loads(file.read())
    file.close()
    case = CaseDistrProposal(moduleConfig)

    if len(sys.argv) < 2:
        case.exit()
    opt = sys.argv[1]
    if opt == "test":
        case.test()
    elif opt == "start":
        case.okcli.run_all_node(case.config["nodeCount"], case.config["ledgerTime"])
    elif opt == "stop":
        case.okcli.kill_process("exchaind")
    elif opt == "ps":
        case.okcli.ps("exchaind")
    elif opt == "ledger":
        logging.info(str(case.okcli.get_ledger_seq()))
    else:
        case.exit()
