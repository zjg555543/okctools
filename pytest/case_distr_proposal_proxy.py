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

class CaseDistrProposal:
    def __init__(self, configObj):
        self.config = configObj
        self.okcli = rpc.OKCli("exchaind", "exchaincli", self.config["chainId"], self.config["rpc"])
        return

    def test(self):
        logging.info("123")
        validators = self.okcli.query_staking_validators()
        for v in validators:
            # logging.info("validators:" + v["operator_address"])
            delegators = self.okcli.query_shares_added_to(v["operator_address"])
            if delegators == -1 or delegators == None:
                continue

            # logging.info("delegators:" + str(delegators))
            for d in delegators:
                # logging.info("delegator:" + d["delegator_address"])
                dInfo = self.okcli.query_shares(d["delegator_address"])
                if dInfo["is_proxy"] == True:
                    dList = self.okcli.query_proxy(d["delegator_address"])
                    logging.info("proxy-debug: v:" + v["operator_address"] + ", p:" + d["delegator_address"] + ", plist:" + str(dList))



        # self.okcli.query_shares("ex1qllmuet9vuq9eznqva5dxput4mq0lqh482nvzx")

        # self.okcli.query_proxy("ex1fye6qatnuxc4lprwpwzrza382dyp3xgkjqh6eh")


    def exit(self, stop = True):
        #if stop:
            #case.okcli.kill_process("exchaind")
        logging.info("Please use arg eg:  auto")
        sys.exit()

if __name__ == '__main__':
    pybase = pybase.Pybase()

    file = open('config/case_distr_proposal_proxy.json', 'r', encoding='UTF-8')
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
