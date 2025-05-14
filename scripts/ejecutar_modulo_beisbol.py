# sampro_v6/beisbol/scripts/ejecutar_modulo_beisbol.py

import subprocess

def run_script(nombre):
    print(f"\n🟡 Ejecutando: {nombre}")
    try:
        subprocess.run(["python", nombre], check=True)
    except subprocess.CalledProcessError:
        print(f"⛔ Error ejecutando {nombre}")

# ✅ 1. DESCARGA Y PROCESAMIENTO
run_script("descargar_datos_beisbol.py")
run_script("descargar_datos_por_partido_beisbol.py")
run_script("procesar_datos_avanzados_beisbol.py")

# ✅ 2. MERCADOS CON DATOS API
mercados_api = [
    "ganador",
    "overunder",
    "total_equipo",
    "primera_mitad",
    "parimpar",
    "btts"
]

for mercado in mercados_api:
    run_script(f"descargar_mercado_{mercado}.py")
    run_script(f"calcular_mercado_{mercado}.py")
    run_script(f"clasificar_mercado_{mercado}.py")
    run_script(f"generar_visual_{mercado}.py")

# ✅ 3. MERCADOS CALCULADOS (sin datos de API)
run_script("calcular_mercado_runline.py")
run_script("clasificar_mercado_runline.py")
run_script("generar_visual_runline.py")

# ✅ 4. HTML FINAL DE PICKS TOTAL EQUIPO
run_script("generar_html_visuales_total_equipo.py")

# ✅ 5. NUEVO HTML GLOBAL DE TODOS LOS PICKS
run_script("generar_html_picks_completo.py")

print("\n✅ EJECUCIÓN COMPLETA DEL MÓDULO BÉISBOL.")
