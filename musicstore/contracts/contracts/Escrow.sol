// contracts/Escrow.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

contract Escrow {
    address public seller;
    address public buyer;
    uint public amount;
    bool public released = false;

    event Deposited(address indexed buyer, uint amount);
    event Released(address indexed seller, uint amount);
    event Canceled(address indexed buyer, uint amount);

    constructor(address _seller) {
        seller = _seller;
    }

    // Buyer deposits funds
    function deposit() external payable {
        require(msg.value > 0, "Deposit must be greater than zero");
        require(buyer == address(0), "Already funded");
        buyer = msg.sender;
        amount = msg.value;

        emit Deposited(buyer, msg.value);
    }

    // Buyer releases funds to the seller
    function releaseFunds() external {
        require(msg.sender == buyer, "Only buyer can release funds");
        require(!released, "Funds already released");
        released = true;

        payable(seller).transfer(amount);
        emit Released(seller, amount);
    }

    // Buyer cancels the escrow and retrieves funds
    function cancel() external {
        require(msg.sender == buyer, "Only buyer can cancel");
        require(!released, "Funds already released");

        uint refundAmount = amount;
        amount = 0;
        buyer = address(0);

        payable(msg.sender).transfer(refundAmount);
        emit Canceled(msg.sender, refundAmount);
    }

    // Fallback function to prevent accidental ETH transfers
    receive() external payable {
        revert("Direct payments not allowed");
    }
}
