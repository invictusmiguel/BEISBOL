# sampro_v6/beisbol/scripts/calcular_mercado_primera_mitad.py

import os
import json
import datetime
from scipy.stats import poisson

# 📅 Fecha
today = datetime.date.today().strftime("%Y-%m-%d")

# 📁 Rutas
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
procesado_dir = os.path.join(base_dir, 'datos', 'procesados')
cuotas_dir = os.path.join(base_dir, 'datos', 'mercados', 'primera_mitad')
pred_dir = os.path.join(base_dir, 'predicciones')
os.makedirs(pred_dir, exist_ok=True)

picks = []

for file in os.listdir(procesado_dir):
    if not file.startswith("avanzado_") or not file.endswith(".json"):
        continue

    with open(os.path.join(procesado_dir, file), "r", encoding="utf-8") as f:
        data = json.load(f)

    game_id = data["game_id"]
    home = data["home"]["team"]
    away = data["away"]["team"]
    λ_home = data["home"]["h2h_avg_runs_scored"] * 5 / 9
    λ_away = data["away"]["h2h_avg_runs_scored"] * 5 / 9
    fecha = data["fecha"]

    prob_home_win_1h = 0
    prob_away_win_1h = 0

    for x in range(0, 10):
        for y in range(0, 10):
            p_x = poisson.pmf(x, λ_home)
            p_y = poisson.pmf(y, λ_away)
            if x > y:
                prob_home_win_1h += p_x * p_y
            elif y > x:
                prob_away_win_1h += p_x * p_y

    prob_home_win_1h = round(prob_home_win_1h, 4)
    prob_away_win_1h = round(prob_away_win_1h, 4)

    # 🧪 Cuotas (genéricas si no hay reales)
    cuota_home = 1.95
    cuota_away = 1.95

    odds_file = os.path.join(cuotas_dir, f"primera_mitad_{game_id}.json")
    if os.path.exists(odds_file):
        with open(odds_file, "r", encoding="utf-8") as f:
            mercado = json.load(f)
            for v in mercado.get("values", []):
                val = v["value"].lower()
                if home.lower() in val:
                    cuota_home = float(v["odd"])
                elif away.lower() in val:
                    cuota_away = float(v["odd"])

    ev_home = round(prob_home_win_1h * cuota_home - 1, 4)
    ev_away = round(prob_away_win_1h * cuota_away - 1, 4)

    picks.append({
        "id": game_id,
        "fecha": fecha,
        "home": home,
        "away": away,
        "λ_home_1h": round(λ_home, 2),
        "λ_away_1h": round(λ_away, 2),
        "prob_home_win_1h": prob_home_win_1h,
        "prob_away_win_1h": prob_away_win_1h,
        "cuota_home": cuota_home,
        "cuota_away": cuota_away,
        "valor_esperado_home": ev_home,
        "valor_esperado_away": ev_away
    })

# 💾 Guardar
out_file = os.path.join(pred_dir, f"predicciones_primera_mitad_{today}.json")
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(picks, f, ensure_ascii=False, indent=2)

print(f"✅ Predicciones PRIMERA MITAD guardadas en: {out_file}")
