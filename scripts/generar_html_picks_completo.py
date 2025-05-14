import json
import os
import re
from datetime import datetime
from jinja2 import Template

# 📁 Ruta base absoluta del proyecto
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# 🌟 Buscar el archivo más reciente de predicciones clasificadas
def cargar_picks_clasificados():
    ruta_predicciones = os.path.join(BASE_DIR, "predicciones")

    if not os.path.exists(ruta_predicciones):
        print(f"⚠️ Carpeta no encontrada: {ruta_predicciones}")
        return [], None

    archivos = [f for f in os.listdir(ruta_predicciones) if "_clasificadas_" in f and f.endswith(".json")]

    archivos_con_fecha = []
    for f in archivos:
        match = re.search(r"_clasificadas_(\d{4}-\d{2}-\d{2})\.json", f)
        if match:
            archivos_con_fecha.append((f, match.group(1)))

    if not archivos_con_fecha:
        print("⚠️ No se encontraron archivos clasificados válidos.")
        return [], None

    archivos_ordenados = sorted(
        archivos_con_fecha,
        key=lambda x: datetime.strptime(x[1], "%Y-%m-%d"),
        reverse=True
    )

    archivo_mas_reciente, fecha = archivos_ordenados[0]
    ruta_archivo = os.path.join(ruta_predicciones, archivo_mas_reciente)

    try:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data, fecha
    except Exception as e:
        print(f"❌ Error al leer {archivo_mas_reciente}: {e}")
        return [], None

# ⏰ Cargar horas desde juegos_hoy.json
def cargar_horas_partidos():
    ruta_juegos = os.path.join(BASE_DIR, "datos", "juegos_hoy.json")
    if not os.path.exists(ruta_juegos):
        print(f"⚠️ Archivo no encontrado: {ruta_juegos}")
        return {}

    try:
        with open(ruta_juegos, "r", encoding="utf-8") as f:
            data = json.load(f)
        return {str(item["id"]): item.get("hora", "--:--") for item in data.get("response", [])}
    except Exception as e:
        print(f"❌ Error al cargar horas de partidos: {e}")
        return {}

# 🧱 Función principal para generar HTML
def generar_html():
    picks, fecha = cargar_picks_clasificados()
    if not picks:
        print("⚠️ No hay picks para mostrar.")
        return

    horas = cargar_horas_partidos()

    # ⏱️ Agregar hora a cada pick
    for pick in picks:
        pick["hora"] = horas.get(str(pick.get("id_partido")), "--:--")

    # 🧼 Filtrar picks válidos
    picks = [p for p in picks if all(k in p for k in ("partido", "pick", "probabilidad"))]

    # 🔢 Ordenar por probabilidad descendente
    picks.sort(key=lambda x: x.get("probabilidad", 0), reverse=True)

    # 🖼️ Plantilla HTML
    html_template = """
    <html>
    <head>
        <meta charset="utf-8">
        <title>Picks Clasificados</title>
        <style>
            body { background-color: black; color: lime; font-family: Arial; text-align: center; }
            table { width: 90%; margin: auto; border-collapse: collapse; }
            th, td { border: 1px solid #00FF00; padding: 8px; }
            th { background-color: #111; }
        </style>
    </head>
    <body>
        <h1>🎯 Picks Clasificados con Confianza — {{ fecha }}</h1>
        <table>
            <tr>
                <th>Partido</th>
                <th>Pick</th>
                <th>Probabilidad</th>
                <th>Cuota</th>
                <th>Valor Esperado</th>
                <th>Confianza</th>
                <th>Hora</th>
            </tr>
            {% for pick in picks %}
            <tr>
                <td>{{ pick.partido }}</td>
                <td>{{ pick.pick }}</td>
                <td>{{ "%.1f"|format(pick.probabilidad * 100) }}%</td>
                <td>{{ pick.cuota or "-" }}</td>
                <td>{{ "+%.3f"|format(pick.valor_esperado) if pick.valor_esperado >= 0 else "%.3f"|format(pick.valor_esperado) }}</td>
                <td>{{ pick.confianza or "-" }}</td>
                <td>{{ pick.hora or "--:--" }}</td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """

    template = Template(html_template)
    html = template.render(fecha=fecha, picks=picks)

    ruta_salida = os.path.join(BASE_DIR, "visuales", f"picks_completos_{fecha}.html")
    os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)

    with open(ruta_salida, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ HTML generado: {ruta_salida}")

# ▶️ Ejecutar como script principal
if __name__ == "__main__":
    generar_html()
