#!/usr/bin/env python3

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from shared.constants import w3, ESCROW_ABI, USDC_ERC20_ADDRESS
from shared.utils import get_escrow_contract

def test_contract_interaction(escrow_address):
    """Test basic contract interaction to identify issues"""
    
    print(f"Testing contract at address: {escrow_address}")
    print(f"Chain ID: {w3.eth.chain_id}")
    print(f"Current block: {w3.eth.block_number}")
    print(f"Connected to RPC: {w3.is_connected()}")
    
    try:
        # Test 1: Check if contract exists at address
        code = w3.eth.get_code(escrow_address)
        if code == b'':
            print("❌ ERROR: No contract deployed at this address")
            return False
        print("✅ Contract code found at address")
        
        # Test 2: Create contract instance
        escrow_contract = get_escrow_contract(escrow_address, ESCROW_ABI)
        print("✅ Contract instance created")
        
        # Test 3: Try to call a simple view function
        try:
            client_address = escrow_contract.functions.client().call()
            print(f"✅ Client address: {client_address}")
        except Exception as e:
            print(f"❌ ERROR calling client(): {e}")
            return False
            
        # Test 4: Try to call getMilestones
        try:
            milestones = escrow_contract.functions.getMilestones().call()
            print(f"✅ getMilestones() returned {len(milestones)} milestones")
            for i, milestone in enumerate(milestones):
                print(f"  Milestone {i}: amount={milestone[0]}, funded={milestone[1]}, released={milestone[2]}")
        except Exception as e:
            print(f"❌ ERROR calling getMilestones(): {e}")
            return False
            
        # Test 5: Check USDC contract
        try:
            usdc_code = w3.eth.get_code(USDC_ERC20_ADDRESS)
            if usdc_code == b'':
                print("❌ WARNING: No USDC contract found at specified address")
            else:
                print("✅ USDC contract found")
        except Exception as e:
            print(f"❌ ERROR checking USDC contract: {e}")
            
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_contract.py <escrow_address>")
        sys.exit(1)
        
    escrow_address = sys.argv[1]
    success = test_contract_interaction(escrow_address)
    
    if success:
        print("\n✅ All tests passed! Contract interaction should work.")
    else:
        print("\n❌ Tests failed. Check the errors above.") 