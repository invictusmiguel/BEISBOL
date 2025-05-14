# sampro_v6/beisbol/scripts/clasificar_mercado_total_equipo.py

import os
import json
import datetime

# 📅 Fecha
today = datetime.date.today().strftime("%Y-%m-%d")

# 📁 Rutas
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
pred_dir = os.path.join(base_dir, 'predicciones')

file_in = os.path.join(pred_dir, f"predicciones_total_equipo_{today}.json")
file_out = os.path.join(pred_dir, f"predicciones_total_equipo_clasificadas_{today}.json")

if not os.path.exists(file_in):
    print("❌ No se encontró el archivo de predicciones TOTAL EQUIPO.")
    exit()

with open(file_in, "r", encoding="utf-8") as f:
    picks = json.load(f)

clasificados = []

for p in picks:
    ev = p["valor_esperado"]
    confianza = "descartado"

    if ev >= 0.10:
        confianza = "alta"
    elif ev >= 0.04:
        confianza = "media"

    if confianza != "descartado":
        p["confianza"] = confianza
        clasificados.append(p)

# 💾 Guardar
with open(file_out, "w", encoding="utf-8") as f:
    json.dump(clasificados, f, ensure_ascii=False, indent=2)

print(f"✅ Clasificación TOTAL EQUIPO completada: {len(clasificados)} picks guardados.")
