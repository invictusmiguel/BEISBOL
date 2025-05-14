# sampro_v6/beisbol/scripts/descargar_mercado_parimpar.py

import os
import json
import requests
import time

# 🔐 API Config
API_KEY = "cef9115ecad4dcadf30573ca8c3d3abe"
API_HOST = "v1.baseball.api-sports.io"
API_URL = f"https://{API_HOST}"

HEADERS = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": API_HOST
}

# 📁 Rutas
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
datos_dir = os.path.join(base_dir, 'datos')
output_dir = os.path.join(datos_dir, 'mercados', 'parimpar')
os.makedirs(output_dir, exist_ok=True)

file_juegos = os.path.join(datos_dir, "juegos_hoy.json")

def get(endpoint, params=None):
    url = f"{API_URL}{endpoint}"
    try:
        res = requests.get(url, headers=HEADERS, params=params, timeout=10)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print(f"⛔ Error en {endpoint}: {e}")
        return {}

def descargar_parimpar():
    if not os.path.exists(file_juegos):
        print("❌ No existe juegos_hoy.json")
        return

    with open(file_juegos, "r", encoding="utf-8") as f:
        juegos = json.load(f).get("response", [])

    print(f"🔍 Procesando {len(juegos)} partidos para mercado PAR/IMPAR...")

    for partido in juegos:
        game_id = partido["id"]
        home = partido["teams"]["home"]["name"]
        away = partido["teams"]["away"]["name"]
        print(f"⚾ {home} vs {away} — ID: {game_id}")

        odds_data = get("/odds", {"game": game_id})
        encontrado = False

        for resp in odds_data.get("response", []):
            for book in resp.get("bookmakers", []):
                for bet in book.get("bets", []):
                    nombre = bet.get("name", "").lower()
                    if "odd/even" in nombre or "par" in nombre or "impar" in nombre:
                        out_path = os.path.join(output_dir, f"parimpar_{game_id}.json")
                        with open(out_path, "w", encoding="utf-8") as f_out:
                            json.dump(bet, f_out, ensure_ascii=False, indent=2)
                        print(f"✅ Guardado: parimpar_{game_id}.json")
                        encontrado = True
                        break
                if encontrado:
                    break
            if encontrado:
                break

        if not encontrado:
            print(f"⚠️ No se encontró mercado PAR/IMPAR para {game_id}")

        time.sleep(0.5)

    print("🎯 Descarga del mercado PAR/IMPAR completada.")

if __name__ == "__main__":
    descargar_parimpar()
