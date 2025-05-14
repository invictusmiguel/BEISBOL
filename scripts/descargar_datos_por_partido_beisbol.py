import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.beisbol_api import obtener_datos_partido
import os
import json
from datetime import datetime
from api.beisbol_api import obtener_datos_partido

# 📁 Carga los partidos desde el archivo juegos_hoy.json
with open("D:/sampro_v6/beisbol/datos/juegos_hoy.json", "r", encoding="utf-8") as f:
    juegos = json.load(f)["response"]

# 📂 Directorios para guardar los datos
carpetas = {
    "cuotas": "D:/sampro_v6/beisbol/datos/cuotas",
    "estadisticas_equipo": "D:/sampro_v6/beisbol/datos/estadisticas_equipo",
    "estadisticas_jugadores": "D:/sampro_v6/beisbol/datos/estadisticas_jugadores",
    "eventos": "D:/sampro_v6/beisbol/datos/eventos",
    "h2h": "D:/sampro_v6/beisbol/datos/h2h"
}

# 🔁 Crea las carpetas si no existen
for carpeta in carpetas.values():
    os.makedirs(carpeta, exist_ok=True)

print(f"📦 Descargando datos detallados de {len(juegos)} partidos...")

for game in juegos:
    game_id = game["id"]
    home = game["teams"]["home"]["name"]
    away = game["teams"]["away"]["name"]

    print(f"⚾ {home} vs {away} — ID: {game_id}")

    try:
        # ⏱️ Fecha y hora
        date_raw = game["date"]
        time_raw = game.get("time", "00:00")
        fecha_hora = f"{date_raw} {time_raw}"

        # 🔄 Llama a la API personalizada para obtener todos los datos por partido
        datos = obtener_datos_partido(game_id)

        # ✅ Verifica que la respuesta sea válida
        if not datos or not all(k in datos for k in ["cuotas", "equipo", "jugadores", "eventos", "h2h"]):
            print(f"⚠️ Datos incompletos para partido {game_id}, se omite.")
            continue

        # 📝 Guarda los archivos en sus respectivas carpetas
        with open(os.path.join(carpetas["cuotas"], f"odds_{game_id}.json"), "w", encoding="utf-8") as f:
            json.dump(datos["cuotas"], f, indent=2)

        with open(os.path.join(carpetas["estadisticas_equipo"], f"{game_id}.json"), "w", encoding="utf-8") as f:
            json.dump(datos["equipo"], f, indent=2)

        with open(os.path.join(carpetas["estadisticas_jugadores"], f"{game_id}.json"), "w", encoding="utf-8") as f:
            json.dump(datos["jugadores"], f, indent=2)

        with open(os.path.join(carpetas["eventos"], f"{game_id}.json"), "w", encoding="utf-8") as f:
            json.dump(datos["eventos"], f, indent=2)

        with open(os.path.join(carpetas["h2h"], f"{game_id}.json"), "w", encoding="utf-8") as f:
            json.dump(datos["h2h"], f, indent=2)

        print(f"✅ Guardado: datos detallados de {game_id}")

    except Exception as e:
        print(f"❌ Error al procesar partido {game_id}: {e}")

print("🎯 Descarga completa por partido.")
