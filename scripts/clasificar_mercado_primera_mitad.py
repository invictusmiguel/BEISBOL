# sampro_v6/beisbol/scripts/clasificar_mercado_primera_mitad.py

import os
import json
import datetime

# 📅 Fecha
today = datetime.date.today().strftime("%Y-%m-%d")

# 📁 Rutas
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
pred_dir = os.path.join(base_dir, 'predicciones')

file_in = os.path.join(pred_dir, f"predicciones_primera_mitad_{today}.json")
file_out = os.path.join(pred_dir, f"predicciones_primera_mitad_clasificadas_{today}.json")

if not os.path.exists(file_in):
    print("❌ No se encontró el archivo de predicciones PRIMERA MITAD.")
    exit()

with open(file_in, "r", encoding="utf-8") as f:
    picks = json.load(f)

clasificados = []

for p in picks:
    # Home pick
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
            "pick": f"{p['home']} gana 1H",
            "equipos": f"{p['home']} vs {p['away']}",
            "λ": p["λ_home_1h"],
            "cuota": p["cuota_home"],
            "probabilidad": p["prob_home_win_1h"],
            "valor_esperado": ev_h,
            "confianza": confianza
        })

    # Away pick
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
            "pick": f"{p['away']} gana 1H",
            "equipos": f"{p['home']} vs {p['away']}",
            "λ": p["λ_away_1h"],
            "cuota": p["cuota_away"],
            "probabilidad": p["prob_away_win_1h"],
            "valor_esperado": ev_a,
            "confianza": confianza
        })

# 💾 Guardar
with open(file_out, "w", encoding="utf-8") as f:
    json.dump(clasificados, f, ensure_ascii=False, indent=2)

print(f"✅ Clasificación PRIMERA MITAD completada: {len(clasificados)} picks guardados.")
