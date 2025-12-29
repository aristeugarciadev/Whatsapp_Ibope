from fastapi import FastAPI, Request
from datetime import datetime
import sqlite3
import hashlib
import re

app = FastAPI()

DB_NAME = "ibope.db"

# =========================
# Banco de Dados
# =========================

def get_conn():
    return sqlite3.connect(
        DB_NAME,
        timeout=30,
        check_same_thread=False
    )


def create_tables():
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS interacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telefone TEXT,
        mensagem TEXT,
        mensagem_hash TEXT,
        data_hora TEXT
    )
    """)

    conn.commit()
    cursor.close()
    conn.close()


# =========================
# Utilidades
# =========================

def normalizar_texto(texto: str) -> str:
    texto = texto.lower()
    texto = re.sub(r"[^a-z0-9\s]", "", texto)
    return texto.strip()


def gerar_hash(texto: str) -> str:
    return hashlib.sha256(texto.encode()).hexdigest()


# =========================
# Persistência
# =========================

def salvar_interacao(telefone: str, mensagem: str):
    conn = get_conn()
    cursor = conn.cursor()

    try:
        mensagem_norm = normalizar_texto(mensagem)
        mensagem_hash = gerar_hash(mensagem_norm)

        cursor.execute("""
            INSERT INTO interacoes (
                telefone,
                mensagem,
                mensagem_hash,
                data_hora
            )
            VALUES (?, ?, ?, ?)
        """, (
            telefone,
            mensagem,
            mensagem_hash,
            datetime.now().isoformat()
        ))

        conn.commit()

    finally:
        cursor.close()
        conn.close()


# =========================
# Eventos
# =========================

@app.on_event("startup")
def startup_event():
    create_tables()


# =========================
# Rotas
# =========================

@app.get("/")
def home():
    return {"status": "API WhatsApp Ibope rodando com sucesso"}


@app.post("/webhook")
async def webhook(request: Request):
    payload = await request.json()

    telefone = payload.get("telefone")
    mensagem = payload.get("mensagem")

    if telefone and mensagem:
        salvar_interacao(telefone, mensagem)

    return {"status": "ok"}
