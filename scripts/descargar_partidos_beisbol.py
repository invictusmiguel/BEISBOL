# sampro_v6/beisbol/scripts/descargar_partidos_beisbol.py

import requests
import os
import datetime
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

# 📁 Rutas
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
data_dir = os.path.join(base_dir, 'datos')
os.makedirs(data_dir, exist_ok=True)

# 🔁 Función de request
def get(endpoint, params=None):
    url = f"{API_URL}{endpoint}"
    try:
        res = requests.get(url, headers=HEADERS, params=params, timeout=10)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print(f"⛔ Error en {endpoint}: {e}")
        return {}

# 💾 Guardar archivo
def save_json(filename, content):
    path = os.path.join(data_dir, filename)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(content, f, ensure_ascii=False, indent=2)
    print(f"✅ Guardado: {filename}")

# 📥 Descargar solo partidos del día
def descargar_partidos():
    print(f"📅 Descargando partidos de béisbol para {today}...")
    juegos = get("/games", {"date": today})
    save_json("juegos_hoy.json", juegos)

    total = len(juegos.get("response", []))
    print(f"🎯 Total de partidos encontrados: {total}")

if __name__ == "__main__":
    descargar_partidos()
