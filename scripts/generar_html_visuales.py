# generate_visual.py
import os
import json
from datetime import datetime

def generar_html(fecha=None):
    if not fecha:
        fecha = datetime.today().strftime("%Y-%m-%d")

    base = os.path.dirname(os.path.abspath(__file__))
    ruta_json = os.path.join(base, "beisbol", "predicciones", f"predicciones_ganador_clasificadas_{fecha}.json")
    ruta_html = os.path.join(base, "beisbol", "visuales", f"picks_visuales_{fecha}.html")

    if not os.path.exists(ruta_json):
        return False, f"⛔ No se encuentra el JSON: {ruta_json}"

    with open(ruta_json, "r", encoding="utf-8") as f:
        picks = json.load(f)

    picks.sort(key=lambda x: x["probabilidad_real"], reverse=True)

    html = f"""<!DOCTYPE html>
<html lang="es"><head>
    <meta charset="UTF-8">
    <title>Picks Visuales {fecha}</title>
    <style>
        body {{ background: #111; color: #fff; font-family: Arial; padding: 20px; }}
        h1 {{ color: #00ffff; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th, td {{ padding: 10px; border: 1px solid #333; text-align: center; }}
        th {{ background: #222; }}
        td:first-child {{ text-align: left; }}
    </style>
</head><body>
    <h1>📊 Picks Visuales — {fecha}</h1>
    <table><tr><th>Partido</th><th>Confianza</th><th>Probabilidad</th></tr>"""

    for p in picks:
        html += f"""
        <tr>
            <td>{p['partido']}</td>
            <td style='color:{"lime" if p["confianza"]=="ALTA" else "orange"}'>{p["confianza"]}</td>
            <td>{round(p["probabilidad_real"] * 100, 1)}%</td>
        </tr>"""

    html += "</table></body></html>"

    with open(ruta_html, "w", encoding="utf-8") as f:
        f.write(html)

    return True, f"✅ Visual generado: {ruta_html}"
