# /usr/bin/env python3
# --coding:utf-8 --
from cmath import log
import json
import logging
from os import system
import sys
import pybase
import rpc

class CaseDistrProposal:
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

    def test(self):
        x = 1238888888888888888888888123
        
        logging.info(str(int(x)))

    def earn(self):

        validators = self.okcli.query_staking_validators()
        jailed_str = ""
        normal_str = ""
        logging.info("----------start----------")
        totalShares = 0
        
        for v in validators:
            if v["jailed"]:
                jailed_str += "\n" + v["description"]["moniker"] + ",   " + v["operator_address"] + ",  " + v["delegator_shares"]
            else:
                shares = self.format_decimal(v["delegator_shares"])
                arp = self.config["sharesPerOkt"] / shares
                normal_str += "\n" + v["description"]["moniker"] + ",   " + v["operator_address"] + ",  " + str(shares) + ",  " + "%.18f" % arp
                totalShares += shares
        logging.info("----------normal----------")
        logging.info(normal_str)
        logging.info("----------jailed----------")
        logging.info(jailed_str)
        logging.info("----------total shares----------")
        logging.info(str(totalShares))
        logging.info("----------end----------")

if __name__ == '__main__':
    pybase = pybase.Pybase()

    file = open('config/case_distr_proposal_earn.json', 'r', encoding='UTF-8')
    moduleConfig = json.loads(file.read())
    file.close()
    case = CaseDistrProposal(moduleConfig)
    opt = sys.argv[1]

    if opt == "test":
        case.test()

    if opt == "earn":
        case.earn()
