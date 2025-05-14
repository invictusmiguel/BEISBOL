# sampro_v6/beisbol/scripts/calcular_mercado_overunder.py

import os
import json
import datetime
from scipy.stats import poisson

# 📅 Fecha
today = datetime.date.today().strftime("%Y-%m-%d")

# 📁 Rutas
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
datos_dir = os.path.join(base_dir, 'datos')
procesado_dir = os.path.join(datos_dir, 'procesados')
cuotas_dir = os.path.join(datos_dir, 'mercados', 'overunder')
pred_dir = os.path.join(base_dir, 'predicciones')
os.makedirs(pred_dir, exist_ok=True)

# 🏷 Línea por defecto
linea_total = 9.5

resultados = []

for file in os.listdir(procesado_dir):
    if not file.startswith("avanzado_") or not file.endswith(".json"):
        continue

    path = os.path.join(procesado_dir, file)
    with open(path, "r", encoding="utf-8") as f:
        datos = json.load(f)

    game_id = datos["game_id"]
    home = datos["home"]["team"]
    away = datos["away"]["team"]
    fecha = datos["fecha"]

    λ_home = datos["home"]["h2h_avg_runs_scored"]
    λ_away = datos["away"]["h2h_avg_runs_scored"]
    λ_total = round(λ_home + λ_away, 2)

    p_over = round(1 - poisson.cdf(int(linea_total), λ_total), 4)
    p_under = round(poisson.cdf(int(linea_total), λ_total), 4)

    # Cuotas (si están)
    odds_file = os.path.join(cuotas_dir, f"overunder_{game_id}.json")
    cuota_over = cuota_under = None
    ev_over = ev_under = None

    if os.path.exists(odds_file):
        with open(odds_file, "r", encoding="utf-8") as f_odds:
            mercado = json.load(f_odds)
            for val in mercado.get("values", []):
                if "over" in val["value"].lower():
                    cuota_over = float(val["odd"])
                elif "under" in val["value"].lower():
                    cuota_under = float(val["odd"])

    if cuota_over:
        ev_over = round((p_over * cuota_over) - 1, 3)
    if cuota_under:
        ev_under = round((p_under * cuota_under) - 1, 3)

    resultados.append({
        "id": game_id,
        "fecha": fecha,
        "home": home,
        "away": away,
        "λ_home": λ_home,
        "λ_away": λ_away,
        "λ_total": λ_total,
        "prob_over": p_over,
        "prob_under": p_under,
        "cuota_over": cuota_over,
        "cuota_under": cuota_under,
        "valor_esperado_over": ev_over,
        "valor_esperado_under": ev_under
    })

# 💾 Guardar
out_file = os.path.join(pred_dir, f"predicciones_overunder_{today}.json")
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(resultados, f, ensure_ascii=False, indent=2)

print(f"✅ Predicciones OVER/UNDER guardadas en: {out_file}")
