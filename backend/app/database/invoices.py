
from .utils import get_db_conn

def get_escrow_info(escrow_address):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("""
    Select escrow, client.email, freelancer.email
    from invoices
        join users client on invoices.client_id=client.id
        join users freelancer on invoices.freelancer_id = freelancer.id
    where escrow = %s
""", (escrow_address,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if row:
        return {
            "escrow": row[0],
            "client_email": row[1],
            "freelancer_email": row[2]
        }
    return None

def get_invoice_info_with_milestones(invoice_id: int):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("""
    Select invoices.escrow, client.email, freelancer.email
    from invoices 
        join users client on invoices.client_id=client.id
        join users freelancer on invoices.freelancer_id = freelancer.id
    where invoices.id = %s
""", (invoice_id,))
    row = cursor.fetchone()
    
    if not row:
        cursor.close()
        conn.close()
        return None
        
    escrow_address, client, freelancer = row

    cursor.execute("""
      SELECT idx, amount, funded, released, funded_tx, release_tx
      FROM milestones WHERE escrow=%s ORDER BY idx
    """, (escrow_address,))
    mrows = cursor.fetchall()
    cursor.close()
    conn.close()

    milestones = [
        {
            "index": idx,
            "amount": float(amount),
            "funded": funded,
            "released": released,
        } for idx, amount, funded, released, *_ in mrows
    ]

    return {
        "invoice_id": invoice_id,
        "escrow": escrow_address,
        "client_email": client,
        "freelancer_email": freelancer,
        "milestones": milestones
    }


def insert_invoice(escrow:str, client:str, freelancer: str):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO invoices (escrow, client_id, freelancer_id) VALUES (%s, %s, %s) RETURNING id",
        (escrow, client, freelancer)
    )
    invoice_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return invoice_id