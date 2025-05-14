# sampro_v6/beisbol/scripts/clasificar_mercado_overunder.py

import os
import json
import datetime

# 📅 Fecha
today = datetime.date.today().strftime("%Y-%m-%d")

# 📁 Rutas
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
pred_dir = os.path.join(base_dir, 'predicciones')

file_in = os.path.join(pred_dir, f"predicciones_overunder_{today}.json")
file_out = os.path.join(pred_dir, f"predicciones_overunder_clasificadas_{today}.json")

if not os.path.exists(file_in):
    print("❌ No se encontró el archivo de predicciones OVER/UNDER.")
    exit()

with open(file_in, "r", encoding="utf-8") as f:
    partidos = json.load(f)

clasificados = []

for p in partidos:
    over_ev = p.get("valor_esperado_over")
    under_ev = p.get("valor_esperado_under")

    if over_ev is not None:
        confianza = "descartado"
        if over_ev >= 0.1:
            confianza = "alta"
        elif over_ev >= 0.04:
            confianza = "media"

        if confianza != "descartado":
            clasificados.append({
                "id": p["id"],
                "fecha": p["fecha"],
                "pick": "OVER 9.5",
                "equipos": f'{p["home"]} vs {p["away"]}',
                "λ_total": p["λ_total"],
                "probabilidad": p["prob_over"],
                "cuota": p["cuota_over"],
                "valor_esperado": over_ev,
                "confianza": confianza
            })

    if under_ev is not None:
        confianza = "descartado"
        if under_ev >= 0.1:
            confianza = "alta"
        elif under_ev >= 0.04:
            confianza = "media"

        if confianza != "descartado":
            clasificados.append({
                "id": p["id"],
                "fecha": p["fecha"],
                "pick": "UNDER 9.5",
                "equipos": f'{p["home"]} vs {p["away"]}',
                "λ_total": p["λ_total"],
                "probabilidad": p["prob_under"],
                "cuota": p["cuota_under"],
                "valor_esperado": under_ev,
                "confianza": confianza
            })

# 💾 Guardar
with open(file_out, "w", encoding="utf-8") as f:
    json.dump(clasificados, f, ensure_ascii=False, indent=2)

print(f"✅ Clasificación OVER/UNDER completada: {len(clasificados)} picks guardados.")
