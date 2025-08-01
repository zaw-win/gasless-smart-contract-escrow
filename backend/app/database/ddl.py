create_users_tbl = """
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    public_address TEXT NOT NULL,
    private_key_encrypted TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
)
"""

create_milestones_tbl = """
CREATE TABLE IF NOT EXISTS milestones(
    id SERIAL PRIMARY KEY,
    escrow TEXT REFERENCES invoices(escrow),
    idx INTEGER,
    amount NUMERIC(18,6),
    funded BOOLEAN DEFAULT FALSE,
    released BOOLEAN DEFAULT FALSE,
    funded_tx TEXT,
    release_tx TEXT,
    UNIQUE (escrow, idx)
)
"""

create_invoices_tbl = """
CREATE TABLE IF NOT EXISTS invoices(
    id SERIAL PRIMARY KEY,
    escrow TEXT NOT NULL UNIQUE,
    client_id INTEGER REFERENCES users(id),
    freelancer_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW()
    );
"""

