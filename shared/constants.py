from dotenv import load_dotenv
import os
from web3 import Web3
import json

load_dotenv()

RPC_URL = os.getenv("RPC_URL")
# PRIVATE_KEY = os.getenv("PRIVATE_KEY")
# FREELANCER_PRIVATE_KEY = os.getenv("FREELANCER_PRIVATE_KEY")
SPONSOR_PRIVATE_KEY = os.getenv("SPONSOR_PRIVATE_KEY")  # For meta transactions
# ESCROW_CONTRACT_ADDRESS = os.getenv("ESCROW_CONTRACT_ADDRESS_v2")
USDC_ERC20_ADDRESS = os.getenv("USDC_CONTRACT_ADDRESS")
CHAIN_ID = 84532 #base_sepolia_chain
DATABASE_URL = os.getenv("DATABASE_URL")
LLM_MODEL = os.getenv("LLM_MODEL")

#w3 instantiation
w3 = Web3(Web3.HTTPProvider(RPC_URL, request_kwargs={"timeout": 60}))
if not w3.is_connected():
    raise ConnectionError("Web3 is not connected. Check your RPC_URL.")

# # client account on base sepolia
# client = w3.eth.account.from_key(PRIVATE_KEY)

# # freelancer account on base sepolia
# freelancer = w3.eth.account.from_key(FREELANCER_PRIVATE_KEY)

# USDC address on base sepolia
with open("backend/app/utils/usdc_abi.json") as f:
    USDC_ABI = json.load(f)
usdc = w3.eth.contract(address=USDC_ERC20_ADDRESS, abi=USDC_ABI)

# ESCROW SCHEMA
with open("backend/app/utils/escrow_abi.json") as f:
    escrow_json = json.load(f)
    ESCROW_ABI = escrow_json["abi"]
    ESCROW_BYTECODE = escrow_json["bytecode"]

# FORWARDER SCHEMA
with open("backend/app/utils/forwarder_abi.json") as f:
    FORWARDER_ABI = json.load(f)["abi"]

# FORWARDER SCHEMA
with open("backend/app/utils/permit2_abi.json") as f:
    PERMIT2_ABI = json.load(f)["abi"]

# Forwarder contract address (you'll need to deploy this first)
FORWARDER_ADDRESS = os.getenv("FORWARDER_CONTRACT_ADDRESS")  # Add this to your .env file