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

    def init(self):
        # result = self.okcli.run_cmd("cd " + self.config["newGitPath"] + "/dev/testnet/;./run4v1r.sh")
        # time.sleep(5)
        # result = self.okcli.version("exchaincli") 
        # assert result == self.config["newVersion"], result

        # case.okcli.kill_all_process()
        
        # case.okcli.run_all_raw_node(case.config["nodeCount"], case.config["ledgerTime"], case.config["nodes"])

        assert self.okcli.deposit("100000000", "ex1h0j8x0v9hs4eq6ppgamemfyu4vuvp2sl0q9p3v") != -1
        assert self.okcli.add_shares(self.vals3, "ex1h0j8x0v9hs4eq6ppgamemfyu4vuvp2sl0q9p3v") != -1
        # proposal_num = self.okcli.submit_change_type_proposal_onchain(self.config["vals"][0][1])
        # self.okcli.vote("ex1h0j8x0v9hs4eq6ppgamemfyu4vuvp2sl0q9p3v", proposal_num)
        # assert self.okcli.withdraw("10", "ex1h0j8x0v9hs4eq6ppgamemfyu4vuvp2sl0q9p3v") != -1

        # assert self.okcli.edit_validator_rate("0.1", self.config["vals"][0][1])
        # assert self.okcli.edit_validator_rate("0.1", self.config["vals"][1][1])

        return

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

    if opt == "init":
        case.init()
    elif opt == "start":
        case.okcli.run_all_raw_node(case.config["nodeCount"], case.config["ledgerTime"], case.config["nodes"])
    elif opt == "stop":
        case.okcli.kill_all_process()
    elif opt == "ps":
        case.okcli.ps("exchaind")
    elif opt == "ledger":
        logging.info(str(case.okcli.get_ledger_seq()))
    else:
        case.exit()
