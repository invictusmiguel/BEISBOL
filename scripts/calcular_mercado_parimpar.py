# sampro_v6/beisbol/scripts/calcular_mercado_parimpar.py

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

    path = os.path.join(procesado_dir, file)
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    game_id = data["game_id"]
    home = data["home"]["team"]
    away = data["away"]["team"]
    λ_home = data["home"]["h2h_avg_runs_scored"]
    λ_away = data["away"]["h2h_avg_runs_scored"]
    λ_total = λ_home + λ_away
    fecha = data["fecha"]

    # 🎲 Calcular probabilidad total PAR
    prob_par = 0.0
    for k in range(0, 40, 2):  # Solo pares
        prob_par += poisson.pmf(k, λ_total)

    prob_par = round(prob_par, 4)
    prob_impar = round(1 - prob_par, 4)

    # Cuotas genéricas
    cuota_par = 1.90
    cuota_impar = 1.90

    ev_par = round((prob_par * cuota_par) - 1, 4)
    ev_impar = round((prob_impar * cuota_impar) - 1, 4)

    picks.append({
        "id": game_id,
        "fecha": fecha,
        "equipos": f"{home} vs {away}",
        "λ_total": round(λ_total, 2),
        "prob_par": prob_par,
        "prob_impar": prob_impar,
        "cuota_par": cuota_par,
        "cuota_impar": cuota_impar,
        "valor_esperado_par": ev_par,
        "valor_esperado_impar": ev_impar
    })

# 💾 Guardar resultados
out_file = os.path.join(pred_dir, f"predicciones_parimpar_{today}.json")
with open(out_file, "w", encoding="utf-8") as f_out:
    json.dump(picks, f_out, ensure_ascii=False, indent=2)

print(f"✅ Predicciones PAR/IMPAR guardadas en: {out_file}")
