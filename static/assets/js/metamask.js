
document.addEventListener('DOMContentLoaded', async function() {
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

            // Убираем обработчик для изменения amount, так как значение уже задано

            transactionForm.addEventListener('submit', async function(event) {
                event.preventDefault();
                const recipientAddress = document.getElementById('recipientAddress').value;
                const amount = parseFloat(document.getElementById('amount').value);
               await window.ethereum.enable();
                                const web3 = new Web3(window.ethereum, "any");

                         transactionForm.style.display = 'block';
                        // Получите адрес аккаунта кошелька
                        const accounts = await web3.eth.getAccounts();
                        const accountAddress = accounts[0];
                        const contractAddress = "0xbCF26943C0197d2eE0E5D05c716Be60cc2761508";
                        const contractABI = [

	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_purchasePrice",
				"type": "uint256"
			},
			{
				"internalType": "address",
				"name": "_customer",
				"type": "address"
			}
		],
		"name": "finalizeAgreement",
		"outputs": [],
		"stateMutability": "payable",
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
				"name": "_bank",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "_markupAmount",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_monthlyInstallment",
				"type": "uint256"
			}
		],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"inputs": [],
		"name": "withdrawAll",
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
		"name": "markupAmount",
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
		"inputs": [],
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
		"inputs": [],
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
	}

];
                        const contract = new web3.eth.Contract(contractABI, contractAddress);

                           if (accounts.length > 0) {

                        const gas = '21000'

                            const transaction = {
                                from: accountAddress,
                                to: recipientAddress,
                                value: web3.utils.toWei(amount.toString(),'ether'),
                                gas: gas
                            };
                            console.log(accountAddress)
                             try {
                             const hash = await contract.methods.pay().send({ from: accountAddress, value: web3.utils.toWei(amount.toString(),'ether') });


                            console.log(hash)
                            const data = {
                            recipient_address: recipientAddress,
                            amount: amount,
                            hash: hash
                        };
const currentUrl = window.location.href;

// Разделите URL-адрес по слешам и получите последний элемент
const urlParts = currentUrl.split('/');
const order_id = urlParts[urlParts.length - 1];

// order_id теперь содержит значение <int:order_id>
console.log(order_id);
                        const response = await fetch('/order/'+order_id, {
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