// static/js/metamask.js

// Connect MetaMask and get user's wallet address
async function connectMetaMask() {
    if (typeof window.ethereum !== 'undefined') {
        try {
            const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
            alert("Connected to MetaMask: " + accounts[0]);

            // Save wallet address to session via Django endpoint
            await saveWalletAddress(accounts[0]);
        } catch (error) {
            alert("Error connecting to MetaMask: " + error.message);
        }
    } else {
        alert("MetaMask is not installed!");
    }
}

// Save wallet address to Django backend
async function saveWalletAddress(walletAddress) {
    try {
        const response = await fetch("/save_wallet/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ wallet_address: walletAddress }),
        });

        const data = await response.json();
        console.log("Wallet address saved:", data.message);
    } catch (error) {
        console.error("Error saving wallet address:", error);
    }
}

// Initialize escrow payment
async function initiateEscrow(sellerAddress, contractAddress, amount) {
    if (!window.ethereum) {
        alert("MetaMask not detected!");
        return;
    }

    try {
        await window.ethereum.request({ method: 'eth_requestAccounts' });
        const web3 = new window.Web3(window.ethereum);

        const abi = [
            {
                "inputs": [{ "internalType": "address", "name": "_seller", "type": "address" }],
                "stateMutability": "nonpayable",
                "type": "constructor"
            },
            {
                "inputs": [],
                "name": "deposit",
                "outputs": [],
                "stateMutability": "payable",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "releaseFunds",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
        ];

        const escrowContract = new web3.eth.Contract(abi, contractAddress);
        const accounts = await web3.eth.getAccounts();

        const amountInWei = web3.utils.toWei(amount.toString(), "ether");

        alert("Processing payment...");

        await escrowContract.methods.deposit().send({
            from: accounts[0],
            value: amountInWei,
        });

        alert("Payment successful via Escrow!");
    } catch (error) {
        console.error("Error during payment:", error);
        alert("Payment failed: " + error.message);
    }
}

// Release funds to the seller (only by buyer)
async function releaseFunds(contractAddress) {
    if (!window.ethereum) {
        alert("MetaMask not detected!");
        return;
    }

    try {
        await window.ethereum.request({ method: 'eth_requestAccounts' });
        const web3 = new window.Web3(window.ethereum);

        const abi = [
            {
                "inputs": [],
                "name": "releaseFunds",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
        ];

        const escrowContract = new web3.eth.Contract(abi, contractAddress);
        const accounts = await web3.eth.getAccounts();

        alert("Releasing funds...");

        await escrowContract.methods.releaseFunds().send({
            from: accounts[0],
        });

        alert("Funds released successfully to the seller!");
    } catch (error) {
        console.error("Error releasing funds:", error);
        alert("Release failed: " + error.message);
    }
}

// Auto-connect if MetaMask is already authorized
window.addEventListener("load", async () => {
    if (window.ethereum) {
        try {
            const accounts = await window.ethereum.request({ method: "eth_accounts" });
            if (accounts.length > 0) {
                console.log("Auto-connected to MetaMask:", accounts[0]);
            }
        } catch (error) {
            console.error("Auto-connect error:", error);
        }
    }
});
