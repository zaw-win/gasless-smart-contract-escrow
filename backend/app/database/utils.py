import os, psycopg2
from dotenv import load_dotenv
load_dotenv()

def get_db_conn():
    url = os.getenv("DATABASE_URL")
    conn = psycopg2.connect(url)
    return conn

def execute_sql(sql_stmt: str):

    try:
        conn = get_db_conn()
        cursor = conn.cursor()
        cursor.execute(sql_stmt)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()
