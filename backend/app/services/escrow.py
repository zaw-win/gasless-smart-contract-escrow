from shared.constants import *
from ..database.invoices import insert_invoice, get_escrow_info, get_invoice_info_with_milestones
from ..database.milestones import upsert_milestones
from ..database.users import get_user_by_email
from shared.utils import get_escrow_contract
from eth_account.messages import encode_typed_data
from .permit2 import generate_usdc_permit_signature, submit_usdc_permit_via_sponsor
import time

# global variable
sponsor_account = w3.eth.account.from_key(SPONSOR_PRIVATE_KEY)

def _ensure_usdc_allowance_gasless(client_account, spender_address, required_amount):
    """
    Ensure spender has sufficient USDC allowance from client using gasless EIP-2612 permit.
    
    Args:
        client_account: Web3 account object for the client
        spender_address: Address that needs allowance (e.g., escrow contract)
        required_amount: Minimum required allowance amount
    """
    # Check current allowance
    current_allowance = usdc.functions.allowance(client_account.address, spender_address).call()
    print(f"Current USDC allowance from {client_account.address} to {spender_address}: {current_allowance}")
    print(f"Required amount: {required_amount}")
    
    if current_allowance < required_amount:
        max_uint256 = 2**256 - 1
        
        # Generate permit signature for USDC approval
        permit_signature = generate_usdc_permit_signature(
            client_account,
            spender_address,
            max_uint256,
            int(time.time()) + (365 * 24 * 60 * 60)  # 1 year deadline
        )
        
        # Submit permit via sponsor (sponsor pays gas)
        permit_receipt = submit_usdc_permit_via_sponsor(
            client_account.address,
            spender_address,
            max_uint256,
            permit_signature['deadline'],
            permit_signature['v'],
            permit_signature['r'],
            permit_signature['s']
        )
        
        # Wait for permit to be confirmed and verify allowance
        print(f"Permit confirmed in block {permit_receipt.blockNumber}, verifying allowance...")
        
        # Double-check that allowance was actually set
        new_allowance = usdc.functions.allowance(client_account.address, spender_address).call()
        print(f"New allowance after permit: {new_allowance}")
        
        if new_allowance < required_amount:
            raise Exception(f"Permit failed: allowance {new_allowance} still less than required {required_amount}")

def _sign_and_get_receipt(client, txn):
    signed = client.sign_transaction(txn)
    
    # Retry logic for nonce collision issues
    max_retries = 3
    for attempt in range(max_retries):
        try:
            txn_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
            receipt = w3.eth.wait_for_transaction_receipt(
                txn_hash,
                timeout=300,
                poll_latency=5
            )
            return receipt
        except Exception as e:
            error_msg = str(e)
            if "replacement transaction underpriced" in error_msg or "nonce too low" in error_msg:
                if attempt < max_retries - 1:
                    print(f"Nonce collision detected, retrying (attempt {attempt + 1}/{max_retries})")
                    time.sleep(2)  # Wait 2 seconds before retry
                    # Update nonce and gas price for retry
                    new_nonce = w3.eth.get_transaction_count(client.address, "pending")
                    txn["nonce"] = new_nonce
                    txn["gasPrice"] = txn.get("gasPrice", w3.eth.gas_price) + w3.to_wei(1, 'gwei')
                    signed = client.sign_transaction(txn)
                    continue
                else:
                    print(f"Failed after {max_retries} attempts: {error_msg}")
                    raise e
            else:
                raise e

def _execute_forwarder_meta(client_account, target_contract, function_name, args, sponsor_account):
    """
    Execute a gasless meta-transaction using OpenZeppelin ERC2771Forwarder.
    
    The client signs an EIP-712 message authorizing the function call,
    and the sponsor submits the transaction paying all gas fees.
    
    Args:
        client_account: Web3 account of the user making the call
        target_contract: Contract instance to call
        function_name: Name of the function to call
        args: Arguments to pass to the function
        sponsor_account: Account that pays gas fees
        
    Returns:
        tuple: (receipt, sponsor_nonce) from the executed transaction
    """
    client_address = client_account.address

    # Get forwarder contract
    forwarder_contract = w3.eth.contract(address=FORWARDER_ADDRESS, abi=FORWARDER_ABI)
    
    # Get client's nonce from forwarder
    client_nonce = forwarder_contract.functions.nonces(client_address).call()
    
    # Build function call data with client as sender to avoid validation errors
    function_data = target_contract.get_function_by_name(function_name)(*args).build_transaction({
        'from': client_address  # Specify client as sender for validation
    })['data']
    
    # Calculate deadline (current time + 1 hour)
    deadline = int(time.time()) + 3600
    
    # Build ForwardRequest struct for EIP-712 signing (includes nonce, excludes signature)
    typed_data = {
        "types": {
            "EIP712Domain": [
                {"name": "name",              "type": "string"},
                {"name": "version",           "type": "string"},
                {"name": "chainId",           "type": "uint256"},
                {"name": "verifyingContract", "type": "address"},
            ],
            "ForwardRequest": [
                {"name": "from",      "type": "address"},
                {"name": "to",        "type": "address"},
                {"name": "value",     "type": "uint256"},
                {"name": "gas",       "type": "uint256"},
                {"name": "nonce",     "type": "uint256"},
                {"name": "deadline",  "type": "uint48"},
                {"name": "data",      "type": "bytes"},
            ],
        },
        "domain": {
            "name":              "Forwarder",
            "version":           "1",
            "chainId":           w3.eth.chain_id,
            "verifyingContract": FORWARDER_ADDRESS,
        },
        "primaryType": "ForwardRequest",
        "message": {
            'from': client_address,
            'to': target_contract.address,
            'value': 0,
            'gas': 200000,
            'nonce': client_nonce,  # Include nonce in EIP-712 signature
            'deadline': deadline,
            'data': function_data,
        },
    }

    # Sign the message
    signable_msg = encode_typed_data(full_message=typed_data)
    signed = client_account.sign_message(signable_msg)
    signature = signed.signature
    
    # Verify signature is valid (optional debug check)
    try:
        recovered_address = w3.eth.account.recover_message(signable_msg, signature=signature)
        if recovered_address.lower() != client_address.lower():
            raise ValueError(f"Signature verification failed: expected {client_address}, got {recovered_address}")
    except Exception as e:
        raise ValueError(f"Invalid signature: {e}")
    
    # Create the final ForwardRequestData tuple for the contract call
    # OpenZeppelin ERC2771Forwarder.ForwardRequestData struct format:
    # struct ForwardRequestData {
    #     address from;
    #     address to;
    #     uint256 value;
    #     uint256 gas;
    #     uint48 deadline;  // deadline comes before data
    #     bytes data;
    #     bytes signature;
    # }
    # Note: nonce is NOT included in the execute call tuple, only in the EIP-712 signature
    request_tuple = (
        client_address,           # from
        target_contract.address,  # to
        0,                        # value
        200000,                   # gas
        deadline,                 # deadline (uint48)
        function_data,            # data
        signature                 # signature
    )
       
    # Sponsor executes the forward request
    sponsor_nonce = w3.eth.get_transaction_count(sponsor_account.address, "pending")
    
    execute_txn = forwarder_contract.functions.execute(
        request_tuple
    ).build_transaction({
        "from": sponsor_account.address,
        "nonce": sponsor_nonce,
        "chainId": CHAIN_ID,
        "gasPrice": w3.eth.gas_price + w3.to_wei(1, 'gwei')  # Add 1 gwei to avoid underpriced
    })
    
    # Sponsor signs and submits
    receipt = _sign_and_get_receipt(sponsor_account, execute_txn)
    print(f"[forwarder_meta] {function_name} successful: {receipt.transactionHash.hex()}")
    
    return receipt, sponsor_nonce


def fund_milestone(invoice_id: int, milestone_index: int):

    escrow_address = get_invoice_info_with_milestones(invoice_id)["escrow"]
    escrow_contract = get_escrow_contract(escrow_address, ESCROW_ABI)
    escrow_info = get_escrow_info(escrow_address=escrow_address)

    client_data = get_user_by_email(escrow_info["client_email"])
    client_private_key = client_data["private_key"]
    client_account = w3.eth.account.from_key(client_private_key)

    amount = escrow_contract.functions.milestones(milestone_index).call()[0]
    print("Amount to fund: ", amount)

    # Ensure escrow contract has approval to spend client's USDC (gasless)
    _ensure_usdc_allowance_gasless(client_account, escrow_address, amount)

    # Execute meta-transaction using forwarder
    try:
        print(f"[fund_milestone] Funding milestone {milestone_index} via gasless transaction...")
        
        fund_receipt, _ = _execute_forwarder_meta(
            client_account,
            escrow_contract,
            'fundMilestone',
            [milestone_index],
            sponsor_account
        )
        print(f"[fund_milestone] Milestone funding successful: {fund_receipt.transactionHash.hex()}")
        
        receipt = fund_receipt
    except Exception as e:
        print(f"[fund_milestone] Transaction failed: {e}")
        raise e
    upsert_milestones(escrow_address=escrow_address, idx=milestone_index, amt=amount, funded=True, funded_tx=receipt.transactionHash.hex())
    return receipt


def release_milestone(invoice_id: int, milestone_index: int):
    escrow_address = get_invoice_info_with_milestones(invoice_id)["escrow"]
    escrow_contract = get_escrow_contract(escrow_address, ESCROW_ABI)
    escrow_info = get_escrow_info(escrow_address=escrow_address)
    
    client_data = get_user_by_email(escrow_info["client_email"])
    client_private_key = client_data["private_key"]
    client_account = w3.eth.account.from_key(client_private_key)
    
    amount = escrow_contract.functions.milestones(milestone_index).call()[0]
    print(f"Amount to release: {amount}")

    # Execute meta-transaction using forwarder
    try:
        print(f"[release_milestone] Releasing milestone {milestone_index} via gasless transaction...")
        
        release_receipt, _ = _execute_forwarder_meta(
            client_account,
            escrow_contract,
            'releaseMilestone',
            [milestone_index],
            sponsor_account
        )
        print(f"[release_milestone] Milestone release successful: {release_receipt.transactionHash.hex()}")
        
        receipt = release_receipt
    except Exception as e:
        print(f"[release_milestone] Transaction failed: {e}")
        raise e
        
    upsert_milestones(escrow_address=escrow_address, idx=milestone_index, amt=amount, released=True, release_tx=receipt.transactionHash.hex())
    return receipt

def get_milestones(invoice_id):
    return get_invoice_info_with_milestones(invoice_id)["milestones"]


def _update_gas_fees(txn, priority_tip_in_gwei:int):
    block=w3.eth.get_block("latest")
    base=block["baseFeePerGas"]
    priority=w3.to_wei(priority_tip_in_gwei,"gwei")
    txn.update({
        "maxFeePerGas":base + priority*2,
        "maxPriorityFeePerGas": priority,
    })



def create_escrow(client_email: str, freelancer_email: str, milestone_amounts: list):
    client_data = get_user_by_email(client_email)
    freelancer_data = get_user_by_email(freelancer_email)
    
    client_id = client_data["id"]
    client_address = client_data["public_address"]
    freelancer_id = freelancer_data["id"]
    freelancer_address = freelancer_data["public_address"]
    
    # Get client's private key for signing
    client_private_key = client_data["private_key"]
    client_account = w3.eth.account.from_key(client_private_key)
    
    # Get initial nonce for sponsor account
    sponsor_nonce = w3.eth.get_transaction_count(sponsor_account.address, "pending")
    
    # Deploy the contract with forwarder address
    Escrow = w3.eth.contract(abi=ESCROW_ABI, bytecode=ESCROW_BYTECODE)
    deploy_txn = Escrow.constructor(FORWARDER_ADDRESS).build_transaction({
        "from": sponsor_account.address,
        "nonce": sponsor_nonce,
        "chainId": CHAIN_ID,
        "gasPrice": w3.eth.gas_price + w3.to_wei(1, 'gwei')  # Add 1 gwei to avoid underpriced
    })
    
    # Sponsor deploys the contract
    deploy_receipt = _sign_and_get_receipt(sponsor_account, deploy_txn)
    
    escrow_address = deploy_receipt.contractAddress
    
    # Now call the meta transaction function using forwarder
    escrow_contract = get_escrow_contract(escrow_address, ESCROW_ABI)

    # Execute meta-transaction using forwarder
    try:
        print("[create_escrow] Initializing escrow via gasless transaction...")
        print(f"Debug - Escrow address: {escrow_address}")
        print(f"Debug - Client address: {client_address}")
        print(f"Debug - Freelancer address: {freelancer_address}")
        print(f"Debug - Milestone amounts: {milestone_amounts}")
        
        # Check if escrow is properly deployed and forwarder is trusted
        try:
            is_trusted = escrow_contract.functions.isTrustedForwarder(FORWARDER_ADDRESS).call()
            print(f"Debug - Is forwarder trusted by new escrow: {is_trusted}")
        except Exception as debug_e:
            print(f"Debug - Could not check trusted forwarder: {debug_e}")
        
        create_receipt, _ = _execute_forwarder_meta(
            client_account,
            escrow_contract,
            'createEscrow',
            [client_address, freelancer_address, USDC_ERC20_ADDRESS, milestone_amounts],
            sponsor_account
        )
        print(f"[create_escrow] Escrow initialization successful: {create_receipt.transactionHash.hex()}")
        
        update_contract_receipt = create_receipt
    except Exception as e:
        print(f"[create_escrow] Transaction failed: {e}")
        print(f"Debug - Full error details: {type(e).__name__}: {e}")
        raise e
    
    # Create invoice and milestones
    invoice_id = insert_invoice(escrow_address, client_id, freelancer_id)
    
    for index, amt in enumerate(milestone_amounts):
        print(f"Amt {amt} in Index {index}")
        upsert_milestones(
            escrow_address=escrow_address,
            idx=index,
            amt=amt,
            funded=False,
            released=False
        )
    
    return {
        "invoice_id": invoice_id,
        "escrow": escrow_address,
        "txn_hash": update_contract_receipt.transactionHash.hex()
    }

