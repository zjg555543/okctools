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

class WasmPress:
    def __init__(self, configObj):
        self.config = configObj
        self.okcli = rpc.OKCli("okbchaind", "okbchaincli", self.config["chainId"], self.config["rpc"])
        return

    def format_decimal(self, num):
        str_num = str(num)
        if "." in str_num:
            a, b = str(str_num).split('.')
            return int(a)
        else:
            return int(str_num)

    def auto(self):
        return

    def create_account(self):
        file = open('data/address.txt', 'w', encoding='UTF-8')
        loop_num = 100000
        for l in range(loop_num): 
            address = self.okcli.get_new_address()
            file.write(address + "\n")

        file.close()
        return

    def init(self):
        code_id = self.okcli.wasm_store("captain", "/Users/oker/workspace/github/wasm-test/contract/iterator-press/artifacts/iterator_press.wasm")
        logging.info(code_id)

        contract_address = self.okcli.wasm_instantiate("captain", code_id,  "{}", "0xbbE4733d85bc2b90682147779DA49caB38C0aA1F")
        
        file = open('data/address.txt', 'r', encoding='UTF-8')

        loop_num = 100
        for l in range(loop_num): 
            num = 100
            press_paras='{"add":{"spender":['
            for i in range(num): 
                address = file.readline().strip('\n')
                press_paras += '"'
                press_paras += address
                press_paras += '"'
                if i != num - 1 :
                    press_paras += ','

            press_paras += ']}}'
            logging.info(press_paras)

            self.okcli.wasm_execute("captain", contract_address, press_paras)

        file.close()
        self.okcli.wasm_query(contract_address, '{"get_total":{}}')
        logging.info(contract_address)

        return
    
    def press(self):
        contract_address = "0x76171b2B4fCDF61b3E5c70A86AD17b304f17740a"
        self.okcli.wasm_execute("captain", contract_address, '{"press":{"ascending":true}}')
        return 

if __name__ == '__main__':
    pybase = pybase.Pybase()
    strlist = os.path.basename(__file__).split('.') 
    file = open('config/' + strlist[0] + '.json', 'r', encoding='UTF-8')
    moduleConfig = json.loads(file.read())
    file.close()
    case = WasmPress(moduleConfig)

    opt = sys.argv[1]
    if opt == "auto":
        case.auto()
    if opt == "init":
        case.init()
    if opt == "press":
        case.press()
    if opt == "create_account":
        case.create_account()

