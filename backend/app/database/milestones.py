from .utils import get_db_conn

def upsert_milestones(escrow_address, idx, amt, funded=None, released=None, funded_tx=None,release_tx=None ):
    try:
        conn = get_db_conn()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO milestones (escrow, idx, amount, funded, released, funded_tx, release_tx)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (escrow, idx) DO UPDATE
            SET amount   = EXCLUDED.amount,
                funded   = COALESCE(EXCLUDED.funded, milestones.funded),
                released = COALESCE(EXCLUDED.released, milestones.released),
                funded_tx = COALESCE(EXCLUDED.funded_tx, milestones.funded_tx),
                release_tx = COALESCE(EXCLUDED.release_tx, milestones.release_tx);
        """, (escrow_address, idx, amt, funded, released, funded_tx, release_tx))
        conn.commit()
    except Exception as e:
        raise
    finally:
        cursor.close()
        conn.close()
