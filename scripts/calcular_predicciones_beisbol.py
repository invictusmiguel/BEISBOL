# sampro_v6/beisbol/scripts/calcular_predicciones_beisbol.py

import os
import json
import datetime

# 📅 Fecha
today = datetime.date.today().strftime("%Y-%m-%d")

# 📁 Rutas
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
data_dir = os.path.join(base_dir, 'datos')
procesado_dir = os.path.join(data_dir, 'procesados')
pred_dir = os.path.join(base_dir, 'predicciones')
os.makedirs(pred_dir, exist_ok=True)

predicciones = []

def calcular_lambda(pitcher_rival, h2h_runs, obp_estimado=0.310):
    # ⚙️ Ajuste de predicción avanzada
    era = pitcher_rival.get("ERA", 4.5)
    whip = pitcher_rival.get("WHIP", 1.3)
    avg = pitcher_rival.get("AVG", 0.25)
    k9 = pitcher_rival.get("K9", 7.5)

    # 🔮 Fórmula avanzada con componentes: OBP, ERA, WHIP, AVG, H2H
    λ = (obp_estimado * 14) - (era * 0.6) - (avg * 2) - (whip * 0.5) + (h2h_runs * 0.2)
    return round(max(λ, 1.5), 2)  # mínimo 1.5 carreras para evitar negativos

# 📦 Leer todos los partidos procesados
for file in os.listdir(procesado_dir):
    if not file.startswith("avanzado_") or not file.endswith(".json"):
        continue

    path = os.path.join(procesado_dir, file)
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    game_id = data["game_id"]
    home = data["home"]
    away = data["away"]

    λ_home = calcular_lambda(
        away["pitcher"],
        home["h2h_avg_runs_scored"]
    )

    λ_away = calcular_lambda(
        home["pitcher"],
        away["h2h_avg_runs_scored"]
    )

    diferencial = round(λ_home - λ_away, 2)
    favorito = home["team"] if diferencial > 0 else away["team"]

    # 💰 Buscar cuota si existe
    odds_file = os.path.join(data_dir, f"cuotas/odds_{game_id}.json")
    cuota = None
    valor_esperado = None

    if os.path.exists(odds_file):
        with open(odds_file, "r", encoding="utf-8") as f_odds:
            odds_data = json.load(f_odds).get("response", [])
            try:
                values = odds_data[0]["bookmakers"][0]["bets"][0]["values"]
                for o in values:
                    if o["value"] == favorito:
                        cuota = float(o["odd"])
                        break
            except:
                pass

    if cuota:
        prob_estimada = 0.55 if abs(diferencial) >= 1.5 else 0.5
        valor_esperado = round((prob_estimada * cuota) - 1, 3)

    predicciones.append({
        "id": game_id,
        "fecha": data["fecha"],
        "home": home["team"],
        "away": away["team"],
        "λ_home": λ_home,
        "λ_away": λ_away,
        "diferencial": diferencial,
        "favorito": favorito,
        "cuota": cuota,
        "valor_esperado": valor_esperado
    })

# 💾 Guardar archivo
out_file = os.path.join(pred_dir, f"predicciones_beisbol_{today}.json")
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(predicciones, f, ensure_ascii=False, indent=2)

print(f"✅ Predicciones calculadas y guardadas: {out_file}")
