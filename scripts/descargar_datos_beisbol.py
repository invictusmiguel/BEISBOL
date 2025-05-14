# sampro_v6/beisbol/scripts/descargar_datos_beisbol.py

import requests
import datetime
import os
import json

# 🔐 Configuración API
API_KEY = "cef9115ecad4dcadf30573ca8c3d3abe"
API_HOST = "v1.baseball.api-sports.io"
API_URL = f"https://{API_HOST}"

HEADERS = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": API_HOST
}

# 📅 Fecha de hoy
today = datetime.date.today().strftime("%Y-%m-%d")

# 📁 Directorio donde se guardan los datos
data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'datos'))
ruta_juegos = os.path.join(data_dir, "juegos_hoy.json")

def get(endpoint, params=None):
    url = f"{API_URL}{endpoint}"
    try:
        res = requests.get(url, headers=HEADERS, params=params, timeout=10)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print(f"⛔ Error en GET {endpoint}: {e}")
        return {}

def descargar_juegos():
    print(f"📅 Buscando partidos de béisbol para {today}...")

    response = get("/games", {"date": today})
    juegos = response.get("response", [])

    if not juegos:
        print("⚠️ No se encontraron juegos para hoy.")
        return

    print(f"📌 Partidos encontrados: {len(juegos)}")

    # 🕒 Extraer hora y guardarla en el JSON
    for game in juegos:
        fecha = game.get("fixture", {}).get("date", "")
        if fecha:
            game["hora"] = fecha[11:16]  # Extrae HH:MM

    # 💾 Guardar JSON final
    os.makedirs(data_dir, exist_ok=True)
    with open(ruta_juegos, "w", encoding="utf-8") as f:
        json.dump({"response": juegos}, f, ensure_ascii=False, indent=2)

    print(f"✅ Guardado: {ruta_juegos}")
    print("🎯 ¡Descarga completa del módulo BÉISBOL!")

if __name__ == "__main__":
    descargar_juegos()
