import asyncio
import requests
from telegram import Bot



# 🔑 DATOS DE TU BOT
TOKEN = "8516573287:AAGVAMbvvBkU4G4JmSM3wj2AE_BhlDU2uJQ"
CHAT_ID = 2068937462



bot = Bot(token=TOKEN)

async def enviar(texto):
    await bot.send_message(chat_id=CHAT_ID, text=texto)

BUSQUEDAS = ["celular", "notebook", "televisor", "consola", "audifonos"]

headers = {"User-Agent": "Mozilla/5.0"}

while True:
    for busqueda in BUSQUEDAS:
        url = f"https://api.mercadolibre.com/sites/MLC/search?q={busqueda}&limit=50"
        r = requests.get(url, headers=headers)

        print("Estado:", r.status_code)

        data = r.json()

        if "results" not in data:
            print("Bloqueado en:", busqueda)
            continue

        productos = data["results"]

        for p in productos:
            titulo = p["title"]
            precio = p["price"]
            original = p.get("original_price")

            if not original:
                continue

            descuento = int(100 - (precio * 100 / original))

            if descuento >= 30:
                mensaje = f"""
🔥 OFERTA DETECTADA
{titulo}
💰 ${precio}
📉 {descuento}% OFF
🔗 {p['permalink']}
"""
                asyncio.run(enviar(mensaje))

    import time
    time.sleep(300)



 
