# sampro_v6/beisbol/scripts/generar_visual_ganador.py

import os
import json
import datetime
from PIL import Image, ImageDraw, ImageFont

# 📅 Fecha
today = datetime.date.today().strftime("%Y-%m-%d")

# 📁 Rutas
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
pred_dir = os.path.join(base_dir, 'predicciones')
img_dir = os.path.join(base_dir, 'visuales', 'imagenes', 'ganador')
os.makedirs(img_dir, exist_ok=True)

file_in = os.path.join(pred_dir, f"predicciones_ganador_clasificadas_{today}.json")

if not os.path.exists(file_in):
    print("❌ No se encontraron picks clasificados del mercado GANADOR.")
    exit()

with open(file_in, "r", encoding="utf-8") as f:
    picks = json.load(f)

# 🎨 Fuente y tamaños
try:
    font_path = "arial.ttf"  # Usa otra ruta si estás en Linux o Mac
    font_title = ImageFont.truetype(font_path, 32)
    font_text = ImageFont.truetype(font_path, 22)
except:
    font_title = font_text = ImageFont.load_default()

for pick in picks:
    favorito = pick["favorito"]
    home = pick["home"]
    away = pick["away"]
    cuota = pick["cuota"]
    p = pick["probabilidad_modelo"]
    ev = pick["valor_esperado"]
    confianza = pick.get("confianza", "media")

    # 🖼 Crear imagen base
    img = Image.new("RGB", (600, 300), color=(25, 25, 25))
    draw = ImageDraw.Draw(img)

    # 🖌 Títulos y textos
    draw.text((20, 20), f"{home} vs {away}", font=font_title, fill="white")
    draw.text((20, 80), f"🏅 Pick: {favorito}", font=font_text, fill="gold")
    draw.text((20, 120), f"💰 Cuota: {cuota}", font=font_text, fill="lightgreen")
    draw.text((20, 150), f"📊 Prob: {p*100:.1f}%", font=font_text, fill="lightblue")
    draw.text((20, 180), f"📈 EV: {ev:+.3f}", font=font_text, fill="orange")
    draw.text((20, 220), f"⭐ Confianza: {confianza.upper()}", font=font_text, fill="cyan")

    # 💾 Guardar imagen
    nombre_archivo = f"{home}_vs_{away}_ganador.png".replace(" ", "_")
    ruta = os.path.join(img_dir, nombre_archivo)
    img.save(ruta)
    print(f"✅ Imagen guardada: {ruta}")

print("🎯 Visuales del mercado GANADOR generadas.")
