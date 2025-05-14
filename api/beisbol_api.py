import requests
import time

API_KEY = "cef9115ecad4dcadf30573ca8c3d3abe"
BASE_URL = "https://v3.football.api-sports.io"
HEADERS = {
    "x-apisports-key": API_KEY
}

def get(endpoint, params=None):
    url = f"{BASE_URL}{endpoint}"
    try:
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Error en GET {url}: {e}")
        return None

# 🧠 Función principal que se importa
def obtener_datos_partido(game_id):
    datos = {}

    # 1. Cuotas
    odds = get("/odds", {"fixture": game_id})
    datos["cuotas"] = odds if odds else {}

    time.sleep(0.5)  # para no saturar la API

    # 2. Estadísticas por equipo
    stats_equipo = get("/fixtures/statistics", {"fixture": game_id})
    datos["equipo"] = stats_equipo if stats_equipo else {}

    time.sleep(0.5)

    # 3. Estadísticas de jugadores
    stats_jugadores = get("/fixtures/players", {"fixture": game_id})
    datos["jugadores"] = stats_jugadores if stats_jugadores else {}

    time.sleep(0.5)

    # 4. Eventos del partido
    eventos = get("/fixtures/events", {"fixture": game_id})
    datos["eventos"] = eventos if eventos else {}

    time.sleep(0.5)

    # 5. Head to Head (últimos enfrentamientos)
    h2h = get("/fixtures/headtohead", {"h2h": str(game_id)})
    datos["h2h"] = h2h if h2h else {}

    return datos
