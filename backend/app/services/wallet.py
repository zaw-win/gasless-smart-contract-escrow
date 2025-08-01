from ..database.users import does_user_exist, upsert_users
from eth_account import Account
from ..utils.crypto import encrypt_key

def create_user_and_wallet_if_not_exists(user_email: str):
    if not does_user_exist(user_email):
        # create wallet
        account = Account.create()
        pub_addr = account.address
        private_key = encrypt_key(account.key)
        upsert_users(user_email, pub_addr, private_key)
        return user_email
    else:
        return user_email