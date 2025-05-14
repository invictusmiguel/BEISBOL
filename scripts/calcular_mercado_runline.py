# sampro_v6/beisbol/scripts/calcular_mercado_runline.py

import os
import json
import datetime
from scipy.stats import poisson

# 📅 Fecha actual
today = datetime.date.today().strftime("%Y-%m-%d")

# 📁 Rutas
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
procesado_dir = os.path.join(base_dir, 'datos', 'procesados')
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
    λ_home = data["home"]["h2h_avg_runs_scored"]
    λ_away = data["away"]["h2h_avg_runs_scored"]
    fecha = data["fecha"]

    # Probabilidades con Poisson
    p_home_cover = 0.0  # Home -1.5
    p_away_cover = 0.0  # Away +1.5

    for x in range(0, 15):
        for y in range(0, 15):
            prob = poisson.pmf(x, λ_home) * poisson.pmf(y, λ_away)
            if (x - y) >= 2:
                p_home_cover += prob
            if (x - y) >= -1:
                p_away_cover += prob

    p_home_cover = round(p_home_cover, 4)
    p_away_cover = round(p_away_cover, 4)

    # Cuotas base
    cuota_home = 1.90
    cuota_away = 1.90

    ev_home = round(p_home_cover * cuota_home - 1, 4)
    ev_away = round(p_away_cover * cuota_away - 1, 4)

    picks.append({
        "id": game_id,
        "fecha": fecha,
        "equipos": f"{home} vs {away}",
        "λ_home": round(λ_home, 2),
        "λ_away": round(λ_away, 2),
        "prob_home_-1.5": p_home_cover,
        "prob_away_+1.5": p_away_cover,
        "cuota_home_-1.5": cuota_home,
        "cuota_away_+1.5": cuota_away,
        "valor_esperado_home": ev_home,
        "valor_esperado_away": ev_away
    })

# 💾 Guardar
file_out = os.path.join(pred_dir, f"predicciones_runline_{today}.json")
with open(file_out, "w", encoding="utf-8") as f:
    json.dump(picks, f, ensure_ascii=False, indent=2)

print(f"✅ Predicciones RUN LINE guardadas en: {file_out}")
