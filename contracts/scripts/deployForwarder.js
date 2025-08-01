const { ethers } = require("hardhat");

async function main() {
  console.log("Deploying Forwarder contract...");

  const Forwarder = await ethers.getContractFactory("Forwarder");
  const forwarder = await Forwarder.deploy();

  await forwarder.waitForDeployment();

  const forwarderAddress = await forwarder.getAddress();
  console.log("Forwarder deployed to:", forwarderAddress);

  // Verify the deployment
  console.log("Forwarder deployment verified!");
  console.log("Contract address:", forwarderAddress);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  }); 