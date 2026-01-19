import asyncio
import threading
from flask import Flask
from telegram import Bot
import requests
from bs4 import BeautifulSoup
import time
import os


# 🔑 DATOS DE TU BOT
TOKEN = "8516573287:AAGVAMbvvBkU4G4JmSM3wj2AE_BhlDU2uJQ"
CHAT_ID = 2068937462



DESCUENTO_MINIMO = 30  # puedes subirlo a 75 después

BUSQUEDAS = [
    "https://listado.mercadolibre.cl/ofertas",
    "https://listado.mercadolibre.cl/liquidacion",
    "https://listado.mercadolibre.cl/outlet",
    "https://listado.mercadolibre.cl/remate"
]

bot = Bot(token=TOKEN)
precios_guardados = {}

# ===== FLASK (para Render) =====
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot activo"

def iniciar_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# ===== BOT =====
async def enviar_mensaje(texto):
    await bot.send_message(chat_id=CHAT_ID, text=texto)

def revisar_ofertas():
    while True:
        for url in BUSQUEDAS:
            headers = {"User-Agent": "Mozilla/5.0"}
            r = requests.get(url, headers=headers)
            soup = BeautifulSoup(r.text, "html.parser")
            items = soup.find_all("li", class_="ui-search-layout__item")

            for item in items:
                try:
                    titulo = item.find("h2").text
                    link = item.find("a")["href"]

                    precio_actual = item.find("span", class_="andes-money-amount__fraction").text
                    precio_actual = int(precio_actual.replace(".", ""))

                    descuento_tag = item.find("span", class_="andes-money-amount__discount")
                    if not descuento_tag:
                        continue

                    descuento = int(descuento_tag.text.replace("% OFF", "").replace(" ", ""))

                    print("Revisando:", titulo, descuento)

                    if descuento < DESCUENTO_MINIMO:
                        continue

                    if link in precios_guardados and precio_actual >= precios_guardados[link]:
                        continue

                    precios_guardados[link] = precio_actual

                    mensaje = f"""
🔥 DESCUENTO DETECTADO
{titulo}
💲 ${precio_actual}
📉 {descuento}% OFF
🔗 {link}
"""
                    asyncio.run(enviar_mensaje(mensaje))

                except:
                    continue

        time.sleep(300)

# ===== INICIO =====
threading.Thread(target=revisar_ofertas).start()
iniciar_web()
