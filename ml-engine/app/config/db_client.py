import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Memuat konfigurasi dari file .env ml-engine
load_dotenv()

def get_db_connection():
    """
    Membuat koneksi ke PostgreSQL menggunakan psycopg2 dengan RealDictCursor
    agar hasil query langsung berbentuk dictionary Python (key-value).
    """
    try:
        connection = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD"),
            port=int(os.getenv("DB_PORT", 5432)),
            cursor_factory=RealDictCursor
        )
        return connection
    except Exception as e:
        print(f"[Python DB Error] Gagal terhubung ke PostgreSQL: {e}")
        raise e