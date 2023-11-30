// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MurabahaContract {
    address public bank;
    address public customer;
    uint256 public markupprocent;
    uint256 public constant MONTHS_IN_YEAR = 12;
    mapping(address => bool) public agreementCompleted;
    mapping(address => bool) public payed_success;
    mapping(address => uint256) public totalPaid;
    mapping(address => uint256) public purchasePrice;
    mapping(address => uint256) public monthlyInstallment;

    constructor(address _bank, uint256 _markupprocent) {
        bank = _bank;
        markupprocent = _markupprocent;       
    
    }

    modifier onlyBank() {
        require(msg.sender == bank, "Only the bank can call this function");
        _;
    }

    modifier onlyCustomer() {
        require(msg.sender == customer, "Only the customer can call this function");
        _;
    }

    function setAmount(uint _Amount) public {
        purchasePrice[msg.sender] = _Amount;
    }

     function setMonthlyInstallment() public {
        monthlyInstallment[msg.sender] = (purchasePrice[msg.sender]*30)/100;
    }

    function getSender(address _customer) public  {
        customer = _customer;
    }

    function get_monthlyInstallment() public view returns (uint256) {
        return monthlyInstallment[msg.sender];

    }

    function get_total_paid() public view returns(uint256) {
        return totalPaid[msg.sender];
    }

    function get_markupAmount() public view returns(uint256){
        return (purchasePrice[msg.sender] * markupprocent)/100;
    }
   
    function get_payed_success() public view returns (bool){
        return payed_success[msg.sender];
    }
    function pay() external onlyCustomer payable {
        require(payed_success[msg.sender]==false, "You already payed markup");
        // Transfer funds to the bank
        address payable bankAddress = payable(bank);
        bankAddress.transfer(msg.value);
        totalPaid[msg.sender] += msg.value;
        if (totalPaid[msg.sender] >= purchasePrice[msg.sender]+(purchasePrice[msg.sender] * markupprocent)/100) {
            payed_success[msg.sender] = true;

            
        }
    }
    function withdrawAll() external onlyBank {
        address payable _myaddress = payable(bank);
        address this_contract = address(this);
        _myaddress.transfer(this_contract.balance);
        
    }
}