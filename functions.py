import json
import time, hashlib
from web3 import Web3, HTTPProvider

w3 = Web3(HTTPProvider('http://localhost:9000'))


class Block():
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    # Генерация хеша для блока
    def calculate_hash(self, index, previous_hash, timestamp, data):
        value = str(index) + str(previous_hash) + str(timestamp) + str(data)
        return hashlib.sha256(value.encode('utf-8')).hexdigest()

    # Создание генезис-блока
    def create_genesis_block(self):
        return {
            'index': 0,
            'timestamp': time.time(),
            'data': 'Genesis Block',
            'previous_hash': '0',
            'hash': self.calculate_hash(0, '0', time.time(), 'Genesis Block')
        }

    # Создание нового блока
    def create_new_block(self, data):
        previous_block = self.chain[-1]
        index = previous_block['index'] + 1
        timestamp = time.time()
        hash = self.calculate_hash(index, previous_block['hash'], timestamp, data)
        new_block = {
            'index': index,
            'timestamp': timestamp,
            'data': data,
            'previous_hash': previous_block['hash'],
            'hash': hash
        }
        self.chain.append(new_block)
        print(self.chain)
        return new_block

    def show_block(self, id):
        try:
            block = self.chain[id]
        except IndexError:
            block = None
        return block


class Settings():
    def __init__(self):
        with open('Blockchain_proj/contracts_abi.json', 'r') as f:
            data = f.read()
        self.contracts = json.loads(data)

    def contract_load(self, address):
        abi = self.contracts.get(address)
        contract = w3.eth.contract(address=w3.toChecksumAddress(address), abi=abi)
        return contract


class Bank_manage():
    def __init__(self):
        self.permission = False
        self.orders = [
            {'id_order': 0, 'name_from': None, 'name_to': None, 'amount': None, 'permission': self.permission}]

    def create_order(self, data):
        name_from = data['name_from']
        name_to = data['name_to']
        amount = data['amount']
        last_order_id = self.orders[-1]['id_order']
        last_order_id += 1
        new_txn = None
        if name_from and name_to and amount:
            new_txn = {'id_order': last_order_id, 'name_from': name_from, 'name_to': name_to, 'amount': amount,
                       'permission': self.permission}
            self.orders.append(new_txn)

        return new_txn

    def list_orders(self):
        return self.orders

    def get_order(self, order_id):
        try:
            order = self.orders[order_id]
            return order
        except IndexError:
            return None

    def give_permission(self, order_id):
        permission = True
        self.orders[order_id]['permission'] = permission
        return self.orders[order_id]


class Auth():
    def __init__(self):
        self.is_auth = False
        self.password_hash = 'daaad6e5604e8e17bd9f108d91e26afe6281dac8fda0091040a7a6d7bd9b43b5'

    def check_password(self, password):
        if hashlib.sha256(password.encode()).hexdigest() == self.password_hash:
            print(hashlib.sha256(password.encode()).hexdigest())
            is_auth = True
            return is_auth

        return self.is_auth

    def give_ticket(self):
        ticket = 'ticket' + self.password_hash
        print(hashlib.sha256(ticket.encode()).hexdigest())
        return hashlib.sha256(ticket.encode()).hexdigest()
