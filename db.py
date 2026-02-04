import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Carrega variáveis de ambiente do .env
load_dotenv()

def get_connection():
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL não configurada")

    # Cria a conexão
    conn = psycopg2.connect(
        database_url,
        cursor_factory=RealDictCursor
    )

    # Define encoding UTF-8
    conn.set_client_encoding('UTF8')

    return conn
