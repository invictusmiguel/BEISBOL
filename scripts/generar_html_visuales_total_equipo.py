# sampro_v6/beisbol/scripts/generar_html_visuales.py

import os
import datetime

# 📅 Fecha
today = datetime.date.today().strftime("%Y-%m-%d")

# 📁 Rutas
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
img_dir = os.path.join(base_dir, 'visuales', 'imagenes')
html_out = os.path.join(base_dir, 'visuales', f"picks_visuales_{today}.html")

mercados = ["ganador", "overunder", "runline", "total_equipo"]

# 🧱 HTML base
html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Picks Visuales {today}</title>
  <style>
    body {{
      background: #1c1c1c;
      color: white;
      font-family: sans-serif;
    }}
    h1 {{
      text-align: center;
      color: #ffd700;
    }}
    h2 {{
      margin-top: 40px;
      color: lightgreen;
    }}
    .galeria {{
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
    }}
    .galeria img {{
      width: 280px;
      border: 2px solid #444;
      border-radius: 10px;
    }}
    .contenedor {{
      margin: 20px;
    }}
  </style>
</head>
<body>
  <h1>📊 Picks Visuales Clasificados — {today}</h1>
"""

# 📸 Agregar imágenes por mercado
for mercado in mercados:
    ruta = os.path.join(img_dir, mercado)
    if not os.path.exists(ruta):
        continue

    html += f"<div class='contenedor'><h2>📌 Mercado: {mercado.upper()}</h2><div class='galeria'>\n"

    for file in sorted(os.listdir(ruta)):
        if file.endswith(".png"):
            rel_path = f"./imagenes/{mercado}/{file}"
            html += f'<img src="{rel_path}" alt="{file}">\n'

    html += "</div></div>\n"

html += "</body></html>"

# 💾 Guardar HTML
with open(html_out, "w", encoding="utf-8") as f:
    f.write(html)

print(f"✅ Página HTML generada: {html_out}")
