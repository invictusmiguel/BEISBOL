# sampro_v6/beisbol/scripts/generar_visual_parimpar.py

import os
import json
import datetime
from PIL import Image, ImageDraw, ImageFont

# 📅 Fecha actual
today = datetime.date.today().strftime("%Y-%m-%d")

# 📁 Rutas
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
pred_dir = os.path.join(base_dir, 'predicciones')
img_dir = os.path.join(base_dir, 'visuales', 'imagenes', 'parimpar')
os.makedirs(img_dir, exist_ok=True)

file_in = os.path.join(pred_dir, f"predicciones_parimpar_clasificadas_{today}.json")

if not os.path.exists(file_in):
    print("❌ No hay picks clasificados para PAR/IMPAR.")
    exit()

with open(file_in, "r", encoding="utf-8") as f:
    picks = json.load(f)

# 🎨 Fuentes
try:
    font_path = "arial.ttf"
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

    img = Image.new("RGB", (600, 260), color=(25, 25, 25))
    draw = ImageDraw.Draw(img)

    draw.text((20, 20), f"{equipos}", font=font_title, fill="white")
    draw.text((20, 80), f"🎯 Pick: {tipo}", font=font_text, fill="gold")
    draw.text((20, 120), f"💰 Cuota: {cuota}", font=font_text, fill="lightgreen")
    draw.text((20, 150), f"📊 Prob: {prob*100:.1f}%", font=font_text, fill="skyblue")
    draw.text((20, 180), f"📈 EV: {ev:+.3f}", font=font_text, fill="orange")
    draw.text((20, 210), f"⭐ Confianza: {confianza.upper()}", font=font_text, fill="cyan")

    nombre = f"{equipos.replace(' ', '_')}_{tipo.replace(' ', '_')}.png"
    ruta = os.path.join(img_dir, nombre)
    img.save(ruta)
    print(f"✅ Imagen guardada: {ruta}")

print("🎯 Visuales PAR/IMPAR generadas.")
