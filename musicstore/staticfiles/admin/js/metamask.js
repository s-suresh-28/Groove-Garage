// static/js/metamask.js

// MetaMask Connection
async function connectMetaMask() {
    if (window.ethereum) {
        try {
            const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
            alert('Connected to MetaMask: ' + accounts[0]);

            // Send wallet address to the Django backend
            saveWalletAddress(accounts[0]);
        } catch (error) {
            console.error('Error connecting to MetaMask:', error);
        }
    } else {
        alert('MetaMask is not detected. Please install MetaMask.');
    }
}

// Save Wallet Address to Backend
async function saveWalletAddress(address) {
    try {
        await fetch('/save-wallet/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify({ wallet_address: address }),
        });
    } catch (error) {
        console.error('Error saving wallet address:', error);
    }
}

// Get CSRF Token
function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}
