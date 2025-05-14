from flask import Flask, request, send_file
import os
from scripts.generate_visual import generar_html  # ✅ Import correcto desde carpeta scripts

app = Flask(__name__)

@app.route('/')
def home():
    return "<h2>🏠 API Visual activa. Usa /visual?fecha=YYYY-MM-DD</h2>"

@app.route('/visual')
def visual():
    fecha = request.args.get('fecha')
    if not fecha:
        return "<h3>⛔ Falta parámetro ?fecha</h3>", 400

    archivo_html = f"picks_visuales_{fecha}.html"
    ruta_html = os.path.join("beisbol", "visuales", archivo_html)

    # 🔁 Generar si no existe
    if not os.path.exists(ruta_html):
        exito, mensaje = generar_html(fecha)
        if not exito:
            return f"<h3>{mensaje}</h3>", 404

    return send_file(ruta_html)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
