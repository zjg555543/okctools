# /usr/bin/env python3
# --coding:utf-8 --
import json
import logging
import os
import time
import json

class OKCli:
    def __init__(self, exchaind, exchaincli, chainID, rpc):
        self.exchaind = exchaind
        self.exchaincli = exchaincli
        self.node_rpc = " --chain-id " + chainID + " --node " + rpc

    def version(self, name):
        cmd = name + ' version'
        result = os.popen(cmd).read().rstrip()
        logging.info("version, cmd: " + cmd + " result:" + result)
        return result

    def get_ledger_seq(self, rpc = ""):
        cmd = 'exchaincli status '
        if len(rpc) > 0:
            cmd = cmd + " --node " + rpc
        else:
            cmd = cmd + self.node_rpc
        
        result = os.popen(cmd).read().rstrip()
        # logging.info("result, cmd:" + cmd + ", result:" + result)

        result_obj = json.loads(result)
        return int(result_obj["sync_info"]["latest_block_height"])

    def get_ledger_seq_from_hash(self, hash):
        cmd = " exchaincli query tx " + hash  + self.node_rpc
        result = os.popen(cmd).read()
        result_obj = json.loads(result)
        return int(result_obj["height"])

    def wait_ledger(self, target):
        cur = self.get_ledger_seq()
        logging.info("waiting.. cur ledger seq:" + str(cur) + ", target seq:" + str(target))
        while True:
            cur = self.get_ledger_seq()
            if int(cur) >= int(target):
                logging.info("wait ok. cur ledger seq:" + str(cur) + ", target seq:" + str(target))
                break
            time.sleep(1)
            # logging.info("waiting.. cur ledger seq:" + str(cur) + ", target seq:" + str(target))
    def wait_ledger_than(self, num):
        self.wait_ledger(self.get_ledger_seq() + int(num))

    def run_tx(self, cmd):
        now = self.get_ledger_seq()
        self.wait_ledger(now + 1)

        result = os.popen(cmd).read()
        logging.info("result, cmd:  " + cmd + " , result:" + result)

        if len(result) == 0:
            return -1

        result_obj = json.loads(result)
        if "code" in result_obj:
            logging.error("result, cmd:" + cmd + "result:" + result)
            return -1
        self.query_tx(result_obj["txhash"])
        return result_obj["txhash"]
        
    def kill_process(self, name):
        cmd = "killall " + name
        result = os.popen(cmd).read()
        logging.info("result, cmd:" + cmd + ", result:" + result)
        time.sleep(3)

    def kill_all_process(self):
        self.kill_process("exchaind")
        self.kill_process("exchaind-my")
        self.kill_process("exchaind-dev")

    def ps(self, name):
        cmd = "ps axu | grep " + name
        result = os.popen(cmd).read()
        logging.info("result, cmd:" + cmd + ", result:" + result)

    def run_all_node(self, nums, block_time, newVersonNum, nodes):
        for i in range(nums):
            proName = "exchaind-dev"
            if i < newVersonNum:
                proName = "exchaind-my"
            cmd = "nohup %s start --home %snode%d/exchaind --p2p.seed_mode=true --p2p.allow_duplicate_ip --enable-dynamic-gp=false --rpc.enable-multi-call=true --enable-wtx=false --mempool.node_key_whitelist 0b066ca0790f27a6595560b23bf1a1193f100797,3813c7011932b18f27f172f0de2347871d27e852,6ea83a21a43c30a280a3139f6f23d737104b6975,bab6c32fa95f3a54ecb7d32869e32e85a25d2e08,testnet-node-ids --p2p.pex=false --p2p.addr_book_strict=false --p2p.seeds 0b066ca0790f27a6595560b23bf1a1193f100797@127.0.0.1:26656 --p2p.laddr tcp://127.0.0.1:%d --rpc.laddr tcp://127.0.0.1:%d --log_level main:info,*:error,consensus:error,state:info,distr:debug,gov:debug,staking:debug --chain-id exchain-67 --upload-delta=false --enable-gid --consensus.timeout_commit %dms --enable-blockpart-ack=false --block-part-size 16 --block-compress-type 0 --block-compress-flag 0 --block-compress-threshold 512 --append-pid=true --elapsed DeliverTxs=0,Round=1,CommitRound=1,Produce=1 --rest.laddr tcp://localhost:%d --enable-preruntx=false --consensus-role=v0 --keyring-backend test >%sval%d.log 2>&1 &" % (proName, nodes, i, 26656 + i * 100, 26657 + i * 100, block_time ,8545 + i * 100, nodes, i)
            time.sleep(1)
            # logging.info("result, cmd:" + cmd)
            self.run_node(cmd)

    def run_node(self, cmd):
        result = os.popen(cmd).read()
        logging.info("result, cmd:" + cmd + ", result:" + result)

    def deposit(self, token, from_name, sim=True):
        gas = " --gas auto "
        if sim == False:
            gas = " --gas=30000000 "

        cmd = "exchaincli tx staking deposit " + str(token) + "okt --from " + from_name + gas + " --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y" + self.node_rpc
        return self.run_tx(cmd)

    def add_shares(self, vals, from_name, sim=True):
        gas = " --gas auto "
        if sim == False:
            gas = " --gas=30000000 "
        cmd = "exchaincli tx staking add-shares " + vals + " --from " + from_name + gas + " --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y"  + self.node_rpc
        return self.run_tx(cmd)

    def transfer(self, from_name, to_name, tokens):
        cmd = "exchaincli tx send " + from_name + " " + to_name + " " + str(tokens) + "okt --from " + from_name + " --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y"  + self.node_rpc
        return self.run_tx(cmd)

    def proxy_reg(self, from_name, sim=True):
        gas = " --gas auto "
        if sim == False:
            gas = " --gas=30000000 "
        cmd = "exchaincli tx staking proxy reg --from " + from_name + gas + " --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y"  + self.node_rpc
        return self.run_tx(cmd)

    def proxy_bind(self, proxy, from_name, sim=True):
        gas = " --gas auto "
        if sim == False:
            gas = " --gas=30000000 "
        cmd = "exchaincli tx staking proxy bind "+ proxy +" --from " + from_name + gas + " --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y"  + self.node_rpc
        return self.run_tx(cmd)

    def proxy_unbind(self, from_name):
        cmd = "exchaincli tx staking proxy unbind --from " + from_name + " --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y"  + self.node_rpc
        return self.run_tx(cmd)

    def submit_change_type_proposal_offchain(self, from_name, sim=True):
        gas = " --gas auto "
        if sim == False:
            gas = " --gas=30000000 "
        cmd = "exchaincli tx gov submit-proposal change-distr-type proposal-change-distr-type-0.json --from " + from_name + gas + " --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y"  + self.node_rpc
        tx = self.run_tx(cmd)
        if tx == -1:
            return -1

        cmd = " exchaincli query tx " + tx  + self.node_rpc
        result = os.popen(cmd).read()
        result_obj = json.loads(result)
        return result_obj["logs"][0]["events"][1]["attributes"][1]["value"]

    def submit_change_type_proposal_onchain(self, from_name):
        cmd = "exchaincli tx gov submit-proposal change-distr-type proposal-change-distr-type-1.json --from " + from_name + " --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y"  + self.node_rpc
        tx = self.run_tx(cmd)
        cmd = " exchaincli query tx " + tx  + self.node_rpc
        result = os.popen(cmd).read()
        result_obj = json.loads(result)
        return result_obj["logs"][0]["events"][1]["attributes"][1]["value"]
        

    def submit_withdraw_reward_enabled(self, from_name, sim=True):
        gas = " --gas auto "
        if sim == False:
            gas = " --gas=30000000 "

        cmd = "exchaincli tx gov submit-proposal withdraw-reward-enabled proposal-withdraw-enabled.json --from " + from_name + gas + " --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y"  + self.node_rpc
        tx = self.run_tx(cmd)
        if tx == -1:
            return -1

        cmd = " exchaincli query tx " + tx  + self.node_rpc
        result = os.popen(cmd).read()
        result_obj = json.loads(result)
        return result_obj["logs"][0]["events"][1]["attributes"][1]["value"]

    def submit_withdraw_reward_disabled(self, from_name):
        cmd = "exchaincli tx gov submit-proposal withdraw-reward-enabled proposal-withdraw-disabled.json --from " + from_name + " --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y"  + self.node_rpc
        tx = self.run_tx(cmd)
        cmd = " exchaincli query tx " + tx  + self.node_rpc
        result = os.popen(cmd).read()
        result_obj = json.loads(result)
        return result_obj["logs"][0]["events"][1]["attributes"][1]["value"]

    def vote(self, from_name, num):
        result = self.query_proposal(num)
        if result == "Passed":
            logging.info("passed proposal:" + num + ", from_name:" + from_name)
            return

        cmd = "exchaincli tx gov vote " + str(num) + " yes --from " + from_name + " --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y"  + self.node_rpc
        return self.run_tx(cmd)

    def withdraw_commission(self, val, from_name):
        cmd = "exchaincli tx distr withdraw-rewards " + val + " --commission --from " + from_name + " --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y"  + self.node_rpc
        return self.run_tx(cmd)

    def withdraw_rewards(self, val, from_name, sim=True):
        gas = " --gas auto "
        if sim == False:
            gas = " --gas=30000000 "
        cmd = "exchaincli tx distr withdraw-rewards " + val + " --from " + from_name + gas + " --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y"   + self.node_rpc
        return self.run_tx(cmd)

    def withdraw_all_rewards(self, from_name, sim=True):
        gas = " --gas auto "
        if sim == False:
            gas = " --gas=30000000 "
        cmd = "exchaincli tx distr withdraw-all-rewards --from " + from_name + gas + " --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y"  + self.node_rpc
        return self.run_tx(cmd)

    def create_validator(self, from_name):
        cmd = 'exchaincli tx staking create-validator --pubkey=$(exchaind tendermint show-validator) --moniker="zzzzzzzz" --from ' + from_name + ' --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y'  + self.node_rpc
        return self.run_tx(cmd)
    
    def edit_validator(self, details, from_name):
        cmd = "exchaincli tx staking edit-validator --details " + details + " --from " + from_name + " --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y"  + self.node_rpc
        return self.run_tx(cmd)

    def edit_validator_rate(self, rate, from_name, sim=True):
        gas = " --gas auto "
        if sim == False:
            gas = " --gas=30000000 "
        cmd = "exchaincli tx staking edit-validator-commission-rate " + str(rate) + " --from " + from_name + gas + " --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y"  + self.node_rpc
        return self.run_tx(cmd)
    
    def destroy_validator(self, from_name):
        cmd = "exchaincli tx staking destroy-validator --from " + from_name + " --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y"  + self.node_rpc
        return self.run_tx(cmd)

    def query_validator(self, validator):
        cmd = " exchaincli query staking validator " + validator  + self.node_rpc
        result = os.popen(cmd).read()
        logging.info("result, cmd:" + cmd + ", result:" + result)

        result_obj = json.loads(result)

        return result_obj

    def query_shares(self, delegator):
        cmd = " exchaincli query staking delegator " + delegator  + self.node_rpc
        result = os.popen(cmd).read()
        logging.info("result, cmd:" + cmd + ", result:" + result)

        result_obj = json.loads(result)

        return result_obj

    def query_proxy(self, delegator):
        cmd = " exchaincli query staking proxy " + delegator  + self.node_rpc
        result = os.popen(cmd).read()
        logging.info("result, cmd:" + cmd + ", result:" + result)

        result_obj = json.loads(result)

        return result_obj

    def query_account(self, address):
        cmd = " exchaincli query account  " + address  + self.node_rpc
        result = os.popen(cmd).read()
        logging.info("result, cmd:" + cmd + ", , result:" + result)

        result_obj = json.loads(result)

        return result_obj["value"]["coins"][0]["amount"]

    def query_commission(self, address, height = 0):
        arg = ""
        if height > 0:
            arg = " --height " + str(height)
        cmd = " exchaincli query distr commission   " + address + " " + arg  + self.node_rpc
        result = os.popen(cmd).read()
        logging.info("result, cmd:" + cmd + ", result:" + result)

        result_obj = json.loads(result)

        return result_obj[0]["amount"]

    def query_commission_gt(self, address, amount):
        while True:
            cmd = " exchaincli query distr commission   " + address  + self.node_rpc
            result = os.popen(cmd).read()
            logging.info("result, cmd:" + cmd + ", result:" + result)

            try:
                result_obj = json.loads(result)
                a = self.format_decimal(result_obj[0]["amount"])
                b = self.format_decimal(amount)
                logging.info("a:" + str(result_obj[0]["amount"]) + ",b:" + str(amount))
                if a > b:
                    break
            except:
                logging.error(result)
            time.sleep(1)

    # def query_rewards(self, delegator, validator):
    #     cmd = " exchaincli query distr rewards   " + delegator +  " " + validator  + self.node_rpc
    #     result = os.popen(cmd).read()
    #     logging.info("result, cmd:" + cmd + ", result:" + result)

    #     try:
    #         result_obj = json.loads(result)
    #         return result_obj
    #     except:
    #         return -1

    def query_rewards(self, delegator, validator, height = 0):
        arg = ""
        if height > 0:
            arg = " --height " + str(height)

        cmd = " exchaincli query distr rewards   " + delegator +  " " + validator + arg + "  "+ self.node_rpc
        result = os.popen(cmd).read()
        logging.info("result, cmd:" + cmd + ", result:" + result)

        try:
            result_obj = json.loads(result)
            return result_obj
        except:
            return -1

    def query_total_rewards_gt(self, delegator, validator, amount):
        while True:
            cmd = " exchaincli query distr rewards   " + delegator +  " " + validator  + self.node_rpc
            result = os.popen(cmd).read()
            logging.info("result, cmd:" + cmd + ", result:" + result)
            
            try:
                if len(validator) > 0:
                    result_obj = json.loads(result)
                    a = self.format_decimal(result_obj[0]["amount"])
                    b = self.format_decimal(amount)
                    logging.info("a:" + str(result_obj[0]["amount"]) + ",b:" + str(amount))
                    if a > b:
                        break
                else:
                    result_obj = json.loads(result)
                    a = self.format_decimal(result_obj["total"][0]["amount"])
                    b = self.format_decimal(amount)
                    logging.info("a:" + str(result_obj["total"][0]["amount"]) + ",b:" + str(amount))
                    if a > b:
                        break
            except:
                logging.error(result)
            time.sleep(1)

    def query_withdraw(self, address):
        cmd = " exchaincli query distr withdraw-addr   " + address  + self.node_rpc
        result = os.popen(cmd).read()
        logging.info("result, cmd:" + cmd + ", result:" + result)

        return result

    def query_staking_validators(self):
        cmd = " exchaincli query staking validators   "  + self.node_rpc
        result = os.popen(cmd).read()
        logging.info("result, cmd:" + cmd + ", result:" + result)
        result_obj = json.loads(result)
        return result_obj

    def query_proposal(self, num):
        cmd = " exchaincli query gov proposal   " + str(num)  + self.node_rpc
        result = os.popen(cmd).read()
        logging.info("result, cmd:" + cmd + ", result:" + result)

        result_obj = json.loads(result)

        return result_obj["proposal_status"]
    
    def query_outstanding(self, address, height = 0):
        arg = ""
        if height > 0:
            arg = " --height " + str(height)

        cmd = " exchaincli query distr outstanding-rewards   " + address + " " + arg  + self.node_rpc
        result = os.popen(cmd).read()
        logging.info("result, cmd:" + cmd + ", result:" + result)
        try:
            result_obj = json.loads(result)
        except:
            return -1

        return result_obj[0]["amount"]

    def query_outstanding_gt(self, address, amount):
        while True:
            cmd = " exchaincli query distr outstanding-rewards   " + address  + self.node_rpc
            result = os.popen(cmd).read()
            logging.info("result, cmd:" + cmd + ", result:" + result)

            try:
                result_obj = json.loads(result)
                a = self.format_decimal(result_obj[0]["amount"])
                b = self.format_decimal(amount)
                logging.info("a:" + str(result_obj[0]["amount"]) + ",b:" + str(amount))
                if a > b:
                    break
            except:
                logging.error(result)
            time.sleep(1)

    def query_shares_added_to(self, val):
        cmd = " exchaincli query staking shares-added-to   " + val + " " + self.node_rpc
        result = os.popen(cmd).read()
        logging.info("result, cmd:" + cmd + ", result:" + result)
        try:
            result_obj = json.loads(result)
        except:
            return -1

        return result_obj

    def query_distr_params(self):
        cmd = " exchaincli query distr params   "  + self.node_rpc
        result = os.popen(cmd).read()
        logging.info("result, cmd:" + cmd + ", result:" + result)

        result_obj = json.loads(result)

        return result_obj

    def run_cmd(self, cmd):
        result = os.popen(cmd).read()
        logging.info("result, cmd:" + cmd + ", result:" + result)

    def copy_node(self, toName, goBin):
        if len(goBin) <= 0:
            assert False
        if goBin == "/":
            assert False
            
        cmd = "rm " + goBin + toName
        result = os.popen(cmd).read()
        logging.info("result, cmd:" + cmd + ", result:" + result)
        
        cmd = "cp " + goBin + "exchaind " + goBin + toName
        result = os.popen(cmd).read()
        logging.info("result, cmd:" + cmd + ", result:" + result)

    def copy_node_cli(self, toName, goBin):
        if len(goBin) <= 0:
            assert False
        if goBin == "/":
            assert False

        cmd = "rm " + goBin + toName
        result = os.popen(cmd).read()
        logging.info("result, cmd:" + cmd + ", result:" + result)
        
        cmd = "cp " + goBin + "exchaincli " + goBin + toName
        result = os.popen(cmd).read()
        logging.info("result, cmd:" + cmd + ", result:" + result)

    def recover(self, name, mnemonic):
        cmd = 'exchaincli keys add --recover '  + name + ' -m "' + mnemonic + '" -y'
        result = os.popen(cmd).read()
        logging.info("result, cmd:" + cmd + ", result:" + result)
        # result_obj = json.loads(result)
        # return result_obj["name"]

    def recover_val(self, name, mnemonic):
        cmd = 'exchaincli keys add --recover '  + name + ' -m "' + mnemonic + '" --coin-type 996 -y'
        result = os.popen(cmd).read()
        logging.info("result, cmd:" + cmd + ", result:" + result)
        # result_obj = json.loads(result)
        # return result_obj["name"]

    def query_tx(self, tx, delay_seconds = 50):
        for i in range(1, delay_seconds):
            cmd = " exchaincli query tx " + tx  + self.node_rpc
            result = os.popen(cmd).read()
            try:
                result_obj = json.loads(result)
                if "gas_used" in result_obj:
                    logging.info("result, cmd:" + cmd + ", result:" + result)
                    if "code" in result_obj:
                        return result_obj["code"]
                    return 0
            except:
                a = 1
                # logging.info("result, cmd:" + cmd + ", result:" + result)
            time.sleep(1)
            

    def set_withdraw_addr(self, new_addr, from_name):
        cmd = "exchaincli tx distr set-withdraw-addr " + new_addr + " --from " + from_name + " --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y"  + self.node_rpc
        return self.run_tx(cmd)

    def withdraw(self, amount, from_name):
        cmd = "exchaincli tx staking withdraw " + str(amount) + "okt --from " + from_name + " --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y"  + self.node_rpc
        return self.run_tx(cmd)

    def unreg(self, from_name):
        cmd = "exchaincli tx staking  proxy unreg --from " + from_name + " --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y"  + self.node_rpc
        return self.run_tx(cmd)

    def format_decimal(self, num):
        str_num = str(num)
        if "." in str_num:
            a, b = str(str_num).split('.')
            return int(a)
        else:
            return int(str_num)

