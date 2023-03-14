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

gBlockPerYear =      8304636  # 年区块总数
gBlockReward =       0.125             # 区块奖励
gRewardsPerYear =    gBlockPerYear * gBlockReward   # 年区块奖励
gSharesPerOkt =      10109657         # 1 OKT兑换的票数 need change
gDepoistOKT  =      1             # 质押的OKT个数 
gVoteValidatorNum =  21              # 投票的验证节点个数 
gTopNum =            21              # 出块节点个数
gValidatorCommission = 0.2             # 验证节点抽成

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

    def reward(self):
        fileName = "data/vnums" + str(gVoteValidatorNum) + "_okt" + str(gDepoistOKT) +"_reward.csv"
        csv_file = open(fileName, "w")
        
        validators = self.okcli.query_staking_validators()
        jailed_str = ""
        logging.info("----------start----------")

        #init
        validators_list = []
        for v in validators:
            # shares = self.format_decimal(v["delegator_shares"])
            # logging.info(v["description"]["moniker"] + ", " + str(v["jailed"]) + ", " + v["operator_address"] + ", " + str(shares))
            if v["jailed"]:
                jailed_str += "\n" + v["description"]["moniker"] + ",   " + v["operator_address"] + ",  " + v["delegator_shares"]
            else:
                shares = self.format_decimal(v["delegator_shares"])
                validator = Validator()
                validator.name = v["description"]["moniker"]
                validator.address = v["operator_address"]
                validator.shares = shares
                validator.commissionRate = gValidatorCommission
                validators_list.append(validator)
        #voting shares
        logging.info("legth:" + str(len(validators_list)))
        validators_list = sorted(validators_list, key=lambda x: x.shares, reverse=True)
        for index in range(len(validators_list)) : 
            if index < gVoteValidatorNum:
                validators_list[index].update_okt_nums(gDepoistOKT)
                # logging.info(str(index) + ", shares:" + str(validators_list[index].shares))
        
        #get totalShares
        validators_list = sorted(validators_list, key=lambda x: x.shares, reverse=True)
        totalShares = 0
        for index in range(len(validators_list)) : 
            totalShares += validators_list[index].shares

        # update
        for index in range(len(validators_list)) : 
            if index == 0:
                csv_file.write(validators_list[index].get_property_str() + "\r")
            if index < gTopNum:
                validators_list[index].update_rewards_25()
            validators_list[index].update_all_rewards(totalShares)
            validators_list[index].update_arp()
            validators_list[index].update_okt_rewards()
            csv_file.write(validators_list[index].to_str() + "\r")

        csv_file.write("\r\r\r\r")
        csv_file.write("--------\r")


        # total arp
        totalArp = 0
        for index in range(len(validators_list)) : 
            if index < gVoteValidatorNum:
                totalArp = totalArp + float(validators_list[index].APR)
        
        csv_file.write("depoistOKT,voteValidatorNum,totalARP\r")
        csv_file.write(str(gDepoistOKT) +  ", " + str(gVoteValidatorNum) +  ", " + "%.8f" % totalArp + "%" + "\r")

        logging.info("----------end----------")
        csv_file.close()

    def format_decimal(self, num):
        str_num = str(num)
        if "." in str_num:
            a, b = str(str_num).split('.')
            return int(a)
        else:
            return int(str_num)

    def no_office_staking(self):
        # fileName = "data/vnums" + str(gVoteValidatorNum) + "_okt" + str(gDepoistOKT) +"_reward.csv"
        # csv_file = open(fileName, "w")
        
        validators = self.okcli.query_staking_validators()
        # jailed_str = ""
        logging.info("----------start----------")

        #非官方的delegator
        no_office_deledator = {}
        for v in validators:
            # shares = self.format_decimal(v["delegator_shares"])
            # logging.info(v["description"]["moniker"] + ", " + str(v["jailed"]) + ", " + v["operator_address"])
            # if v["jailed"]:
            #     jailed_str += "\n" + v["description"]["moniker"] + ",   " + v["operator_address"] + ",  " + v["delegator_shares"]
            #     continue

            # logging.info(self.format_decimal(v["min_self_delegation"]))

            # 忽略掉官方信息
            if self.is_office_v(v["operator_address"]) == True:
                continue
            logging.info("no office validator:" + v["operator_address"])
            delegators = self.okcli.query_shares_added_to(v["operator_address"])

            if delegators == -1 or delegators == None:
                continue

            # logging.info("delegators:" + str(delegators))
            for d in delegators:
                no_office_deledator[d["delegator_address"]] = True
            # logging.info(str(no_office_deledator))

        logging.info("total delegator nums:" + str(len(no_office_deledator)))
        total_tokens = 0
        for key, value in no_office_deledator.items():
                # logging.info("delegator:" + d["delegator_address"])
                dInfo = self.okcli.query_shares(key)
                # logging.info(dInfo["delegator_address"] + "," + dInfo["tokens"])
                total_tokens = total_tokens + self.format_decimal(dInfo["tokens"])
                # if dInfo["is_proxy"] == True:
                #     dList = self.okcli.query_proxy(d["delegator_address"])
                #     logging.info("proxy-debug: v:" + v["operator_address"] + ", p:" + d["delegator_address"] + ", plist:" + str(dList))

        logging.info("No office deledator tokens:" + str(total_tokens))
    def is_office_v(self, operator):
        for index in range(len(self.config["v-nodes"])) : 
            if self.config["v-nodes"][index] == operator:
                return True
        return False

    def validator_rewards(self):
        fileName = "data/validator_rewards.csv"
        csv_file = open(fileName, "w")
        
        validators = self.okcli.query_staking_validators()
        jailed_str = ""
        logging.info("----------start----------")

        #init
        validators_list = []
        for v in validators:
            # shares = self.format_decimal(v["delegator_shares"])
            # logging.info(v["description"]["moniker"] + ", " + str(v["jailed"]) + ", " + v["operator_address"] + ", " + str(shares))
            if v["jailed"]:
                jailed_str += "\n" + v["description"]["moniker"] + ",   " + v["operator_address"] + ",  " + v["delegator_shares"]
            else:
                shares = self.format_decimal(v["delegator_shares"])
                validator = Validator()
                validator.name = v["description"]["moniker"]
                validator.address = v["operator_address"]
                validator.shares = shares
                validator.commissionRate = gValidatorCommission
                validators_list.append(validator)
        #voting shares
        validators_list = sorted(validators_list, key=lambda x: x.shares, reverse=True)
        for index in range(len(validators_list)) : 
            if index < gVoteValidatorNum:
                validators_list[index].update_okt_nums(gDepoistOKT)
                # logging.info(str(index) + ", shares:" + str(validators_list[index].shares))
        
        #get totalShares
        validators_list = sorted(validators_list, key=lambda x: x.shares, reverse=True)
        totalShares = 0
        for index in range(len(validators_list)) : 
            totalShares += validators_list[index].shares

        # update
        for index in range(len(validators_list)) : 
            if index == 0:
                csv_file.write(validators_list[index].get_property_str() + "\r")
            if index < gTopNum:
                validators_list[index].update_rewards_25()
            validators_list[index].update_all_rewards(totalShares)
            validators_list[index].update_arp()
            validators_list[index].update_okt_rewards()
            csv_file.write(validators_list[index].to_str() + "\r")

        csv_file.write("\r\r\r\r")
        csv_file.write("--------\r")

        # total arp
        totalArp = 0
        for index in range(len(validators_list)) : 
            if index < gVoteValidatorNum:
                totalArp = totalArp + float(validators_list[index].APR)
        
        csv_file.write("depoistOKT,voteValidatorNum,totalARP\r")
        csv_file.write(str(gDepoistOKT) +  ", " + str(gVoteValidatorNum) +  ", " + "%.8f" % totalArp + "%" + "\r")

        logging.info("----------end----------")

        office_validators_rewards = 0
        no_office_validators_rewards = 0
        for index in range(len(validators_list)) : 
            # 官方节点
            if self.is_office_v(validators_list[index].address) == True:
                # logging.info(validators_list[index].address)
                office_validators_rewards = office_validators_rewards + self.format_decimal(validators_list[index].rewardsPerYear)
            else:
                no_office_validators_rewards = no_office_validators_rewards + self.format_decimal(validators_list[index].rewardsPerYear)
        logging.info("office_validators_rewards:" + str(office_validators_rewards))
        logging.info("no_office_validators_rewards:" + str(no_office_validators_rewards))

    def outstanding(self):
        validators = self.okcli.query_staking_validators()
        logging.info("----------start----------")

        office_outstanding = 0
        no_office_outstanding = 0
        for v in validators:
            # 官方信息
            if self.is_office_v(v["operator_address"]) == True:
                # logging.info("office validator:" + v["operator_address"] + ",outstand:" + self.okcli.query_outstanding(v["operator_address"]))
                office_outstanding = office_outstanding + self.format_decimal(self.okcli.query_outstanding(v["operator_address"]))
            else:
                no_office_outstanding = no_office_outstanding + self.format_decimal(self.okcli.query_outstanding(v["operator_address"]))
        logging.info("office_outstanding:" + str(office_outstanding))
        logging.info("no_office_outstanding:" + str(no_office_outstanding))

if __name__ == '__main__':
    pybase = pybase.Pybase()

    file = open('config/case_distr_proposal_reward.json', 'r', encoding='UTF-8')
    moduleConfig = json.loads(file.read())
    file.close()
    case = CaseDistrProposal(moduleConfig)
    opt = sys.argv[1]

    if opt == "test":
        case.test()

    if opt == "reward":
        case.reward()

    if opt == "no_office_staking":
        case.no_office_staking()

    if opt == "validator_rewards":
        case.validator_rewards()

    if opt == "outstanding":
        case.outstanding()

    if opt == "reward_chat":
        gVoteValidatorNum =  1
        case.reward()
        gVoteValidatorNum =  5
        case.reward()
        gVoteValidatorNum =  10
        case.reward()
        gVoteValidatorNum =  15
        case.reward()
        gVoteValidatorNum =  20
        case.reward()
        gVoteValidatorNum =  25
        case.reward()
        gVoteValidatorNum =  30
        case.reward()
        
