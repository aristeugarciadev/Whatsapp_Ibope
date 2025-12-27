from fastapi import FastAPI, Request
from datetime import datetime
import hashlib

app = FastAPI()

def hash_phone(phone: str):
    return hashlib.sha256(phone.encode()).hexdigest()

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()

    phone = data.get("phone", "desconhecido")
    message_type = data.get("type", "text")

    phone_hash = hash_phone(phone)

    print({
        "phone_hash": phone_hash,
        "tipo": message_type,
        "hora": datetime.now().strftime("%H:%M:%S")
    })

    return {"status": "ok"}
