# sampro_v6/beisbol/scripts/clasificar_confianza_beisbol.py

import os
import json
import datetime

# 📅 Fecha
today = datetime.date.today().strftime("%Y-%m-%d")

# 📁 Rutas
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
pred_dir = os.path.join(base_dir, 'predicciones')

# 📄 Archivos
file_pred = os.path.join(pred_dir, f"predicciones_beisbol_{today}.json")
file_out = os.path.join(pred_dir, f"predicciones_clasificadas_{today}.json")

if not os.path.exists(file_pred):
    print("❌ No se encontraron predicciones para hoy.")
    exit()

with open(file_pred, "r", encoding="utf-8") as f:
    predicciones = json.load(f)

clasificadas = []

for pick in predicciones:
    delta = pick["diferencial"]
    valor = pick.get("valor_esperado")

    confianza = "descartado"

    if abs(delta) >= 1.5 or (valor is not None and valor > 0.1):
        confianza = "alta"
    elif 0.8 <= abs(delta) < 1.5:
        confianza = "media"

    pick["confianza"] = confianza

    if confianza != "descartado":
        clasificadas.append(pick)

# 💾 Guardar archivo
with open(file_out, "w", encoding="utf-8") as f:
    json.dump(clasificadas, f, ensure_ascii=False, indent=2)

print(f"✅ Clasificación completada: {len(clasificadas)} picks guardados en {file_out}")
