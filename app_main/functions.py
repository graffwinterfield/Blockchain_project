import json
import fitz
import time, hashlib
from web3 import Web3, HTTPProvider
from app_main import db
from models import Block_txn, Orders, User, Cars, Contracts
from sqlalchemy import desc
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from flask import url_for

try:
    w3 = Web3(HTTPProvider('http://localhost:9000'))
except Exception as e:
    print(e)


class save_to_db():
    def __init__(self, data):
        self.data = data
        db.session.add(data)
        db.session.commit()

    def show_db(self):
        data = self.data.txn
        row = Block_txn.query.filter_by(txn=data).first()

        return row.txn


class PrivatePublicKey():
    def __init__(self):
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )

    def private_pem_key(self):
        private_pem = self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        return private_pem.decode()

    def public_pem_key(self):
        public_key = self.private_key.public_key()

        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return public_pem.decode()


class Block():
    def __init__(self):
        first_block = Block_txn.query.order_by(desc(Block_txn.id)).all()
        if first_block == []:
            block = Block_txn(txn=self.create_genesis_block())
            f = save_to_db(data=block).show_db()
            print(f"транзакция {f['hash']} сохранена")

    # Генерация хеша для блока
    def calculate_hash(self, index, previous_hash, timestamp, data):
        value = str(index) + str(previous_hash) + str(timestamp) + str(data)
        return hashlib.sha256(value.encode('utf-8')).hexdigest()

    # Создание генезис-блока
    def create_genesis_block(self):
        return {
            'index': 1,
            'timestamp': time.time(),
            'data': 'Genesis Block',
            'previous_hash': '0',
            'hash': self.calculate_hash(1, '0', time.time(), 'Genesis Block')
        }

    # Создание нового блока
    def create_new_block(self, data, user_id):
        previous_block = db.session.query(Block_txn).order_by(Block_txn.id.desc()).first()
        previous_block = previous_block.txn
        index = previous_block['index'] + 1
        user = User.query.get(user_id)
        new_block = {
            'index': index,
            'data': data,

        }
        new_block = Block_txn(user=user, txn=new_block)
        f = save_to_db(data=new_block).show_db()
        print(f"транзакция {f} сохранена")
        return new_block

    def show_blocks(self, user_id):
        try:
            user = User.query.get(user_id)
            print(user)
            if user.transactions != []:
                return [block.txn for block in user.transactions]
            else:
                return None
        except Exception as e:
            print(e)

    def show_block(self, user_id, txn_id):
        try:
            txn = Block_txn.query.filter_by(id=txn_id, user_id=user_id).first()
            print(txn)
            return txn
        except Exception:
            return None

    def search_hash(self, hash_to_search):
        blocks = Block_txn.query.order_by().all()
        found = None
        for block in blocks:
            if block.txn['hash'] == hash_to_search:
                found = block.txn
        return found


class Settings():
    def __init__(self):
        with open('config/contracts_abi.json', 'r') as f:
            data = f.read()
        self.contracts = json.loads(data)

    def contract_load(self, address):
        abi = self.contracts.get(address)
        contract = w3.eth.contract(address=w3.toChecksumAddress(address), abi=abi)
        return contract


class Bank_manage():
    def __init__(self):
        self.orders = Orders.query.order_by().all()

    def create_order(self, data, user_id):
        name_from = data['name_from']
        description = data['description']
        amount = data['amount']
        car_id = data['car_id']
        orders = Orders.query.order_by(Orders.id).all()
        if orders:
            max_id_order = max(order.id for order in orders)
            id_order = max_id_order + 1
        else:
            id_order = 1
        if name_from and description and amount:
            order_info = {'id_order': id_order, 'car_id': car_id, 'name_from': name_from, 'description': description,
                          'amount': amount,
                          'permission': None}
            user = User.query.get(user_id)
            data = Orders(order_info=order_info, user=user)
            save_to_db(data=data)
            return order_info

    def list_orders(self):
        return [order.order_info for order in self.orders]

    def get_order(self, order_id):
        try:
            order = self.orders[order_id - 1].order_info
            return order
        except IndexError:
            return None

    def give_permission(self, user_id, order_id):
        print(order_id)
        order = Orders.query.get(order_id)
        print(order)
        if order:
            data = order.order_info
            data['permission'] = True
            db.session.query(Orders).filter_by(id=order_id, user_id=user_id).update({"order_info": data})
            # order.order_info['permission'] = True
            db.session.commit()
        print(self.orders)

    def denied_order(self, order_id):
        order = Orders.query.get(order_id)
        if order:
            data = order.order_info
            data['permission'] = False
            db.session.query(Orders).filter_by(id=order_id).update({"order_info": data})
            # order.order_info['permission'] = False
            db.session.commit()


class User_orders():
    def get_orders(self, user_id):
        user = User.query.get(user_id)
        if user.orders != []:
            return [order.order_info for order in user.orders]
        else:
            return None

    def get_order(self, user_id, order_id):
        try:
            order = Orders.query.filter_by(id=order_id, user_id=user_id).first()
            print(order)
            return order.order_info
        except Exception:
            return None

    def create_order_contract(self, user_id, email, replacements):
        print(user_id, email, type(user_id), type(email))
        doc = fitz.open("C:\\Users\\graff\\Desktop\\Blockchain_proj\\car.pdf")
        metadata = doc.metadata
        print(metadata)
        page = doc[0]
        for word in page.get_text("words", sort=False):
            for key, value in replacements.items():
                print(word)
                if word[4] == key:
                    print(word[4], word[:4])
                    rect = fitz.Rect(word[:4])
                    page.add_redact_annot(rect, '')  # create redaction for text
                    page.apply_redactions()
                    page.insert_text(rect.bl - (0, 3), value, fontname='Arial',
                                     fontfile='C:\\Windows\\Fonts\\ariali.ttf',
                                     fontsize=7.5)
        output_file = hashlib.sha256((email + str(user_id)).encode('utf-8')).hexdigest() + '.pdf'
        path = f'static/crypto-master/img/documents/{output_file}'
        doc.save(path)
        path_to_save = f'crypto-master/img/documents/{output_file}'
        add_contract = Contracts(user_id=user_id, path=path_to_save)
        save_to_db(add_contract)
        return output_file

    def load_file(self, contract_id, user_id):
        contract_data = Contracts.query.filter_by(id=contract_id, user_id=user_id).first()
        return contract_data


class Car_manage:
    def show_cars(self):
        cars = Cars.query.order_by().all()
        if cars == None:
            return None
        return cars

    def get_car(self, car_id):
        car = Cars.query.filter_by(id=car_id).first()
        print(car.id)
        if car == None:
            return None
        else:
            data = {'id': car.id, 'mark': car.mark, 'year': car.year, 'color': car.color, 'price': car.price,
                    'image': url_for('static', filename=car.image)}
        return data
