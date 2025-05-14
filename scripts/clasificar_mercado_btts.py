# sampro_v6/beisbol/scripts/clasificar_mercado_btts.py

import os
import json
import datetime

# 📅 Fecha actual
today = datetime.date.today().strftime("%Y-%m-%d")

# 📁 Rutas
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
pred_dir = os.path.join(base_dir, 'predicciones')

file_in = os.path.join(pred_dir, f"predicciones_btts_{today}.json")
file_out = os.path.join(pred_dir, f"predicciones_btts_clasificadas_{today}.json")

if not os.path.exists(file_in):
    print("❌ No se encontró el archivo de predicciones BTTS.")
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
        clasificados.append({
            "id": p["id"],
            "fecha": p["fecha"],
            "equipos": f"{p['home']} vs {p['away']}",
            "λ_home": p["λ_home"],
            "λ_away": p["λ_away"],
            "cuota": p["cuota_btts"],
            "probabilidad": p["probabilidad_btts"],
            "valor_esperado": ev,
            "confianza": confianza,
            "pick": "Ambos anotan"
        })

# 💾 Guardar
with open(file_out, "w", encoding="utf-8") as f:
    json.dump(clasificados, f, ensure_ascii=False, indent=2)

print(f"✅ Clasificación BTTS completada: {len(clasificados)} picks guardados.")
