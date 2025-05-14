# sampro_v6/beisbol/scripts/calcular_mercado_ganador.py

import os
import json
import datetime

# 📅 Fecha
today = datetime.date.today().strftime("%Y-%m-%d")

# 📁 Rutas
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
datos_dir = os.path.join(base_dir, 'datos')
procesado_dir = os.path.join(datos_dir, 'procesados')
cuotas_dir = os.path.join(datos_dir, 'mercados', 'ganador')
pred_dir = os.path.join(base_dir, 'predicciones')
os.makedirs(pred_dir, exist_ok=True)

resultados = []

for file in os.listdir(procesado_dir):
    if not file.startswith("avanzado_") or not file.endswith(".json"):
        continue

    path_avanzado = os.path.join(procesado_dir, file)
    with open(path_avanzado, "r", encoding="utf-8") as f:
        datos = json.load(f)

    game_id = datos["game_id"]
    archivo_cuota = os.path.join(cuotas_dir, f"ganador_{game_id}.json")

    if not os.path.exists(archivo_cuota):
        print(f"⚠️ No hay cuota para partido {game_id}, se omite.")
        continue

    with open(archivo_cuota, "r", encoding="utf-8") as f:
        mercado = json.load(f)

    valores = mercado.get("values", [])
    if len(valores) < 2:
        print(f"⚠️ Cuotas incompletas para {game_id}")
        continue

    equipo1 = valores[0]["value"]
    cuota1 = float(valores[0]["odd"])
    equipo2 = valores[1]["value"]
    cuota2 = float(valores[1]["odd"])

    λ_home = datos["home"]["h2h_avg_runs_scored"]
    λ_away = datos["away"]["h2h_avg_runs_scored"]

    diferencial = round(λ_home - λ_away, 2)

    favorito = equipo1 if diferencial > 0 else equipo2
    cuota = cuota1 if favorito == equipo1 else cuota2

    # 🧠 Probabilidad estimada (modelo simple Poisson comparado)
    total = abs(λ_home) + abs(λ_away)
    p_modelo = round(abs(λ_home) / total, 3) if diferencial > 0 else round(abs(λ_away) / total, 3)

    # 📈 Probabilidad implícita y EV
    p_implícita = round(1 / cuota, 3)
    valor_esperado = round((p_modelo * cuota) - 1, 3)

    resultados.append({
        "id": game_id,
        "fecha": datos["fecha"],
        "home": datos["home"]["team"],
        "away": datos["away"]["team"],
        "favorito": favorito,
        "cuota": cuota,
        "probabilidad_modelo": p_modelo,
        "probabilidad_implícita": p_implícita,
        "valor_esperado": valor_esperado,
        "diferencial": diferencial
    })

# 💾 Guardar resultados
out_file = os.path.join(pred_dir, f"predicciones_ganador_{today}.json")
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(resultados, f, ensure_ascii=False, indent=2)

print(f"✅ Predicciones del mercado GANADOR guardadas en: {out_file}")
