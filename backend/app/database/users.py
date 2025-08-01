from .utils import get_db_conn
from ..utils.crypto import decrypt_key

def upsert_users(email: str, public_address: str, private_key_encrypted: str):
    try:
        conn = get_db_conn()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users (email, public_address, private_key_encrypted)
            VALUES (%s, %s, %s)
            ON CONFLICT (email) DO NOTHING;
        """, (email, public_address, private_key_encrypted))
        conn.commit()
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()

def get_user_by_email(email: str):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("""
                SELECT id, email, public_address, private_key_encrypted
                   FROM users
                   WHERE email = (%s)
                   """, (email,))
    user = cursor.fetchone()
    return {
        "id": user[0], 
        "email": user[1],
        "public_address": user[2],
        "private_key": decrypt_key(user[3]).hex()
    }

def does_user_exist(email: str = None, id: int = None):
    if not email and not id:
        raise Exception("Enter user email or id.")
    
    conn = get_db_conn()
    cursor = conn.cursor()
    try:
        if email:
            cursor.execute("""
                        SELECT id, email, public_address
                        FROM users
                        WHERE email = (%s)
                        """, (email,))
            user = cursor.fetchone()
            return user is not None
        
        else:
            cursor.execute("""
                        SELECT id, email, public_address
                        FROM users
                        WHERE id = (%s)
                        """, (id,))
            user = cursor.fetchone()
            return user is not None
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()