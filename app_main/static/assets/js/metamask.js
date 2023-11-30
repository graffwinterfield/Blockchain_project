
document.addEventListener('DOMContentLoaded', async function() {
const currentUrl = window.location.href;
const urlParts = currentUrl.split('/');
const order_id = urlParts[urlParts.length - 1];
console.log(order_id);
const send_resp = await fetch('/get_payment/'+order_id, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: []
                        });
                        if (send_resp.ok) {
    const response_ = await send_resp.json();
    const totalPaidValue = document.getElementById('totalPaidValue');
    const total_left = document.getElementById('total_left');
    totalPaidValue.innerText = response_.contract_data.total_paid;
    total_left.innerText = response_.contract_data.total_left;
    const amount_set = document.getElementById('amount');
    amount_set.value = response_.contract_data.fixed_amount;
    const amount = parseFloat(document.getElementById('amount').value);

}
            const connectMetaMaskBtn = document.getElementById('connectMetaMaskBtn');
            const transactionForm = document.getElementById('transactionForm');
            connectMetaMaskBtn.addEventListener('click', async function() {
                await window.ethereum.request({
                method: 'wallet_switchEthereumChain',
                params: [{
                    chainId: '0x7a69'
                }], // chainId must be in hexadecimal numbers
            });
            accounts = await ethereum.request({
                method: 'eth_requestAccounts'
            });
            const chainId = await ethereum.request({
                method: 'eth_chainId'
            });

            if (chainId == '0x7a69') {
                myAddress = accounts[0];
                currentWalletAddress = accounts[0];
                provider = new Web3(window.ethereum, "any");
                  transactionForm.style.display = 'block';

            } else {
                $('#blockChainBSC').val('Please switch to BSC blockchain')
                $('#walletAddress').val(accounts[0]);
            }

            });
            transactionForm.addEventListener('submit', async function(event) {


                event.preventDefault();
                const currentUrl = window.location.href;
const urlParts = currentUrl.split('/');
const order_id = urlParts[urlParts.length - 1];
console.log(order_id);
const send_resp = await fetch('/get_payment/'+order_id, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: []
                        });
                        if (send_resp.ok) {
                const response = await send_resp.json();
            console.log(response);
                const recipientAddress = document.getElementById('recipientAddress').value;
                const amount_set = document.getElementById('amount');
                amount_set.value = response.contract_data.fixed_amount;
                const amount = parseFloat(document.getElementById('amount').value);
                console.log(amount);
                }
                const amount = document.getElementById('amount').value;
               await window.ethereum.enable();
                                const web3 = new Web3(window.ethereum, "any");

                         transactionForm.style.display = 'block';
                        // Получите адрес аккаунта кошелька
                        const accounts = await web3.eth.getAccounts();
                        const accountAddress = accounts[0];
                        const contractAddress = "0x663F3ad617193148711d28f5334eE4Ed07016602";
                        const contractABI = [
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_bank",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "_markupprocent",
				"type": "uint256"
			}
		],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"inputs": [],
		"name": "MONTHS_IN_YEAR",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "agreementCompleted",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "bank",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "customer",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_customer",
				"type": "address"
			}
		],
		"name": "getSender",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "get_markupAmount",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "get_monthlyInstallment",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "get_payed_success",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "get_total_paid",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "markupprocent",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "monthlyInstallment",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "pay",
		"outputs": [],
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "payed_success",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "purchasePrice",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_Amount",
				"type": "uint256"
			}
		],
		"name": "setAmount",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "setMonthlyInstallment",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "totalPaid",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "withdrawAll",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	}


];
console.log(amount);
console.log(web3.utils.toWei(amount.toString(),'ether'));
                        const contract = new web3.eth.Contract(contractABI, contractAddress);
                           if (accounts.length > 0) {
                        const gas = '21000'
                            const transaction = {
                                from: accountAddress,
                                to: recipientAddress,
                                value: web3.utils.toWei(amount.toString(),'ether'),
                                gas: gas
                            };
                             try {
                             const hash = await contract.methods.pay().send({ from: accountAddress, value: web3.utils.toWei(amount.toString(),'ether') });
                            console.log(hash)
                            const data = {
                            recipient_address: recipientAddress,
                            amount: amount,
                            hash: hash
                        };

                        const send_resp = await fetch('/get_payment/'+order_id, {
                                                method: 'POST',
                                                headers: {
                                                    'Content-Type': 'application/json'
                                                },
                                                body: []
                                            });
                                            if (send_resp.ok) {
                        const response_ = await send_resp.json();
                        const totalPaidValue = document.getElementById('totalPaidValue');
                        const total_left = document.getElementById('total_left');
                        totalPaidValue.innerText = response_.contract_data.total_paid;
                        total_left.innerText = response_.contract_data.total_left;
                        console.log(total_left);
                        }


                        const response = await fetch('/create_txn/'+order_id, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify(data)
                        });

                        const result = await response.json;
                            console.log('Transaction hash:', hash.transactionHash);
                            } catch (error) {
            console.error('Error sending transaction:', error);
                }
             }
            });
        });