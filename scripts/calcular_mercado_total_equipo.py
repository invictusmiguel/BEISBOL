# sampro_v6/beisbol/scripts/calcular_mercado_total_equipo.py

import os
import json
import datetime
from scipy.stats import poisson

# 📅 Fecha actual
today = datetime.date.today().strftime("%Y-%m-%d")

# 📁 Rutas base
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
datos_dir = os.path.join(base_dir, 'datos')
procesado_dir = os.path.join(datos_dir, 'procesados')
cuotas_dir = os.path.join(datos_dir, 'mercados', 'total_equipo')
pred_dir = os.path.join(base_dir, 'predicciones')
os.makedirs(pred_dir, exist_ok=True)

# 📦 Lista de resultados finales
picks = []

for file in os.listdir(procesado_dir):
    if not file.startswith("avanzado_") or not file.endswith(".json"):
        continue

    path_proc = os.path.join(procesado_dir, file)
    with open(path_proc, "r", encoding="utf-8") as f:
        data = json.load(f)

    game_id = data["game_id"]
    home = data["home"]["team"]
    away = data["away"]["team"]
    λ_home = data["home"]["h2h_avg_runs_scored"]
    λ_away = data["away"]["h2h_avg_runs_scored"]
    fecha = data["fecha"]

    odds_file = os.path.join(cuotas_dir, f"total_equipo_{game_id}.json")
    if not os.path.exists(odds_file):
        continue

    with open(odds_file, "r", encoding="utf-8") as f_odds:
        mercado = json.load(f_odds)

    mercado_nombre = mercado.get("name", "").lower()

    # 🧠 Detectar equipo (home o away)
    if "home" in mercado_nombre:
        equipo = home
        λ = λ_home
    elif "away" in mercado_nombre:
        equipo = away
        λ = λ_away
    else:
        continue  # No sabemos a qué equipo pertenece

    for val in mercado.get("values", []):
        valor = val.get("value", "").lower()
        cuota = float(val["odd"])

        if "over" in valor:
            try:
                linea = float(valor.replace("over", "").strip())
            except:
                continue
            prob = round(1 - poisson.cdf(int(linea), λ), 4)
            ev = round((prob * cuota) - 1, 4)

            picks.append({
                "id": game_id,
                "fecha": fecha,
                "equipo": equipo,
                "λ_estimado": round(λ, 2),
                "pick": f"{equipo} OVER {linea}",
                "cuota": cuota,
                "probabilidad": prob,
                "valor_esperado": ev
            })

        elif "under" in valor:
            try:
                linea = float(valor.replace("under", "").strip())
            except:
                continue
            prob = round(poisson.cdf(int(linea), λ), 4)
            ev = round((prob * cuota) - 1, 4)

            picks.append({
                "id": game_id,
                "fecha": fecha,
                "equipo": equipo,
                "λ_estimado": round(λ, 2),
                "pick": f"{equipo} UNDER {linea}",
                "cuota": cuota,
                "probabilidad": prob,
                "valor_esperado": ev
            })

# 💾 Guardar resultados
out_file = os.path.join(pred_dir, f"predicciones_total_equipo_{today}.json")
with open(out_file, "w", encoding="utf-8") as f_out:
    json.dump(picks, f_out, ensure_ascii=False, indent=2)

print(f"✅ Predicciones TOTAL EQUIPO actualizadas y guardadas en: {out_file}")
