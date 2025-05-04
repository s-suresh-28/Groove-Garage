require("@nomicfoundation/hardhat-toolbox");

module.exports = {
    solidity: "0.8.28",

    networks: {
        localhost: {
            url: "http://127.0.0.1:7545", // Ganache RPC
            accounts: [
                "0x3403d940f004df748b830c4191e4364c770487fe411ba7ef6cddc262a3cf644a", // Replace with a valid Ganache private key
            ],
        },
    },
};
