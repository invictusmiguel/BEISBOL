# sampro_v6/beisbol/scripts/generar_visual_overunder.py

import os
import json
import datetime
from PIL import Image, ImageDraw, ImageFont

# 📅 Fecha
today = datetime.date.today().strftime("%Y-%m-%d")

# 📁 Rutas
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
pred_dir = os.path.join(base_dir, 'predicciones')
img_dir = os.path.join(base_dir, 'visuales', 'imagenes', 'overunder')
os.makedirs(img_dir, exist_ok=True)

file_in = os.path.join(pred_dir, f"predicciones_overunder_clasificadas_{today}.json")

if not os.path.exists(file_in):
    print("❌ No se encontraron picks clasificados del mercado OVER/UNDER.")
    exit()

with open(file_in, "r", encoding="utf-8") as f:
    picks = json.load(f)

# 🎨 Fuentes
try:
    font_path = "arial.ttf"  # Cambia según tu sistema
    font_title = ImageFont.truetype(font_path, 30)
    font_text = ImageFont.truetype(font_path, 22)
except:
    font_title = font_text = ImageFont.load_default()

for pick in picks:
    equipos = pick["equipos"]
    tipo = pick["pick"]
    cuota = pick["cuota"]
    prob = pick["probabilidad"]
    ev = pick["valor_esperado"]
    confianza = pick["confianza"]

    img = Image.new("RGB", (600, 280), color=(18, 18, 18))
    draw = ImageDraw.Draw(img)

    draw.text((20, 20), f"{equipos}", font=font_title, fill="white")
    draw.text((20, 80), f"🎯 Pick: {tipo}", font=font_text, fill="gold")
    draw.text((20, 120), f"💰 Cuota: {cuota}", font=font_text, fill="lightgreen")
    draw.text((20, 150), f"📊 Prob: {prob*100:.1f}%", font=font_text, fill="skyblue")
    draw.text((20, 180), f"📈 EV: {ev:+.3f}", font=font_text, fill="orange")
    draw.text((20, 220), f"⭐ Confianza: {confianza.upper()}", font=font_text, fill="cyan")

    nombre = f"{equipos}_{tipo.replace(' ', '')}.png".replace(" ", "_")
    ruta = os.path.join(img_dir, nombre)
    img.save(ruta)
    print(f"✅ Imagen guardada: {ruta}")

print("🎯 Visuales del mercado OVER/UNDER generadas.")
