// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title JointAccountDApp
 * @dev A decentralized application that allows users to create joint accounts and transact through a network.
 */
contract JointAccountDApp {
    struct User {
        string username;
        bool registered;
    }

    struct Account {
        uint256 balance;
        mapping(uint256 => uint256) contributions; // Contributions from each user
    }

    mapping(uint256 => User) public users;
    mapping(uint256 => mapping(uint256 => Account)) public accounts;

    event UserRegistered(uint256 indexed userId, string username);
    event AccountCreated(uint256 indexed userId1, uint256 indexed userId2, uint256 balance);
    event AmountSent(uint256 indexed fromUserId, uint256 indexed toUserId, uint256 amount);
    event AccountClosed(uint256 indexed userId1, uint256 indexed userId2);

    /**
     * @dev Register a new user with a unique ID and username.
     */
    function registerUser(uint256 userId, string memory username) public {
        require(!users[userId].registered, "User already registered");
        users[userId] = User(username, true);
        emit UserRegistered(userId, username);
    }

    /**
     * @dev Create a joint account between two registered users.
     */
    function createAcc(uint256 userId1, uint256 userId2, uint256 initialContribution) public {
        require(users[userId1].registered && users[userId2].registered, "Users must be registered");
        require(accounts[userId1][userId2].balance == 0, "Account already exists");

        Account storage account = accounts[userId1][userId2];
        account.balance = initialContribution * 2;
        account.contributions[userId1] = initialContribution;
        account.contributions[userId2] = initialContribution;

        // Mirror the account
        accounts[userId2][userId1].balance = account.balance;
        accounts[userId2][userId1].contributions[userId1] = account.contributions[userId1];
        accounts[userId2][userId1].contributions[userId2] = account.contributions[userId2];

        emit AccountCreated(userId1, userId2, account.balance);
    }

    /**
     * @dev Send amount from one user to another along a specified path.
     */
    function sendAmount(uint256 fromUserId, uint256 toUserId, uint256 amount, uint256[] memory path) public {
        require(users[fromUserId].registered && users[toUserId].registered, "Users must be registered");
        require(path.length >= 2, "Invalid path");
        require(path[0] == fromUserId && path[path.length - 1] == toUserId, "Path must start and end with sender and receiver");

        // Check balances along the path
        for (uint256 i = 0; i < path.length - 1; i++) {
            uint256 sender = path[i];
            uint256 receiver = path[i + 1];

            Account storage account = accounts[sender][receiver];
            require(account.balance > 0, "Account does not exist between users");
            require(account.contributions[sender] >= amount, "Insufficient balance in account");

            // Update contributions
            account.contributions[sender] -= amount;
            account.contributions[receiver] += amount;

            // Mirror the account
            accounts[receiver][sender].balance = account.balance;
            accounts[receiver][sender].contributions[sender] = account.contributions[sender];
            accounts[receiver][sender].contributions[receiver] = account.contributions[receiver];
        }

        emit AmountSent(fromUserId, toUserId, amount);
    }

    /**
     * @dev Close the joint account between two users.
     */
    function closeAccount(uint256 userId1, uint256 userId2) public {
        require(accounts[userId1][userId2].balance > 0, "Account does not exist");

        delete accounts[userId1][userId2];
        delete accounts[userId2][userId1];

        emit AccountClosed(userId1, userId2);
    }

    /**
     * @dev Get the contribution of a user in an account.
     */
    function getContribution(uint256 userId1, uint256 userId2) public view returns (uint256) {
        return accounts[userId1][userId2].contributions[userId1];
    }
}
