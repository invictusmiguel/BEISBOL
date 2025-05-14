# sampro_v6/beisbol/scripts/clasificar_mercado_runline.py

import os
import json
import datetime

# 📅 Fecha
today = datetime.date.today().strftime("%Y-%m-%d")

# 📁 Rutas
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
pred_dir = os.path.join(base_dir, 'predicciones')

file_in = os.path.join(pred_dir, f"predicciones_runline_{today}.json")
file_out = os.path.join(pred_dir, f"predicciones_runline_clasificadas_{today}.json")

if not os.path.exists(file_in):
    print("❌ No se encontró el archivo de predicciones RUN LINE.")
    exit()

with open(file_in, "r", encoding="utf-8") as f:
    picks = json.load(f)

clasificados = []

for p in picks:
    # 🏠 Home -1.5
    ev_h = p["valor_esperado_home"]
    if ev_h >= 0.10:
        confianza = "alta"
    elif ev_h >= 0.04:
        confianza = "media"
    else:
        confianza = "descartado"

    if confianza != "descartado":
        clasificados.append({
            "id": p["id"],
            "fecha": p["fecha"],
            "pick": f"{p['equipos'].split(' vs ')[0]} -1.5",
            "equipos": p["equipos"],
            "cuota": p["cuota_home_-1.5"],
            "probabilidad": p["prob_home_-1.5"],
            "valor_esperado": ev_h,
            "confianza": confianza
        })

    # 🧳 Away +1.5
    ev_a = p["valor_esperado_away"]
    if ev_a >= 0.10:
        confianza = "alta"
    elif ev_a >= 0.04:
        confianza = "media"
    else:
        confianza = "descartado"

    if confianza != "descartado":
        clasificados.append({
            "id": p["id"],
            "fecha": p["fecha"],
            "pick": f"{p['equipos'].split(' vs ')[1]} +1.5",
            "equipos": p["equipos"],
            "cuota": p["cuota_away_+1.5"],
            "probabilidad": p["prob_away_+1.5"],
            "valor_esperado": ev_a,
            "confianza": confianza
        })

# 💾 Guardar
with open(file_out, "w", encoding="utf-8") as f:
    json.dump(clasificados, f, ensure_ascii=False, indent=2)

print(f"✅ Clasificación RUN LINE completada: {len(clasificados)} picks guardados.")
