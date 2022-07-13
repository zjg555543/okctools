# /usr/bin/env python3
# --coding:utf-8 --
import json
import logging
import os
import time
import json

class OKCli:
    def __init__(self, exchaind, exchaincli):
        self.exchaind = exchaind
        self.exchaincli = exchaincli

    def version(self, name):
        cmd = name + ' version'
        result = os.popen(cmd).read().rstrip()
        logging.info("version, cmd:" + cmd + "result:" + result)
        return result

    def get_ledger_seq(self):
        cmd = 'exchaincli status'
        result = os.popen(cmd).read().rstrip()
        #logging.info("result, cmd:" + cmd + ", result:" + result)

        result_obj = json.loads(result)
        return int(result_obj["sync_info"]["latest_block_height"])

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
        time.sleep(1)
    def ps(self, name):
        cmd = "ps axu | grep " + name
        result = os.popen(cmd).read()
        logging.info("result, cmd:" + cmd + ", result:" + result)

    def run_all_node(self):
        self.run_node("nohup exchaind start --home /Users/oker/workspace/nodes/node0/exchaind --p2p.seed_mode=true --p2p.allow_duplicate_ip --enable-dynamic-gp=false --enable-wtx=false --mempool.node_key_whitelist 0b066ca0790f27a6595560b23bf1a1193f100797,3813c7011932b18f27f172f0de2347871d27e852,6ea83a21a43c30a280a3139f6f23d737104b6975,bab6c32fa95f3a54ecb7d32869e32e85a25d2e08,testnet-node-ids --p2p.pex=false --p2p.addr_book_strict=false --p2p.laddr tcp://127.0.0.1:26656 --rpc.laddr tcp://127.0.0.1:26657 --log_level main:info,*:error,consensus:error,state:info,distr:debug,gov:debug,staking:debug --chain-id exchain-67 --upload-delta=false --enable-gid --consensus.timeout_commit 1000ms --enable-blockpart-ack=false --block-part-size 16 --block-compress-type 0 --block-compress-flag 0 --block-compress-threshold 512 --append-pid=true --elapsed DeliverTxs=0,Round=1,CommitRound=1,Produce=1 --rest.laddr tcp://localhost:8545 --enable-preruntx=false --consensus-role=v0 --keyring-backend test >/Users/oker/workspace/nodes/val0.log 2>&1 &")
        self.run_node("nohup exchaind start --home /Users/oker/workspace/nodes/node1/exchaind --p2p.seed_mode=false --p2p.allow_duplicate_ip --enable-dynamic-gp=false --enable-wtx=false --mempool.node_key_whitelist 0b066ca0790f27a6595560b23bf1a1193f100797,3813c7011932b18f27f172f0de2347871d27e852,6ea83a21a43c30a280a3139f6f23d737104b6975,bab6c32fa95f3a54ecb7d32869e32e85a25d2e08,testnet-node-ids --p2p.pex=false --p2p.addr_book_strict=false --p2p.seeds 0b066ca0790f27a6595560b23bf1a1193f100797@127.0.0.1:26656 --p2p.laddr tcp://127.0.0.1:26756 --rpc.laddr tcp://127.0.0.1:26757 --log_level main:info,*:error,consensus:error,state:info,distr:debug,gov:debug,staking:debug --chain-id exchain-67 --upload-delta=false --enable-gid --consensus.timeout_commit 1000ms --enable-blockpart-ack=false --block-part-size 16 --block-compress-type 0 --block-compress-flag 0 --block-compress-threshold 512 --append-pid=true --elapsed DeliverTxs=0,Round=1,CommitRound=1,Produce=1 --rest.laddr tcp://localhost:8645 --enable-preruntx=false --consensus-role=v1 --keyring-backend test >/Users/oker/workspace/nodes/val1.log 2>&1 &")
        self.run_node("nohup exchaind start --home /Users/oker/workspace/nodes/node2/exchaind --p2p.seed_mode=false --p2p.allow_duplicate_ip --enable-dynamic-gp=false --enable-wtx=false --mempool.node_key_whitelist 0b066ca0790f27a6595560b23bf1a1193f100797,3813c7011932b18f27f172f0de2347871d27e852,6ea83a21a43c30a280a3139f6f23d737104b6975,bab6c32fa95f3a54ecb7d32869e32e85a25d2e08,testnet-node-ids --p2p.pex=false --p2p.addr_book_strict=false --p2p.seeds 0b066ca0790f27a6595560b23bf1a1193f100797@127.0.0.1:26656 --p2p.laddr tcp://127.0.0.1:26856 --rpc.laddr tcp://127.0.0.1:26857 --log_level main:info,*:error,consensus:error,state:info,distr:debug,gov:debug,staking:debug --chain-id exchain-67 --upload-delta=false --enable-gid --consensus.timeout_commit 1000ms --enable-blockpart-ack=false --block-part-size 16 --block-compress-type 0 --block-compress-flag 0 --block-compress-threshold 512 --append-pid=true --elapsed DeliverTxs=0,Round=1,CommitRound=1,Produce=1 --rest.laddr tcp://localhost:8745 --enable-preruntx=false --consensus-role=v2 --keyring-backend test  >/Users/oker/workspace/nodes/val2.log 2>&1 &")
        self.run_node("nohup exchaind start --home /Users/oker/workspace/nodes/node3/exchaind --p2p.seed_mode=false --p2p.allow_duplicate_ip --enable-dynamic-gp=false --enable-wtx=false --mempool.node_key_whitelist 0b066ca0790f27a6595560b23bf1a1193f100797,3813c7011932b18f27f172f0de2347871d27e852,6ea83a21a43c30a280a3139f6f23d737104b6975,bab6c32fa95f3a54ecb7d32869e32e85a25d2e08,testnet-node-ids --p2p.pex=false --p2p.addr_book_strict=false --p2p.seeds 0b066ca0790f27a6595560b23bf1a1193f100797@127.0.0.1:26656 --p2p.laddr tcp://127.0.0.1:26956 --rpc.laddr tcp://127.0.0.1:26957 --log_level main:info,*:error,consensus:error,state:info,distr:debug,gov:debug,staking:debug --chain-id exchain-67 --upload-delta=false --enable-gid --consensus.timeout_commit 1000ms --enable-blockpart-ack=false --block-part-size 16 --block-compress-type 0 --block-compress-flag 0 --block-compress-threshold 512 --append-pid=true --elapsed DeliverTxs=0,Round=1,CommitRound=1,Produce=1 --rest.laddr tcp://localhost:8845 --enable-preruntx=false --consensus-role=v3 --keyring-backend test >/Users/oker/workspace/nodes/val3.log 2>&1 &")
        self.run_node("nohup exchaind start --home /Users/oker/workspace/nodes/node4/exchaind --p2p.seed_mode=false --p2p.allow_duplicate_ip --enable-dynamic-gp=false --enable-wtx=false --mempool.node_key_whitelist 0b066ca0790f27a6595560b23bf1a1193f100797,3813c7011932b18f27f172f0de2347871d27e852,6ea83a21a43c30a280a3139f6f23d737104b6975,bab6c32fa95f3a54ecb7d32869e32e85a25d2e08,testnet-node-ids --p2p.pex=false --p2p.addr_book_strict=false --p2p.seeds 0b066ca0790f27a6595560b23bf1a1193f100797@127.0.0.1:26656 --p2p.laddr tcp://127.0.0.1:27056 --rpc.laddr tcp://127.0.0.1:27057 --log_level main:info,*:error,consensus:error,state:info,distr:debug,gov:debug,staking:debug --chain-id exchain-67 --upload-delta=false --enable-gid --consensus.timeout_commit 1000ms --enable-blockpart-ack=false --block-part-size 16 --block-compress-type 0 --block-compress-flag 0 --block-compress-threshold 512 --append-pid=true --elapsed DeliverTxs=0,Round=1,CommitRound=1,Produce=1 --rest.laddr tcp://localhost:8945 --enable-preruntx=false --consensus-role=v4 --keyring-backend test >/Users/oker/workspace/nodes/val4.log 2>&1 &")

    def run_node(self, cmd):
        result = os.popen(cmd).read()
        logging.info("result, cmd:" + cmd + ", result:" + result)

    def deposit(self, token, from_name):
        cmd = "exchaincli tx staking deposit " + str(token) + "okt --from " + from_name + " --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y"
        return self.run_tx(cmd)

    def add_shares(self, vals, from_name):
        cmd = "exchaincli tx staking add-shares " + vals + " --from " + from_name + " --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y"
        return self.run_tx(cmd)

    def transfer(self, from_name, to_name, tokens):
        cmd = "exchaincli tx send " + from_name + " " + to_name + " " + str(tokens) + "okt --from " + from_name + " --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y"
        return self.run_tx(cmd)

    def proxy_reg(self, from_name):
        cmd = "exchaincli tx staking proxy reg --from " + from_name + " --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y"
        return self.run_tx(cmd)

    def proxy_bind(self, proxy, from_name):
        cmd = "exchaincli tx staking proxy bind "+ proxy +" --from " + from_name + " --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y"
        return self.run_tx(cmd)

    def submit_change_type_proposal_offchain(self, from_name):
        cmd = "exchaincli tx gov submit-proposal change-distr-type proposal-change-distr-type-0.json --from " + from_name + " --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y"
        return self.run_tx(cmd)

    def submit_change_type_proposal_onchain(self, from_name):
        cmd = "exchaincli tx gov submit-proposal change-distr-type proposal-change-distr-type-1.json --from " + from_name + " --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y"
        return self.run_tx(cmd)

    def vote(self, from_name, num):
        cmd = "exchaincli tx gov vote " + str(num) + " yes --from " + from_name + " --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y"
        return self.run_tx(cmd)

    def withdraw_commission(self, val, from_name):
        cmd = "exchaincli tx distr withdraw-rewards " + val + " --commission --from " + from_name + " --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y"
        return self.run_tx(cmd)

    def withdraw_rewards(self, val, from_name):
        cmd = "exchaincli tx distr withdraw-rewards " + val + " --from " + from_name + " --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y"
        return self.run_tx(cmd)

    def withdraw_all_rewards(self, from_name):
        cmd = "exchaincli tx distr withdraw-all-rewards --from " + from_name + " --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y"
        return self.run_tx(cmd)

    def create_validator(self, from_name):
        cmd = 'exchaincli tx staking create-validator --pubkey=$(exchaind tendermint show-validator) --moniker="zzzzzzzz" --from ' + from_name + ' --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y'
        return self.run_tx(cmd)
    
    def edit_validator(self, rate, from_name):
        cmd = "exchaincli tx staking edit-validator-commission-rate " + str(rate) + " --from " + from_name + " --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y"
        return self.run_tx(cmd)
    
    def destroy_validator(self, from_name):
        cmd = "exchaincli tx staking destroy-validator --from " + from_name + " --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y"
        return self.run_tx(cmd)

    def query_validator(self, validator):
        cmd = " exchaincli query staking validator " + validator
        result = os.popen(cmd).read()
        logging.info("result, cmd:" + cmd + ", result:" + result)

        result_obj = json.loads(result)

        return result_obj

    def query_shares(self, delegator):
        cmd = " exchaincli query staking delegator " + delegator
        result = os.popen(cmd).read()
        logging.info("result, cmd:" + cmd + ", result:" + result)

        result_obj = json.loads(result)

        return result_obj

    def query_account(self, address):
        cmd = " exchaincli query account  " + address
        result = os.popen(cmd).read()
        logging.info("result, cmd:" + cmd + ", , result:" + result)

        result_obj = json.loads(result)

        return result_obj["value"]["coins"][0]["amount"]

    def query_commission(self, address):
        cmd = " exchaincli query distr commission   " + address
        result = os.popen(cmd).read()
        logging.info("result, cmd:" + cmd + ", result:" + result)

        result_obj = json.loads(result)

        return result_obj[0]["amount"]

    def query_rewards(self, delegator, validator):
        cmd = " exchaincli query distr rewards   " + delegator +  " " + validator
        result = os.popen(cmd).read()
        logging.info("result, cmd:" + cmd + ", result:" + result)

        try:
            result_obj = json.loads(result)
            return result_obj
        except:
            return -1

    def query_withdraw(self, address):
        cmd = " exchaincli query distr withdraw-addr   " + address
        result = os.popen(cmd).read()
        logging.info("result, cmd:" + cmd + ", result:" + result)

        return result

    def query_staking_validators(self):
        cmd = " exchaincli query staking validators   "
        result = os.popen(cmd).read()
        logging.info("result, cmd:" + cmd + ", result:" + result)
        result_obj = json.loads(result)
        return result_obj

    def query_proposal(self, num):
        cmd = " exchaincli query gov proposal   " + str(num)
        result = os.popen(cmd).read()
        logging.info("result, cmd:" + cmd + ", result:" + result)

        result_obj = json.loads(result)

        return result_obj
    
    def query_outstanding(self, address):
        cmd = " exchaincli query distr outstanding-rewards   " + address
        result = os.popen(cmd).read()
        logging.info("result, cmd:" + cmd + ", result:" + result)
        try:
            result_obj = json.loads(result)
        except:
            return -1

        return result_obj[0]["amount"]

    def query_distr_params(self):
        cmd = " exchaincli query distr params   "
        result = os.popen(cmd).read()
        logging.info("result, cmd:" + cmd + ", result:" + result)

        result_obj = json.loads(result)

        return result_obj

    def run_cmd(self, cmd):
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

    def query_tx(self, tx, delay_seconds = 10):
        for i in range(1, delay_seconds):
            cmd = " exchaincli query tx " + tx
            result = os.popen(cmd).read()
            try:
                result_obj = json.loads(result)
                if "gas_used" in result_obj:
                    #logging.info("result, cmd:" + cmd + ", result:" + result)
                    break
            except:
                logging.info("result, cmd:" + cmd + ", result:" + result)
            time.sleep(1)

    def set_withdraw_addr(self, new_addr, from_name):
        cmd = "exchaincli tx distr set-withdraw-addr " + new_addr + " --from " + from_name + " --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y"
        return self.run_tx(cmd)

    def withdraw(self, amount, from_name):
        cmd = "exchaincli tx staking withdraw " + str(amount) + "okt --from " + from_name + " --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y"
        return self.run_tx(cmd)

    def unreg(self, from_name):
        cmd = "exchaincli tx staking  proxy unreg --from " + from_name + " --gas auto --gas-prices 0.0000000001okt --gas-adjustment 1.3 -y"
        return self.run_tx(cmd)


