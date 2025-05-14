# sampro_v6/beisbol/scripts/clasificar_mercado_ganador.py

import os
import json
import datetime

# 📅 Fecha
today = datetime.date.today().strftime("%Y-%m-%d")

# 📁 Rutas
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
pred_dir = os.path.join(base_dir, 'predicciones')

file_in = os.path.join(pred_dir, f"predicciones_ganador_{today}.json")
file_out = os.path.join(pred_dir, f"predicciones_ganador_clasificadas_{today}.json")

if not os.path.exists(file_in):
    print("❌ No se encontraron predicciones del mercado GANADOR.")
    exit()

with open(file_in, "r", encoding="utf-8") as f:
    picks = json.load(f)

clasificadas = []

for pick in picks:
    ev = pick.get("valor_esperado", 0)
    diferencial = abs(pick.get("diferencial", 0))

    confianza = "descartado"

    if ev >= 0.1 or diferencial >= 1.5:
        confianza = "alta"
    elif ev >= 0.04 or diferencial >= 0.8:
        confianza = "media"

    pick["confianza"] = confianza

    if confianza != "descartado":
        clasificadas.append(pick)

# 💾 Guardar archivo
with open(file_out, "w", encoding="utf-8") as f:
    json.dump(clasificadas, f, ensure_ascii=False, indent=2)

print(f"✅ Clasificación completada: {len(clasificadas)} picks guardados en {file_out}")
