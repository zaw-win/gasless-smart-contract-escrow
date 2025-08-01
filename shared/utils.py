from .constants import w3

def get_escrow_contract(escrow_address, escrow_abi):
    return w3.eth.contract(address=escrow_address, abi=escrow_abi)
