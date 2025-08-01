# for future iterations

# import time
# from web3 import Web3
# from shared.utils import get_escrow_contract
# from shared.constants import w3
# from backend.app.database.utils import get_db_conn


# def run_event_listener(poll_interval: int = 5):
#     conn = get_db_conn()
#     cursor = conn.cursor()
#     funded_filter = escrow_contract.events.MilestoneFunded.create_filter(from_block="latest")
#     released_filter = escrow_contract.events.MilestoneReleased.create_filter(from_block="latest")
#     while True:
#         for event in funded_filter.get_new_entries():
#             idx, txh = event["args"]["index"], event["transactionHash"].hex()
#             cursor.execute(f"""
#                     UPDATE milestones
#                     SET funded=TRUE, funded_tx='{txh}'
#                     where idx = {idx}
#                         """)
#             conn.commit()

#         for event in released_filter.get_new_entries():
#             idx, txh = event["args"]["index"], event["transactionHash"].hex()
#             cursor.execute(f"""
#                     UPDATE milestones
#                     SET released=TRUE, release_tx='{txh}'
#                     where idx = {idx}
#                         """)
#             conn.commit()

#         time.sleep(poll_interval)