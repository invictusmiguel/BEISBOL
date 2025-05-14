# sampro_v6/beisbol/scripts/calcular_mercado_btts.py

import os
import json
import datetime
from scipy.stats import poisson

# 📅 Fecha
today = datetime.date.today().strftime("%Y-%m-%d")

# 📁 Rutas
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
procesado_dir = os.path.join(base_dir, 'datos', 'procesados')
pred_dir = os.path.join(base_dir, 'predicciones')
os.makedirs(pred_dir, exist_ok=True)

picks = []

# 🧪 Supongamos cuota genérica
cuota_btts = 1.80

for file in os.listdir(procesado_dir):
    if not file.startswith("avanzado_") or not file.endswith(".json"):
        continue

    path = os.path.join(procesado_dir, file)
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    game_id = data["game_id"]
    home = data["home"]["team"]
    away = data["away"]["team"]
    λ_home = data["home"]["h2h_avg_runs_scored"]
    λ_away = data["away"]["h2h_avg_runs_scored"]
    fecha = data["fecha"]

    # 📊 Cálculo BTTS
    prob_home_anota = 1 - poisson.pmf(0, λ_home)
    prob_away_anota = 1 - poisson.pmf(0, λ_away)
    prob_btts = round(prob_home_anota * prob_away_anota, 4)

    ev = round((prob_btts * cuota_btts) - 1, 4)

    picks.append({
        "id": game_id,
        "fecha": fecha,
        "home": home,
        "away": away,
        "λ_home": round(λ_home, 2),
        "λ_away": round(λ_away, 2),
        "probabilidad_btts": prob_btts,
        "cuota_btts": cuota_btts,
        "valor_esperado": ev
    })

# 💾 Guardar
out_file = os.path.join(pred_dir, f"predicciones_btts_{today}.json")
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(picks, f, ensure_ascii=False, indent=2)

print(f"✅ Predicciones BTTS guardadas en: {out_file}")
