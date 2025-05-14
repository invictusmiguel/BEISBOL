# sampro_v6/beisbol/scripts/descargar_mercado_ganador.py

import os
import json
import requests
import time

# 🔐 Config API
API_KEY = "cef9115ecad4dcadf30573ca8c3d3abe"
API_HOST = "v1.baseball.api-sports.io"
API_URL = f"https://{API_HOST}"

HEADERS = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": API_HOST
}

# 📁 Rutas
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
data_dir = os.path.join(base_dir, 'datos')
output_dir = os.path.join(data_dir, 'mercados', 'ganador')
os.makedirs(output_dir, exist_ok=True)

file_juegos = os.path.join(data_dir, "juegos_hoy.json")

# 🔁 Request
def get(endpoint, params=None):
    url = f"{API_URL}{endpoint}"
    try:
        res = requests.get(url, headers=HEADERS, params=params, timeout=10)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print(f"⛔ Error en {endpoint}: {e}")
        return {}

# 📥 Descargar solo cuotas del mercado ganador
def descargar_cuotas_ganador():
    if not os.path.exists(file_juegos):
        print("❌ No existe juegos_hoy.json")
        return

    with open(file_juegos, "r", encoding="utf-8") as f:
        juegos = json.load(f).get("response", [])

    print(f"🔍 Procesando {len(juegos)} partidos...")

    for partido in juegos:
        game_id = partido["id"]
        home = partido["teams"]["home"]["name"]
        away = partido["teams"]["away"]["name"]
        print(f"⚾ {home} vs {away} — ID: {game_id}")

        # Buscar cuotas
        odds_data = get("/odds", {"game": game_id})
        encontrado = False

        for bookmaker in odds_data.get("response", []):
            for bet in bookmaker.get("bookmakers", []):
                for market in bet.get("bets", []):
                    if market.get("name", "").lower() in ["winner", "1x2", "match winner", "moneyline"]:
                        # Guardar solo este mercado
                        output_path = os.path.join(output_dir, f"ganador_{game_id}.json")
                        with open(output_path, "w", encoding="utf-8") as f_out:
                            json.dump(market, f_out, ensure_ascii=False, indent=2)
                        print(f"✅ Guardado: ganador_{game_id}.json")
                        encontrado = True
                        break
                if encontrado:
                    break
            if encontrado:
                break

        if not encontrado:
            print(f"⚠️ No se encontró mercado 'ganador' para {game_id}")

        time.sleep(0.5)

    print("🎯 Descarga del mercado GANADOR completada.")

if __name__ == "__main__":
    descargar_cuotas_ganador()
