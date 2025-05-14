# sampro_v6/beisbol/scripts/procesar_datos_avanzados_beisbol.py

import os
import json
import datetime

# 📅 Fecha
today = datetime.date.today().strftime("%Y-%m-%d")

# 📁 Rutas
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
data_dir = os.path.join(base_dir, 'datos')
procesado_dir = os.path.join(data_dir, 'procesados')
os.makedirs(procesado_dir, exist_ok=True)

# 📄 Partidos del día
file_juegos = os.path.join(data_dir, "juegos_hoy.json")
if not os.path.exists(file_juegos):
    print("❌ No se encuentra juegos_hoy.json")
    exit()

with open(file_juegos, "r", encoding="utf-8") as f:
    juegos = json.load(f).get("response", [])

def extraer_pitcher_y_stats(stats_jugadores):
    # Encuentra el lanzador con más innings (supuesto abridor)
    pitchers = [
        j for j in stats_jugadores if j["position"].lower() in ["sp", "rp", "p"]
    ]
    if not pitchers:
        return None

    # Tomamos el de más entradas lanzadas como abridor
    pitcher_principal = sorted(pitchers, key=lambda p: p.get("statistics", {}).get("innings", 0), reverse=True)[0]
    stats = pitcher_principal.get("statistics", {})
    return {
        "nombre": pitcher_principal["player"]["name"],
        "ERA": float(stats.get("ERA", 4.5)),
        "WHIP": float(stats.get("WHIP", 1.35)),
        "K9": float(stats.get("SO/9", 7.5)),
        "AVG": float(stats.get("AVG", 0.25))
    }

def calcular_promedios_h2h(partidos, id_equipo, rival_id):
    runs_scored = []
    runs_received = []

    for p in partidos:
        if p["teams"]["home"]["id"] == id_equipo:
            runs_scored.append(p["scores"]["home"]["total"])
            runs_received.append(p["scores"]["away"]["total"])
        elif p["teams"]["away"]["id"] == id_equipo:
            runs_scored.append(p["scores"]["away"]["total"])
            runs_received.append(p["scores"]["home"]["total"])

    promedio_anotado = round(sum(runs_scored) / len(runs_scored), 2) if runs_scored else 4.0
    promedio_concedido = round(sum(runs_received) / len(runs_received), 2) if runs_received else 4.0

    return promedio_anotado, promedio_concedido

# 📌 Procesar partido por partido
for partido in juegos:
    game_id = partido["id"]
    id_home = partido["teams"]["home"]["id"]
    id_away = partido["teams"]["away"]["id"]
    nombre_home = partido["teams"]["home"]["name"]
    nombre_away = partido["teams"]["away"]["name"]

    # 📥 Leer estadísticas de jugadores
    path_stats = os.path.join(data_dir, f"estadisticas_jugadores/{game_id}.json")
    if not os.path.exists(path_stats):
        print(f"❌ No stats jugadores para {game_id}")
        continue

    with open(path_stats, "r", encoding="utf-8") as f:
        stats_raw = json.load(f).get("response", [])

    stats_dict = {entry["team"]["id"]: entry.get("players", []) for entry in stats_raw}

    pitcher_home = extraer_pitcher_y_stats(stats_dict.get(id_home, [])) or {}
    pitcher_away = extraer_pitcher_y_stats(stats_dict.get(id_away, [])) or {}

    # 📥 Leer H2H
    path_h2h = os.path.join(data_dir, f"h2h/{game_id}.json")
    if not os.path.exists(path_h2h):
        print(f"❌ No H2H para {game_id}")
        continue

    with open(path_h2h, "r", encoding="utf-8") as f:
        h2h_data = json.load(f).get("response", [])

    avg_home_scored, avg_home_received = calcular_promedios_h2h(h2h_data, id_home, id_away)
    avg_away_scored, avg_away_received = calcular_promedios_h2h(h2h_data, id_away, id_home)

    # 🧠 JSON final
    data = {
        "game_id": game_id,
        "fecha": partido["date"],
        "home": {
            "team": nombre_home,
            "pitcher": pitcher_home,
            "h2h_avg_runs_scored": avg_home_scored,
            "h2h_avg_runs_allowed": avg_home_received
        },
        "away": {
            "team": nombre_away,
            "pitcher": pitcher_away,
            "h2h_avg_runs_scored": avg_away_scored,
            "h2h_avg_runs_allowed": avg_away_received
        }
    }

    output_path = os.path.join(procesado_dir, f"avanzado_{game_id}.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ Procesado: {output_path}")
