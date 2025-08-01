const { ethers } = require("hardhat");

async function main(){
    const [deployer, freelancer] = await ethers.getSigners();
    console.log("Deploying with: ", deployer.address);

    const Escrow = await ethers.getContractFactory("Escrow");

    const freelancerAddress = freelancer.address;
    const tokenAddress = "0x036CbD53842c5426634e7929541eC2318f3dCF7e";
    const milestoneAmounts = [ethers.parseUnits("1", 6), ethers.parseUnits("2", 6)];
    
    const escrow = await Escrow.deploy(freelancerAddress, tokenAddress, milestoneAmounts);
    await escrow.waitForDeployment();

    console.log("Escrow deployed to: ", await escrow.getAddress());
}

main().catch((error) => {
    console.error(error);
    process.exit(1) ;
});