import requests
from web3 import Web3, HTTPProvider
from flask import Flask, render_template, request, jsonify
from app_main.functions import Block, Settings, Bank_manage, User_orders, save_to_db, Car_manage
from app_main import db, create_app
from models import User, Role
from flask import redirect, url_for, render_template, request, flash
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app_main.views import admin_required
from werkzeug.utils import secure_filename
import os, re

try:
    w3 = Web3(HTTPProvider('http://localhost:9000'))
    if w3.isConnected():
        print('Подключен к ноде: http://127.0.0.1:9000')
        settings = Settings()
        contract_ = settings.contract_load(address='0x8438Ad1C834623CfF278AB6829a248E37C2D7E3f')
except Exception as e:
    print(e)
app = create_app()
cars = Car_manage()


@app.route('/', methods=['GET'])
def index():
    return render_template('site/index.html')


@app.route('/logout/', methods=['GET'])
def logout():
    logout_user()
    flash('logged out')
    return redirect(url_for('index'))


@app.route('/orders/', methods=['GET'])
@login_required
def orders():
    user_id = current_user.id
    user_orders = User_orders()
    orders = user_orders.get_orders(user_id=user_id)
    if orders == None:
        flash('Заказов еще нет')
    return jsonify({'orders': orders})


@app.route('/transactions/', methods=['GET'])
@login_required
def transactions():
    user_id = current_user.id
    blockchain = Block()
    blocks = blockchain.show_blocks(user_id=user_id)
    if blocks == None:
        flash('Транзакций еще нет')
    return jsonify({'blocks': blocks})


@app.route('/account/', methods=['GET', 'POST'])
@login_required
def account():
    user_id = current_user.id
    user_orders = User_orders()
    blockhain = Block()
    orders = user_orders.get_orders(user_id=user_id)
    blocks = blockhain.show_blocks(user_id=user_id)
    print(blocks)
    print(orders)
    if orders == None:
        flash('Заказов еще нет')
    if blocks == None:
        flash('Транзакций еще нет')
    print(orders)
    # orders = [order_id['id_order'] for order_id in bank.orders if [order_id][0]['id_order'] != 0]
    return render_template('site/accounts.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        if email and password:
            user = User.query.filter_by(email=email).first()
            if not user or not check_password_hash(user.password, password):
                flash('wrong login or password')
                return redirect(url_for('login'))
            else:
                if user.has_role('admin'):
                    login_user(user, remember=remember)
                    return redirect(url_for('admin.admin_main'))
                else:
                    # Перенаправляем обычного пользователя на его аккаунт
                    if user.verification == None:
                        flash('Верификация еще не прошла подождите')
                    elif user.verification == True:
                        flash('Верификация подтверждена')
                        flash(f'logged in {user.username}')
                        login_user(user, remember=remember)
                        return redirect(url_for('account'))  # Замените это на URL страницы пользователя
                    else:
                        flash('Верификация не прошла попробуйте еще раз')

        else:
            flash('Fill all form')
    return render_template('site/login.html', legend='Авторизация')


@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        passport_seria = request.form.get('passport_seria')
        passport_number = request.form.get('passport_number')
        print(request.files)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            parts = os.path.splitext(file.filename)
            filename = parts[0] + str(os.urandom(20).hex())
            full_name = filename + parts[1]
            filename = secure_filename(full_name)

            file.save(os.path.join('static/crypto-master/img/passports/', filename))
            passport_image = 'crypto-master/img/passports/' + filename
        if username and email and password:
            user = User.query.filter_by(email=email).first()
            if user:
                flash('already exists')
                return redirect(url_for('signup'))
            admin_role = Role.query.filter_by(name='admin').first()
            user_role = Role.query.filter_by(name='user').first()
            if not (admin_role and user_role):
                admin_role = Role(name='admin', description='Администратор')
                user_role = Role(name='user', description='Пользователь')
                db.session.add(admin_role)
                db.session.add(user_role)
            roles = [user_role]
            password_hash = generate_password_hash(password, method='sha256')
            date = datetime.utcnow()
            user = User(username=username, email=email, password=password_hash, passport_number=passport_number,
                        passport_seria=passport_seria, passport_image=passport_image, date=date, roles=roles)
            save_to_db(user)
            flash('account created!')
            return redirect(url_for('login'))
    return render_template('site/signup.html', legend='Регистрация')


@app.route('/make_request_to_bank/', methods=['GET', 'POST'])
@login_required
def request_bank():
    user_id = current_user.id
    bank = Bank_manage()
    print(request.form)
    name_from = request.form['name_from']
    amount = request.form['amount']
    description = request.form['description']
    data = {'name_from': name_from, 'description': description, 'amount': amount}
    bank.create_order(data=data, user_id=user_id)
    print(bank.orders)
    orders = [order_object.order_info['id_order'] for order_object in bank.orders]
    print(orders)
    return render_template('site/index_boot.html', orders=orders)


@app.route('/order/<int:order_id>', methods=['GET', 'POST'])
@login_required
def order_wait(order_id):
    user_id = current_user.id
    user_orders = User_orders()
    order = user_orders.get_order(user_id=user_id, order_id=order_id)
    if order == None:
        flash('Заявка не найдена!')
        return redirect(url_for('account'))
    return render_template('site/account.html', order=order)


@app.route('/transaction/<int:txn_id>', methods=['GET', 'POST'])
def transaction_get(txn_id):
    user_id = current_user.id
    user_txns = Block()
    block = user_txns.show_block(user_id=user_id, txn_id=txn_id)
    print(block.txn)
    if block == None:
        flash('Транзакция не найдена!')
        return redirect(url_for('account'))
    return jsonify({'block': block.txn})


@app.route('/load_cars/', methods=['GET'])
def car_show():
    data = cars.show_cars()
    data_send = []
    for i in data:
        print(i.id, i.image)
        data = \
            {
                'id': i.id,
                'image': url_for('static', filename=f'{i.image}'),
                'mark': i.mark,
                'year': i.year,
                'color': i.color,
                'price': i.price
            }
        data_send.append(data)
    print(data_send)
    return jsonify(data_send)


@app.route('/add_car/<int:car_id>', methods=['GET', 'POST'])
def add_car(car_id):
    print('car_id', car_id)
    user_id = current_user.id
    bank = Bank_manage()
    print(request.form)
    car = cars.get_car(car_id=car_id)
    name_from = request.form['name_from']
    print(car)
    amount = car['price']
    description = [{'year': car['year']}, {'color': car['color']}]
    data = {'name_from': name_from, 'car_id': car_id, 'description': description, 'amount': amount}
    bank.create_order(data=data, user_id=user_id)
    car_price = amount
    car_price_float = ''
    for i in car_price.split(' '):
        car_price_float += i
    print(car_price_float)
    url = f'https://pro-api.coinmarketcap.com/v2/tools/price-conversion?symbol=rub&amount={float(car_price_float)}&convert=eth&CMC_PRO_API_KEY=89dad177-138d-4989-96ae-54daa3ab028d'
    r = requests.get(url)
    print(r.json())
    print(r.json()['data'][0]['quote']['ETH']['price'])
    eth_price = r.json()['data'][0]['quote']['ETH']['price']
    user_wallet_addr = w3.toChecksumAddress(data['name_from'])
    contract_.functions.getSender(user_wallet_addr).transact({'from': user_wallet_addr})
    contract_.functions.setAmount(w3.toWei(eth_price, 'ether')).transact({'from': user_wallet_addr})
    contract_.functions.setMonthlyInstallment().transact({'from': user_wallet_addr})
    print(bank.orders)
    orders = [order_object.order_info['id_order'] for order_object in bank.orders]
    print(orders)
    return render_template('site/index_boot.html', orders=orders)


@app.route('/bank_admin/', methods=['GET', 'POST'])
@admin_required
def list_orders():
    users = User.query.order_by(User.id).all()
    users_data = []
    for user in users:
        users_data.append({'id': user.id, 'email': user.email, 'passport_image': user.passport_image,
                           'passport_seria': user.passport_seria, 'passport_number': user.passport_number,
                           'verification': user.verification})
    return render_template('admin/bank_verification.html', users_data=users_data)


@app.route('/get_payment/<int:order_id>', methods=['GET', 'POST'])
@login_required
def payment(order_id):
    user = User_orders()
    data = user.get_order(user_id=current_user.id, order_id=order_id)
    if data == None:
        contract_data = None
    else:
        car_price = data['amount']
        car_price_float = ''
        for i in car_price.split(' '):
            car_price_float += i
        print(car_price_float)
        url = f'https://pro-api.coinmarketcap.com/v2/tools/price-conversion?symbol=rub&amount={float(car_price_float)}&convert=eth&CMC_PRO_API_KEY=89dad177-138d-4989-96ae-54daa3ab028d'
        r = requests.get(url)
        print(r.json()['data'][0]['quote']['ETH']['price'])
        eth_price = r.json()['data'][0]['quote']['ETH']['price']
        user_wallet_addr = w3.toChecksumAddress(data['name_from'])
        fixed_amount = contract_.functions.get_monthlyInstallment().call({'from': user_wallet_addr})
        payed_success = contract_.functions.get_payed_success().call({'from': user_wallet_addr})
        total_paid = contract_.functions.get_total_paid().call({'from': user_wallet_addr})
        print(contract_.functions.purchasePrice(user_wallet_addr).call())
        print(contract_.functions.get_markupAmount().call())
        markup_amount = contract_.functions.get_markupAmount().call({'from': user_wallet_addr})
        total_markup = markup_amount + contract_.functions.purchasePrice(user_wallet_addr).call()
        total_left = total_markup - total_paid
        if fixed_amount >= total_left:
            print('Превышение')
            fixed_amount = total_left
        print(total_paid, total_markup, total_left)
        car_id = data['car_id']
        data_car = cars.get_car(car_id=car_id)
        print(data_car)
        if fixed_amount <= 0:
            fixed_amount = 0
        else:
            fixed_amount = w3.fromWei(fixed_amount, 'ether')
        if total_left <= 0:
            total_left = 0
        else:
            total_left = w3.fromWei(total_left, 'ether')
        contract_data = {'fixed_amount': fixed_amount,
                         'address': user_wallet_addr,
                         'total_left': total_left,
                         'total_paid': w3.fromWei(total_paid, 'ether'),
                         'total_markup': w3.fromWei(total_markup, 'ether'),
                         'markup_amount': w3.fromWei(markup_amount, 'ether'),
                         'payed_success': payed_success,
                         'car_price': car_price,
                         'eth_price': round(eth_price, 2),
                         'data_car': data_car
                         }
    return jsonify({'contract_data': contract_data})


@app.route('/contract_submit/<int:order_id>', methods=['GET', 'POST'])
@login_required
def submit_contract(order_id):
    blockchain = Block()
    user = User_orders()
    user_data = User.query.filter_by(id=current_user.id).first()
    data = user.get_order(user_id=current_user.id, order_id=order_id)
    if data == None:
        contract_data = None
    else:
        print(data)
        car_price = data['amount']
        car_price_float = ''
        for i in car_price.split(' '):
            car_price_float += i
        print(car_price_float)
        url = f'https://pro-api.coinmarketcap.com/v2/tools/price-conversion?symbol=rub&amount={float(car_price_float)}&convert=eth&CMC_PRO_API_KEY=89dad177-138d-4989-96ae-54daa3ab028d'
        r = requests.get(url)
        print(r.json())
        print(r.json()['data'][0]['quote']['ETH']['price'])
        eth_price = r.json()['data'][0]['quote']['ETH']['price']
        user_wallet_addr = w3.toChecksumAddress(data['name_from'])
        contract_.functions.getSender(user_wallet_addr).transact({'from': user_wallet_addr})
        contract_.functions.setAmount(w3.toWei(eth_price, 'ether')).transact({'from': user_wallet_addr})
        contract_.functions.setMonthlyInstallment().transact({'from': user_wallet_addr})
        fixed_amount = contract_.functions.get_monthlyInstallment().call({'from': user_wallet_addr})
        payed_success = contract_.functions.get_payed_success().call({'from': user_wallet_addr})
        total_paid = contract_.functions.get_total_paid().call({'from': user_wallet_addr})
        total_markup = contract_.functions.get_markupAmount().call(
            {'from': user_wallet_addr}) + contract_.functions.purchasePrice(user_wallet_addr).call()
        total_left = total_markup - total_paid
        markup_amount = contract_.functions.get_markupAmount().call({'from': user_wallet_addr})
        if fixed_amount >= total_left:
            print('Превышение')
            fixed_amount = total_left

        if payed_success == True:
            Bank_manage().give_permission(user_id=current_user.id, order_id=order_id)
            order = user.get_order(user_id=current_user.id, order_id=order_id)
            car_id = order['car_id']
            car_info = cars.get_car(car_id=car_id)
            year = car_info['year']
            mark = car_info['mark']
            price = car_info['price']
            email = user_data.email
            user_id = user_data.id
            passport_seria = user_data.passport_seria
            passport_number = user_data.passport_number
            replacements = {
                'date': '12',
                'year': '2012',
                'passportdate': '12.12.2022',
                'seria': str(passport_seria),
                'number': str(passport_number),
                'address,': 'Новинский бульвар',
                'car': mark,
                'vin': '722',
                'type': 'Легковая',
                'category': 'легковая машина',
                'year_of_car': year,
                'price': price
            }
            print(car_info)
            user.create_order_contract(user_id=user_id, email=email, replacements=replacements)

        print(payed_success)
        try:
            if request.method == 'POST':
                data_hash = request.json
                total_markup -= total_paid
                print(total_markup)
                print(data_hash)
                hash = data_hash['hash']['transactionHash']
                print(hash)
                info = w3.eth.getTransaction(hash)
                print(info)
                print(data['permission'])
            if data['permission'] == True:
                print('Confirmed')

        except Exception as e:
            print(e)
        print(fixed_amount)
        if total_left <= 0:
            total_left = 0
        else:
            total_left = w3.fromWei(total_left, 'ether')

        if fixed_amount <= 0:
            fixed_amount = 0
        else:
            fixed_amount = w3.fromWei(fixed_amount, 'ether')
        contract_data = {'fixed_amount': fixed_amount,
                         'address': user_wallet_addr,
                         'total_left': total_left,
                         'total_paid': w3.fromWei(total_paid, 'ether'),
                         'total_markup': w3.fromWei(total_markup, 'ether'),
                         'markup_amount': w3.fromWei(markup_amount, 'ether'),
                         'payed_success': payed_success, 'car_price': car_price, 'eth_price': round(eth_price, 2)}
    return render_template('site/orders_list.html', contract_data=contract_data)


@app.route('/load_contract/<int:contract_id>')
def load_contract(contract_id):
    user = User_orders()
    user_id = current_user.id
    contract_data = user.load_file(contract_id=contract_id, user_id=user_id)
    print(contract_data.path)
    return jsonify({'path': url_for('static', filename=contract_data.path)})


@app.route('/create_txn/<int:txn_id>', methods=['POST'])
def create_txn(txn_id):
    blockchain = Block()
    user_id = current_user.id
    data = request.json
    print(data)
    blockchain.create_new_block(data=data, user_id=user_id)
    return render_template('site/orders_list.html')


@app.route('/submit/<int:user_id>', methods=['POST'])
def submit(user_id):
    user = User.query.filter_by(id=user_id).first()
    access = request.values.get('my_boolean')
    print(type(access))
    if access == 'True':
        user.verification = True
    elif access == 'False':
        user.verification = False
    db.session.commit()
    users = User.query.order_by(User.id).all()
    users_data = []
    for user in users:
        users_data.append({'id': user.id, 'email': user.email, 'passport_image': user.passport_image,
                           'passport_seria': user.passport_seria, 'passport_number': user.passport_number,
                           'verification': user.verification})
    return render_template('admin/bank_verification.html', users_data=users_data)


@app.route('/search_hash/', methods=['POST', 'GET'])
@login_required
def get_txn_by_hash():
    blockchain = Block()
    found = None
    if request.method == 'POST':
        hash_to_search = request.form['hash']
        found = blockchain.search_hash(hash_to_search)
        print(found)
    return render_template('site/search.html', block=found)


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


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5654)
