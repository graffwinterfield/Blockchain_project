function loadTransactions() {
    fetch('/transactions/')
        .then(response => response.json())
        .then(data => {
            const tbody = document.getElementById('transaction-table-body');
            const thead = document.querySelector('thead');
            const section = document.getElementById('section');
            const request = document.getElementById('request');

            tbody.innerHTML = '';
            section.innerHTML = '';
            thead.innerHTML = '';
            request.innerHTML = '';

            // Перебираем данные о транзакциях и создаем строки для каждой транзакции
            if (data.blocks) {
                const columns = document.createElement('tr');
                columns.innerHTML = `
                    <th scope="col">ID</th>
                    <th scope="col">Amount</th>
                    <th scope="col">Hash</th>
                    <th scope="col">Status</th>`;
                thead.appendChild(columns);
                const title = document.createElement('h2');
                title.innerHTML = `Transactions`;
                section.appendChild(title);

                data.blocks.forEach(block => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td><a href="#" data-transaction-id="${block.index}">#${block.index}</a></td>
                        <td>${JSON.stringify(block.data.amount)}</td>
                        <td>${block.data.hash.blockHash}</td>
                        <td style="color: ${block.data.hash.status === true ? 'green' : (block.data.hash.status === false ? 'red' : 'orange')}">
                            ${block.data.hash.status === true ? 'Подтвержденный' : (block.data.hash.status === false ? 'Отказано' : 'Ожидание')}`;
                    tbody.appendChild(row);

                    // Добавляем обработчик события клика на ссылку с data-атрибутом
                    const link = row.querySelector('a');
                    link.addEventListener('click', function(event) {
                        event.preventDefault();
                        const transactionId = link.getAttribute('data-transaction-id');
                        loadTransactionData(transactionId);
                    });
                });
            } else {
                const alert = document.createElement('tr');
                alert.innerHTML = `<h2 style="color:red">У вас нет транзакций</h2>`;
                tbody.appendChild(alert);
            }
        })
        .catch(error => {
            console.error('Ошибка при загрузке данных о транзакциях:', error);
        });
}

function request_to_bank() {

            const tbody = document.getElementById('transaction-table-body');
            const thead = document.querySelector('thead');
            const section = document.getElementById('section');
            const request = document.getElementById('request');

            tbody.innerHTML = '';
            section.innerHTML = '';
            thead.innerHTML = '';
            request.innerHTML = '';

            const form = document.createElement('form');
            form.action = "/make_request_to_bank/";
            form.method = "post";
            form.innerHTML = `
                <h1 class="h3 mb-3 fw-normal">Request to bank</h1>
                <div class="form-floating">
                    <input type="text" class="form-control" id="name_from" name="name_from" placeholder="0x">
                    <label for="name_from">from:</label>
                    <div class="form-floating">
                        <input type="number" class="form-control" id="amount" name="amount" placeholder="0x">
                        <label for="amount">amount:</label>
                    </div>
                </div>
                <label for="description">Описание проекта</label>
                <textarea id="description" name="description" rows="4" cols="50"></textarea>
                <button type="submit">request</button>`;
                 request.appendChild(form);

            }


function LoadOrders() {
    fetch('/orders/')
        .then(response => response.json())
        .then(data => {
            // Получение ссылки на tbody элемент таблицы
            const tbody = document.querySelector('table tbody');
            const thead = document.querySelector('thead');
            const section = document.getElementById('section');

            tbody.innerHTML = '';
            section.innerHTML = '';
            thead.innerHTML = '';
            request.innerHTML = '';

            // Перебираем данные о заказах и создаем строки для каждого заказа
            if (data.orders) {
            const columns = document.createElement('tr');
            columns.innerHTML = `
                        <th scope="col">ID</th>
                        <th scope="col">From</th>
                        <th scope="col">Description</th>
                        <th scope="col">Amount</th>
                        <th scope="col">Status</th>`;
            thead.appendChild(columns);
            const title = document.createElement('h2');
            title.innerHTML = `Orders`;
            section.appendChild(title);
                data.orders.forEach(order => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                     <td><a href="#" data-transaction-id="${order.id_order}">#${order.id_order}</a></td>
                        <td>${order.name_from}</td>
                        <td>${order.description}</td>
                        <td>${order.amount}</td>
                        <td style="color: ${order.permission === true ? 'green' : (order.permission === false ? 'red' : 'orange')}">
                            ${order.permission === true ? 'Подтвержденный' : (order.permission === false ? 'Отказано' : 'Ожидание')}`;
                    tbody.appendChild(row);
                     const link = row.querySelector('a');
                    link.addEventListener('click', function(event) {
                        event.preventDefault();
                        const order_id = link.getAttribute('data-transaction-id');
                        LoadOrderData(order_id);
                    });
                });

            }
            else {
            const alert = document.createElement('tr');
            alert.innerHTML = `<h2 style="color:red">У вас нет заказов</h2>`;
            tbody.appendChild(alert)
            }
        })
        .catch(error => {
            console.error('Ошибка при загрузке данных о заказах:', error);
        });
}

function LoadOrderData(order_id) {
    fetch(`/get_payment/${order_id}`)
        .then(response => response.json())
        .then(data => {

            const tbody = document.getElementById('transaction-table-body');
            const thead = document.querySelector('thead');
            const section = document.getElementById('section');
            const request = document.getElementById('request');

            tbody.innerHTML = '';
            section.innerHTML = '';
            thead.innerHTML = '';
            request.innerHTML = '';

            const title = document.createElement('h2');
            title.innerHTML = `Transaction ${order_id}`;
            section.appendChild(title);



            // Создаем таблицу
            const table = document.createElement('table');
            table.className = 'table table-striped';

            // Создаем строки таблицы для каждого поля данных
            const idRow = document.createElement('tr');
            const dataRow = document.createElement('tr');
            dataRow.innerHTML = `
                <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
                    <h2 id="section"></h2>
                    <div class="table-container table-responsive small" id="tableContainer">
                        <table class="table table-striped table-sm">
                            <thead>
                                <tr>
                                    <th scope="col"></th>
                                </tr>
                            </thead>
                            <tbody id="transaction-table-body">
                                <tr>
                                    <td>
                                        ${data.contract_data ? `
                                        <p>Всего оплачено: <span id="totalPaidValue">${data.contract_data.total_paid}</span></p>
                                         <p>адрес отправителя: <span id="address">${data.contract_data.address}</span></p>
                                        <p>Цена: <span id="price">${data.contract_data.eth_price} ETH </span></p>
                                          <p>Наценка: <span id="amount">${data.contract_data.markup_amount} ETH</span></p>
                                        <p>Задолжность: <span id="total_left">${data.contract_data.total_left} ETH</span></p>
                                        <form action="/contract_submit/${order_id}" method="POST">
                    <input type="hidden" name="pay">
                    <button type="submit" class='btn btn-primary'>Перейти к оплате</button>
                </form>

                ${data.contract_data.payed_success ? `<p>Оплата подтверждена!</p>` : ''}
                                        ` : `<p>Нет заявок.</p>`}
                                    </td>
                                    <td>
                                    <img src=${data.contract_data.data_car.image} width="300" height="200">
                                    <p>Цена: <span> ${data.contract_data.car_price} Р</span></p>
                                    <p>Марка ${data.contract_data.data_car.mark}</p>
                                    <p>Год ${data.contract_data.data_car.year} </p>
                                    <p>Цвет ${data.contract_data.data_car.color} </p>
                                    </td>

                                </tr>
                            </tbody>
                        </table>
                    </div>
                    <div class="table-container table-responsive small" id="request"></div>
                    </main>
                `;
            table.appendChild(dataRow);
            tbody.appendChild(table);

const backButton = document.createElement('button');
backButton.id = 'back-to-orders';
backButton.className = 'btn btn-primary';
backButton.innerText = 'Назад';

backButton.addEventListener('click', function() {
  event.preventDefault(); // Отмена отправки формы

    // Вернуться к списку транзакций
    LoadOrders();
});
            const form = document.querySelector('form'); // Замените на соответствующий селектор формы
            const submitButton = form.querySelector('button[type="submit"]'); // Замените на соответствующий селектор кнопки "Перейти к оплате"

// Вставить кнопку "Назад" перед кнопкой "Перейти к оплате"
form.insertBefore(backButton, submitButton);
});
}


// Функция для загрузки данных о выбранной транзакции
function loadTransactionData(transactionId) {
    fetch(`/transaction/${transactionId}`)
        .then(response => response.json())
        .then(data => {
            const tbody = document.getElementById('transaction-table-body');
            const thead = document.querySelector('thead');
            const section = document.getElementById('section');
            const request = document.getElementById('request');

            tbody.innerHTML = '';
            section.innerHTML = '';
            thead.innerHTML = '';
            request.innerHTML = '';

            const title = document.createElement('h2');
            title.innerHTML = `Transaction ${data.block.index}`;
            section.appendChild(title);

            const backButton = document.createElement('button');
            backButton.id = 'back-to-transactions';
            backButton.className = 'btn btn-primary';
            backButton.innerText = 'Назад';
            backButton.addEventListener('click', function() {
                // Вернуться к списку транзакций
                loadTransactions();
            });
            thead.appendChild(backButton);
             // Создаем таблицу
            const table = document.createElement('table');
            table.className = 'table table-striped';

            // Создаем строки таблицы для каждого поля данных
            const idRow = document.createElement('tr');
            const dataRow = document.createElement('tr');
            dataRow.innerHTML = `<td>Data</td><td>${JSON.stringify(data.block.data)}</td>`;
            const timestampRow = document.createElement('tr');
            timestampRow.innerHTML = `<td>Timestamp</td><td>${data.block.timestamp}</td>`;
            const hashRow = document.createElement('tr');
            hashRow.innerHTML = `<td>Hash</td><td>${data.block.hash}</td>`;
            const statusRow = document.createElement('tr');
            const statusColor = data.block.data.hash.status === true ? 'green' : (data.block.data.hash.status === false ? 'red' : 'orange');
            statusRow.innerHTML = `
                <td>Status</td>
                <td style="color: ${statusColor}">
                    ${data.block.data.hash.status === true ? 'Подтвержденный' : (data.block.data.hash.status === false ? 'Отказано' : 'Ожидание')}
                </td>`;

            // Добавляем строки в таблицу
            table.appendChild(idRow);
            table.appendChild(dataRow);
            table.appendChild(timestampRow);
            table.appendChild(hashRow);
            table.appendChild(statusRow);
            tbody.appendChild(table);


        });
}

function LoadCars() {
    fetch(`/load_cars/`)
        .then(response => response.json())
        .then(data_send => {
            const tbody = document.getElementById('transaction-table-body');
            const thead = document.querySelector('thead');
            const section = document.getElementById('section');
            const request = document.getElementById('request');

            tbody.innerHTML = '';
            section.innerHTML = '';
            thead.innerHTML = '';
            request.innerHTML = '';
            thead.innerHTML = `<thead>
                <tr>
                    <th>Машина</th>
                    <th>Описание</th>
                    <th>Цена</th>
                </tr>
            </thead>`;

            const title = document.createElement('div');
            const table = document.createElement('table');

            data_send.forEach(data => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>
                        <p>${data.id}</p>
                        <img src="${data.image}" width="300" height="200">
                        <p>${data.mark}</p>
                    </td>
                    <td>
                        <p>${data.year} ${data.color}</p>

                    </td>
                    <td> <p>${data.price} р</p>
                     <form action="/add_car/${data.id}" method="post">
                            <div class="form-floating">
                                <input type="text" class="form-control" id="name_from" name="name_from" placeholder="0x">
                                <label for="name_from">from:</label>
                            </div>
                            <button type="submit">request</button>
                        </form></td>
                `;

                tbody.appendChild(row);
            });

        });
}



function dashboard() {
            const tbody = document.getElementById('transaction-table-body');
            const thead = document.querySelector('thead');
            const section = document.getElementById('section');
            const request = document.getElementById('request');

            tbody.innerHTML = '';
            section.innerHTML = '';
            thead.innerHTML = '';
            request.innerHTML = '';
}

document.getElementById('load-transactions-button').addEventListener('click', loadTransactions);
document.getElementById('load-orders-button').addEventListener('click', LoadOrders);
document.getElementById('request_to_bank').addEventListener('click', request_to_bank);
document.getElementById('load_cars').addEventListener('click', LoadCars);