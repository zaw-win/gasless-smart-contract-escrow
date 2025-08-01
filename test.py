from web3 import Web3
from shared.utils import get_escrow_contract
from shared.constants import ESCROW_ABI

# Assume escrow_contract is your contract instance
escrow_contract = get_escrow_contract("0x713cc7F5e389401C8263838bd1Da283196f21b53", ESCROW_ABI)
event_filter = escrow_contract.events.DebugFundMilestoneMeta.create_filter(from_block=0)
events = event_filter.get_all_entries()
for event in events:
    print(event)