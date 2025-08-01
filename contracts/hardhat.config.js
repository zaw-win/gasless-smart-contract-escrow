require("dotenv").config({ path: "../.env" });
require("@nomicfoundation/hardhat-toolbox");

module.exports = {
  solidity: "0.8.28",
  networks: {
    base_sepolia: {
      url: process.env.RPC_URL,
      accounts: [process.env.SPONSOR_PRIVATE_KEY]
    },
  },
}
