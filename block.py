from web3 import Web3, HTTPProvider
from flask import Flask, render_template, request, jsonify
from functions import Block, Settings, Bank_manage, Auth

w3 = Web3(HTTPProvider('http://localhost:9000'))
if w3.isConnected():
    print('Подключен к ноде: http://127.0.0.1:9000')
app = Flask(__name__, template_folder='templates', static_folder="static")
settings = Settings()
blockchain = Block()
bank = Bank_manage()
auth = Auth()


@app.route('/index/', methods=['GET'])
def index():
    orders = [order_id['id_order'] for order_id in bank.orders if [order_id][0]['id_order'] != 0]
    print(orders)
    return render_template('index_boot.html', orders=orders)


@app.route('/bank_login/', methods=['GET'])
def get_admin():
    return render_template('login.html')


@app.route('/make_request_to_bank/', methods=['POST'])
def request_bank():
    print(request.form)
    name_from = request.form['name_from']
    amount = request.form['amount']
    name_to = request.form['name_to']
    print(name_to, name_from, amount)
    data = {'name_from': name_from, 'name_to': name_to, 'amount': amount}
    bank.create_order(data=data)
    orders = [order_id['id_order'] for order_id in bank.orders if [order_id][0]['id_order'] != 0]
    print(orders)
    return render_template('index_boot.html', orders=orders)


hashes = []


@app.route('/order/<int:order_id>', methods=['GET', 'POST'])
def order_wait(order_id):
    print(order_id)
    data = bank.get_order(order_id)
    block = blockchain.show_block(order_id)
    print(block)
    contract_ = settings.contract_load(address='0xbCF26943C0197d2eE0E5D05c716Be60cc2761508')
    print(contract_.functions.get_monthlyInstallment().call())
    fixed_amount = contract_.functions.get_monthlyInstallment().call()
    total_paid = contract_.functions.get_total_paid().call()
    total_markup = contract_.functions.get_markupAmount().call()
    payed_success = contract_.functions.get_payed_success().call({'from': w3.toChecksumAddress(data['name_from'])})
    print(payed_success)

    try:
        print(request.method)
        if request.method == 'POST':
            data_hash = request.json
            total_markup -= total_paid
            print(total_markup)
            print(data_hash)
            hash = data_hash['hash']['transactionHash']
            print(hash)
            hashes.append(hash)
            info = w3.eth.getTransaction(hash)
            print(info)
            print(data['permission'])
        if data['permission'] == True:
            print('Confirmed')

    except Exception as e:

        print(e)
    contract_data = {'fixed_amount': fixed_amount, 'total_paid': total_paid, 'total_markup': total_markup,
                     'payed_success': payed_success}
    return render_template('orders_list.html', data=data, block=block, contract_data=contract_data, hash=hashes)


@app.route('/bank_admin/', methods=['POST'])
def list_orders():
    password = request.form['password']
    is_auth = auth.check_password(password)
    if is_auth == True:
        print('success admin')
        list_orders = bank.list_orders()
        ticket = auth.give_ticket()
        return render_template('bank_orders.html', data=list_orders, ticket=ticket)
    else:
        print('access denied')
        return 'Access denied'


@app.route('/submit/<string:ticket>/<int:order_id>', methods=['POST'])
def submit(ticket, order_id):
    print(ticket)
    if ticket == auth.give_ticket():
        value = request.form.get('my_boolean')
        if value == 'True':
            bank.give_permission(order_id)
            contract_ = settings.contract_load(address='0xbCF26943C0197d2eE0E5D05c716Be60cc2761508')
            print(contract_.abi)
            order = bank.get_order(order_id)
            addr_customer = order['name_from']
            description = order['name_to']
            amount = order['amount']
            print(addr_customer, description, amount)
            contract_.functions.finalizeAgreement(int(amount),
                                                  w3.toChecksumAddress(addr_customer)).transact(
                {'from': w3.toChecksumAddress('0x3C44CdDdB6a900fa2b585dd299e03d12FA4293BC'),
                 'value': w3.toWei(int(amount), 'ether')})

            blockchain.create_new_block(data=order)
    return render_template('bank_orders.html', data=bank.list_orders(), ticket=ticket)


@app.route('/search_hash/', methods=['POST'])
def search_hash():
    hash_to_search = request.form['hash']
    found = None
    for block in blockchain.chain:
        if block['hash'] == hash_to_search:
            found = block
    return render_template('search.html', block=found)


@app.route('/smart_contract_api/<string:address>', methods=['GET'])
def contract_api(address):
    try:
        contract = settings.contract_load(address)
        print(contract)
        functions = [func['name'] for func in contract.abi if func['type'] == 'function']
        print(functions)
    except Exception as e:
        print(e)
        functions = None
    return jsonify(functions)


@app.route('/smart_contract/', methods=['POST'])
def contract():
    address = request.form['contract']
    try:
        contract = settings.contract_load(address)
        functions = [func['name'] for func in contract.abi if func['type'] == 'function']
        print(functions)
    except Exception as e:
        print(e)
        functions = None
    return render_template('contract.html', data=functions)


app.run()
