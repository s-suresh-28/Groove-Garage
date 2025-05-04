const { ethers } = require("hardhat");

async function main() {
    const [deployer] = await ethers.getSigners();
    console.log("Deploying contracts with the account:", deployer.address);

    // Replace this with the seller address from Ganache
    const sellerAddress = "0xddc92dA18F269A46870376286d07afe952BE9AF3";

    // Deploying the contract
    const Escrow = await ethers.getContractFactory("Escrow");
    const escrow = await Escrow.deploy(sellerAddress);

    await escrow.waitForDeployment(); // ✅ Updated here

    console.log("✅ Escrow Contract Deployed to:", await escrow.getAddress());
}

main().catch((error) => {
    console.error("❌ Error during deployment:", error);
    process.exitCode = 1;
});
