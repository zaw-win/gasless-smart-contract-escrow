# backend/app/services/permit2.py

import os
from dotenv import load_dotenv
from eth_account import Account
from eth_account.messages import encode_typed_data
from shared.constants import PERMIT2_ABI, w3, CHAIN_ID, usdc
import time
from web3 import Web3


load_dotenv()

# ─────────── Configuration ───────────
PERMIT2_ADDRESS     = os.getenv("PERMIT2_ADDRESS")
SPONSOR_PRIVATE_KEY = os.getenv("SPONSOR_PRIVATE_KEY")
sponsor_account = Account.from_key(SPONSOR_PRIVATE_KEY)

# ─────────── Permit2 Contract ───────────

token_contract = usdc
permit2_contract = w3.eth.contract(address=PERMIT2_ADDRESS, abi=PERMIT2_ABI)


# Core permit signature and submission functions for USDC EIP-2612


def generate_usdc_permit_signature(client_account, spender_address: str, amount: int, deadline: int):
    """
    Generate EIP-2612 permit signature for USDC approval.
    This allows gasless approval by having the user sign off-chain.
    """
    # Get current nonce for the user
    nonce = token_contract.functions.nonces(client_account.address).call()
    
    # Build complete EIP-712 typed data structure for USDC permit
    typed_data = {
        'types': {
            'EIP712Domain': [
                {'name': 'name', 'type': 'string'},
                {'name': 'version', 'type': 'string'},
                {'name': 'chainId', 'type': 'uint256'},
                {'name': 'verifyingContract', 'type': 'address'}
            ],
            'Permit': [
                {'name': 'owner', 'type': 'address'},
                {'name': 'spender', 'type': 'address'},
                {'name': 'value', 'type': 'uint256'},
                {'name': 'nonce', 'type': 'uint256'},
                {'name': 'deadline', 'type': 'uint256'}
            ]
        },
        'domain': {
            'name': token_contract.functions.name().call(),
            'version': '2',  # USDC uses version '2'
            'chainId': CHAIN_ID,
            'verifyingContract': token_contract.address,
        },
        'primaryType': 'Permit',
        'message': {
            'owner': client_account.address,
            'spender': spender_address,
            'value': amount,
            'nonce': nonce,
            'deadline': deadline
        }
    }

    # Sign using encode_typed_data approach
    signable_message = encode_typed_data(full_message=typed_data)
    signed_message = client_account.sign_message(signable_message)
    
    # Extract v, r, s from signature
    signature_bytes = signed_message.signature
    r = signature_bytes[:32]
    s = signature_bytes[32:64]
    v = signature_bytes[64]

    return {
        'deadline': deadline,
        'v': v,
        'r': r,
        's': s,
        'nonce': nonce
    }

def submit_usdc_permit_via_sponsor(owner_address: str, spender_address: str, value: int, deadline: int, v: int, r: bytes, s: bytes):
    """
    Submit the EIP-2612 permit transaction via sponsor account (sponsor pays gas).
    This completes the gasless approval process.
    """
    print(f"Sponsor submitting USDC permit for {owner_address} to approve {spender_address}")
    
    # Build permit transaction
    permit_tx = token_contract.functions.permit(
        owner_address,  # owner
        spender_address,  # spender
        value,  # value
        deadline,  # deadline
        v,  # v
        r,  # r
        s   # s
    ).build_transaction({
        'from': sponsor_account.address,
        'nonce': w3.eth.get_transaction_count(sponsor_account.address, "pending"),
        'gasPrice': w3.eth.gas_price + w3.to_wei(1, 'gwei'),
        'chainId': CHAIN_ID
    })
    
    # Sponsor signs and submits the transaction
    signed_txn = sponsor_account.sign_transaction(permit_tx)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    
    # Wait for confirmation
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"USDC permit submitted successfully: {tx_hash.hex()}")
    
    return receipt

# Note: This function is now replaced by _ensure_usdc_allowance_gasless in escrow.py
# which provides more flexible allowance management for any spender address

