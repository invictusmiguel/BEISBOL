# sampro_v6/beisbol/scripts/clasificar_mercado_parimpar.py

import os
import json
import datetime

# 📅 Fecha
today = datetime.date.today().strftime("%Y-%m-%d")

# 📁 Rutas
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
pred_dir = os.path.join(base_dir, 'predicciones')

file_in = os.path.join(pred_dir, f"predicciones_parimpar_{today}.json")
file_out = os.path.join(pred_dir, f"predicciones_parimpar_clasificadas_{today}.json")

if not os.path.exists(file_in):
    print("❌ No se encontró el archivo de predicciones PAR/IMPAR.")
    exit()

with open(file_in, "r", encoding="utf-8") as f:
    picks = json.load(f)

clasificados = []

for p in picks:
    # Par
    ev_par = p["valor_esperado_par"]
    if ev_par >= 0.10:
        confianza = "alta"
    elif ev_par >= 0.04:
        confianza = "media"
    else:
        confianza = "descartado"

    if confianza != "descartado":
        clasificados.append({
            "id": p["id"],
            "fecha": p["fecha"],
            "pick": "TOTAL PAR",
            "equipos": p["equipos"],
            "λ_total": p["λ_total"],
            "cuota": p["cuota_par"],
            "probabilidad": p["prob_par"],
            "valor_esperado": ev_par,
            "confianza": confianza
        })

    # Impar
    ev_impar = p["valor_esperado_impar"]
    if ev_impar >= 0.10:
        confianza = "alta"
    elif ev_impar >= 0.04:
        confianza = "media"
    else:
        confianza = "descartado"

    if confianza != "descartado":
        clasificados.append({
            "id": p["id"],
            "fecha": p["fecha"],
            "pick": "TOTAL IMPAR",
            "equipos": p["equipos"],
            "λ_total": p["λ_total"],
            "cuota": p["cuota_impar"],
            "probabilidad": p["prob_impar"],
            "valor_esperado": ev_impar,
            "confianza": confianza
        })

# 💾 Guardar
with open(file_out, "w", encoding="utf-8") as f:
    json.dump(clasificados, f, ensure_ascii=False, indent=2)

print(f"✅ Clasificación PAR/IMPAR completada: {len(clasificados)} picks guardados.")
