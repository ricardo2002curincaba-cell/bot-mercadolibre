import threading
from flask import Flask
from telegram import Bot
import requests
from bs4 import BeautifulSoup
import time
import os

DESCUENTO_MINIMO = 30
# 🔑 DATOS DE TU BOT
TOKEN = "8516573287:AAGVAMbvvBkU4G4JmSM3wj2AE_BhlDU2uJQ"
CHAT_ID = 2068937462



BUSQUEDAS = [
    "https://listado.mercadolibre.cl/ofertas",
    "https://listado.mercadolibre.cl/liquidacion",
    "https://listado.mercadolibre.cl/outlet",
    "https://listado.mercadolibre.cl/remate"
]

bot = Bot(token=TOKEN)
precios_guardados = {}

# ===== FLASK =====
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot activo"

# ===== BOT =====
def revisar_ofertas():
    bot.send_message(chat_id=CHAT_ID, text="🟢 Bot iniciado correctamente")

    while True:
        for url in BUSQUEDAS:
            try:
                headers = {"User-Agent": "Mozilla/5.0"}
                r = requests.get(url, headers=headers)
                soup = BeautifulSoup(r.text, "html.parser")

                items = soup.find_all("li", class_="ui-search-layout__item")

                for item in items:
                    try:
                        titulo = item.find("h2").text
                        link = item.find("a")["href"]

                        descuento_tag = item.find("span", class_="andes-money-amount__discount")
                        if not descuento_tag:
                            continue

                        descuento = int(descuento_tag.text.replace("% OFF", "").replace(" ", ""))

                        print("Revisando:", titulo, descuento)

                        if descuento < DESCUENTO_MINIMO:
                            continue

                        bot.send_message(
                            chat_id=CHAT_ID,
                            text=f"🔥 {titulo}\n📉 {descuento}% OFF\n🔗 {link}"
                        )

                    except:
                        continue
            except:
                pass

        time.sleep(300)

# ===== INICIO =====
threading.Thread(target=revisar_ofertas).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
