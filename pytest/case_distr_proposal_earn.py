# /usr/bin/env python3
# --coding:utf-8 --
from cmath import log
import json
import logging
from os import system
import sys
import pybase
import rpc
# -*- coding: UTF-8 -*-

gProductBlockTime =  4               # 出块时间 4秒
gBlockPerYear =      7884000         # 年区块总数 365*24*60*60/4
gBlockReward =       0.5             # 区块奖励
gRewardsPerYear =    3942000         # 年区块奖励     7884000 * 0.5    
gSharesPerOkt =      7341748         # 1 OKT兑换的票数
gVoteOktNums  =      100             # 质押的OKT个数
gVoteValidatorNum =  30               # 投票的验证节点个数
gTopNum =            21              # 出块节点个数
gValidatorCommission = 0             # 验证节点抽成

class Validator:
    def __init__(self):
        self.name = ''                      # 节点名称
        self.address = ''                   # 地址
        self.shares = 0                     # 节点票数
        self.ratePerOneOKT = 0.0            # 1 okt兑换票占比
        self.rewards25PerYear = 0           # 节点年收益(25%部分)
        self.rewards75PerYear = 0           # 节点年收益(75%部分)
        self.rewardsPerYear = 0             # 节点年收益25 + 75
        self.commissionRate = 0.0           # 抽成比例
        self.depositOktNums = 0             # 质押okt个数
        self.depositOktRewardPerYear = 0    # 一年收益
        self.APR = 0.0                      # 年化收益率
        self.beTop21 = False                # 节点名称
        
    def get_property_str(self):
        return "name" + "," + "address" + ", " + "shares" + ", " + "ratePerOneOKT" + "," + "rewards25PerYear" + ", " + "rewards75PerYear" + ", " + "rewardsPerYear" + ", " + "commissionRate" + ", " + "depositOktNums" + ", " + "depositOktRewardPerYear" + ", " + "APR" + ", " + "top21"
    
    def to_str(self):
        return self.name + "," + self.address + ", " + str(self.shares) + ", " + str(self.ratePerOneOKT) + ", " + str(self.rewards25PerYear) + ", " + str(self.rewards75PerYear) + ", " + str(self.rewardsPerYear) + ", " + str(self.commissionRate) + ", "  + str(self.depositOktNums) + ", "  + str(self.depositOktRewardPerYear) + ", " + str(self.APR) + "%, " + str(self.beTop21)

    def update_rewards_25(self):
        self.beTop21 = True
        self.rewards25PerYear = "%.4f" % (gRewardsPerYear * 0.25 / gTopNum)

    def update_all_rewards(self, total_shares):
        self.rewards75PerYear = "%.4f" % (gRewardsPerYear * 0.75 * (self.shares / total_shares) )
        self.rewardsPerYear = "%.4f" % (float(self.rewards25PerYear) + float(self.rewards75PerYear))  

    def update_arp(self):
        self.ratePerOneOKT = "%.18f" % (gSharesPerOkt / self.shares)
        self.APR = "%.8f" % (float(self.ratePerOneOKT) *  float(self.rewardsPerYear) * (1 - self.commissionRate) * 100)
    
    def update_okt_nums(self, depositOktNums):
        self.depositOktNums = depositOktNums
        self.shares = self.shares + depositOktNums * gSharesPerOkt

    def update_okt_rewards(self):
        self.depositOktRewardPerYear = "%.8f" % (float(self.ratePerOneOKT) * self.depositOktNums * float(self.rewardsPerYear) * (1 - self.commissionRate))

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
        fileName = "data/vnums" + str(gVoteValidatorNum) +"_earn.csv"
        csv_file = open(fileName, "w")
        
        validators = self.okcli.query_staking_validators()
        jailed_str = ""
        logging.info("----------start----------")

        #init
        validators_map = {}
        for v in validators:
            if v["jailed"]:
                jailed_str += "\n" + v["description"]["moniker"] + ",   " + v["operator_address"] + ",  " + v["delegator_shares"]
            else:
                shares = self.format_decimal(v["delegator_shares"])
                validator = Validator()
                validator.name = v["description"]["moniker"]
                validator.address = v["operator_address"]
                validator.shares = shares
                validator.commissionRate = gValidatorCommission
                validators_map[shares] = validator

        #voting shares
        index = 0
        for i in sorted (validators_map, reverse=True) : 
            if index < gVoteValidatorNum:
                validators_map[i].update_okt_nums(gVoteOktNums)
            index = index + 1

        #get totalShares
        totalShares = 0
        for i in sorted (validators_map, reverse=True) : 
            totalShares += validators_map[i].shares

        # update
        index = 0
        for i in sorted (validators_map, reverse=True) : 
            if index == 0:
                csv_file.write(validators_map[i].get_property_str() + "\r")
            if index < gTopNum:
                validators_map[i].update_rewards_25()
            index = index + 1
            validators_map[i].update_all_rewards(totalShares)
            validators_map[i].update_arp()
            validators_map[i].update_okt_rewards()
            csv_file.write(validators_map[i].to_str() + "\r")

        csv_file.write("\r\r\r\r")
        csv_file.write("--------\r")


        # total arp
        index = 0
        totalArp = 0
        for i in sorted (validators_map, reverse=True) : 
            if index < gVoteValidatorNum:
                totalArp = totalArp + float(validators_map[i].APR)
            index = index + 1
        
        csv_file.write("voteOktNums,totalARP\r")
        csv_file.write(str(gVoteValidatorNum) +  ", " + "%.8f" % totalArp + "%" + "\r")

        logging.info("----------end----------")
        csv_file.close()

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
