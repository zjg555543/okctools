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
        # dInfo = self.okcli.query_shares("ex15v0vlyltvkz4g9eju3ra2trmpppjafelhucn5h")

        # logging.info("delegator: ex15v0vlyltvkz4g9eju3ra2trmpppjafelhucn5h" + ", token:" + dInfo["tokens"])
        # for v in dInfo["validator_address"]:
        #     vInfo = self.okcli.query_validator(v)
        #     assert vInfo["jailed"] == False
        #     logging.info("vInfo:" + str(vInfo["jailed"]))


        validators = self.okcli.query_staking_validators()
        for v in validators:
            logging.info("validators:" + v["operator_address"])
            # delegators = self.okcli.query_shares_added_to(v["operator_address"])
            # if delegators == -1 or delegators == None:
            #     continue

            # logging.info("delegators:" + str(delegators))
            # for d in delegators:
            #     dInfo = self.okcli.query_shares(d["delegator_address"])
            #     logging.info("delegator:" + d["delegator_address"] + ", token:" + dInfo["tokens"])

            # return

        # self.okcli.query_shares("ex1qllmuet9vuq9eznqva5dxput4mq0lqh482nvzx")

        # self.okcli.query_proxy("ex1fye6qatnuxc4lprwpwzrza382dyp3xgkjqh6eh")

    def calcDepoistOKT(self):
        officeAccountMap = {}
        for account in self.config["officeAccounts"]:
            officeAccountMap[account] = True

        delegatorOfficeMap = {}
        delegatorNomarlMap = {}

        validators = self.okcli.query_staking_validators()
        for v in validators:
            logging.info("validators:" + v["operator_address"])
            if v["jailed"] == True:
                continue

            delegators = self.okcli.query_shares_added_to(v["operator_address"])
            if delegators == -1 or delegators == None:
                continue

            for d in delegators:
                dInfo = self.okcli.query_shares(d["delegator_address"])
                if d["delegator_address"] in officeAccountMap:
                    assert officeAccountMap[d["delegator_address"]] == True
                    delegatorOfficeMap[d["delegator_address"]] = dInfo["tokens"]
                else:
                    delegatorNomarlMap[d["delegator_address"]] = dInfo["tokens"] 

        output = "office delegator, tokens\n"
        for key in delegatorOfficeMap:
            output = output + key + "," + delegatorOfficeMap[key] + "\n"

        output = output + "\nnormal delegator, tokens\n"
        for key in delegatorNomarlMap:
            output = output + key + "," + delegatorNomarlMap[key] + "\n"
        
        logging.info(output)

        fileName = "data/deposit.csv"
        csv_file = open(fileName, "w")
        csv_file.write(output)
        csv_file.close()

if __name__ == '__main__':
    pybase = pybase.Pybase()

    file = open('config/case_distr_proposal_mainnet.json', 'r', encoding='UTF-8')
    moduleConfig = json.loads(file.read())
    file.close()
    case = CaseDistrProposal(moduleConfig)

    if len(sys.argv) < 2:
        case.exit()
    opt = sys.argv[1]

    if opt == "test":
        case.test()

    if opt == "calcDepoistOKT":
        case.calcDepoistOKT()

    else:
        case.exit()
