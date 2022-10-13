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
        self.valsall_1 = ""
        self.valsall_2 = ""
        self.valsall_3 = ""
        index = 0
        for v in self.config["vals"]:
            if index == 0:
                self.valsall = v[3]
                self.valsall_1 = v[3]
                self.valsall_2 = v[3]
                self.valsall_3 = v[3]
            elif index == 1:
                self.valsall = self.valsall + "," + v[3]
                self.valsall_2 = self.valsall_2 + "," + v[3]
                self.valsall_3 = self.valsall_3 + "," + v[3]
            elif index == 2:
                self.valsall = self.valsall + "," + v[3]
                self.valsall_3 = self.valsall_3 + "," + v[3]
            elif index == 3:
                self.valsall = self.valsall + "," + v[3]
            index = index + 1
        logging.info(self.valsall)
        logging.info(self.valsall_1)
        logging.info(self.valsall_2)
        logging.info(self.valsall_3)
        return

    def press_proxy(self, threadName, delay):
        while True:
            total = len(self.config["proxys"])
            for i in range(total):
                # logging.info("i:" + str(i))
                self.okcli.unreg(self.config["proxys"][i][1])
                self.okcli.proxy_reg(self.config["proxys"][i][1])
                self.okcli.proxy_bind(self.config["proxys"][i][1], self.config["proxydelegators"][i][1])
                self.okcli.withdraw_all_rewards(self.config["proxys"][i][1])
                self.okcli.proxy_unbind(self.config["proxydelegators"][i][1])

    def press_add_shares(self, threadName, delay):
        while True:
            total = len(self.config["delegators"])
            for i in range(total):
                # logging.info("i:" + str(i))
                self.okcli.deposit("0.0001", self.config["delegators"][i][1])
                mod = int(time.time()) % 3
                vals = self.valsall
                if mod == 0:
                    vals = self.valsall
                elif mod == 1:
                     vals = self.valsall_1
                elif mod == 2:
                     vals = self.valsall_2
                elif mod == 3:
                     vals = self.valsall_3

                # logging.info(vals)

                self.okcli.add_shares(vals, self.config["delegators"][i][1])
                self.okcli.withdraw_all_rewards(self.config["delegators"][i][1])

    def press_add_shares_2(self, threadName, index):
        while True:
            for i in range(len(self.config["press_accounts"])):
                if i <= index:
                    continue

                if i >= index + 10:
                    continue
                # logging.info(str(i))
                self.okcli.deposit("0.0001", self.config["press_accounts"][i][0])
                mod = int(time.time()) % 3
                vals = self.valsall
                if mod == 0:
                    vals = self.valsall
                elif mod == 1:
                     vals = self.valsall_1
                elif mod == 2:
                     vals = self.valsall_2
                elif mod == 3:
                     vals = self.valsall_3

                self.okcli.add_shares(vals, self.config["press_accounts"][i][0])
                self.okcli.withdraw_all_rewards(self.config["press_accounts"][i][0])

    def init_press_account(self):
         for v in self.config["press_accounts"]:
            self.okcli.recover(v[0], v[1])
            self.okcli.transfer(self.config["captain"], v[0], 10)

    def check_all(self):
        total = len(self.config["proxys"])
        for i in range(total):
            logging.info("i:" + str(i))
            self.okcli.unreg(self.config["proxys"][i][1])
            self.okcli.proxy_reg(self.config["proxys"][i][1])
            self.okcli.proxy_bind(self.config["proxys"][i][1], self.config["proxydelegators"][i][1])
            assert self.okcli.withdraw_all_rewards(self.config["proxys"][i][1]) != -1
            self.okcli.proxy_unbind(self.config["proxydelegators"][i][1])

        total = len(self.config["delegators"])
        for i in range(total):
            logging.info("i:" + str(i))
            assert self.okcli.deposit("0.0001", self.config["delegators"][i][1]) != -1
            assert self.okcli.add_shares(self.valsall, self.config["delegators"][i][1]) != -1
            assert self.okcli.withdraw_all_rewards(self.config["delegators"][i][1]) != -1

        for i in range(len(self.config["press_accounts"])):
            assert self.okcli.deposit("0.0001", self.config["press_accounts"][i][0]) != -1
            assert self.okcli.add_shares(self.valsall, self.config["press_accounts"][i][0]) != -1
            assert self.okcli.withdraw_all_rewards(self.config["press_accounts"][i][0]) !=- 1

    def test(self):
        # self.okcli.create_account(1)
        # self.okcli.recover("123", "burger battle person bronze capable wash wood taxi bike rubber together title")

        # self.init_press_account()
        # return

        _thread.start_new_thread(self.press_proxy, ("Thread-1", 1))
        _thread.start_new_thread(self.press_add_shares, ("Thread-2", 2))
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
    if opt == "check_all":
        case.check_all()
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
