LINES = {
    "Línea Central": [
        "Aurora",
        "Central Park",
        "Distrito Financiero",
        "Plaza Mayor",
        "Universidad",
        "Puerto Norte"
    ],
    "Línea Costera": [
        "Bahía Sur",
        "Jardines",
        "Plaza Mayor",
        "Museo",
        "Estadio",
        "Puerto Norte"
    ],
    "Línea Universitaria": [
        "Bosque Este",
        "Universidad",
        "Mercado Central",
        "Museo",
        "Aeropuerto",
        "Colinas"
    ]
}

# Tiempo estimado de viaje entre estaciones consecutivas.
# El orden coincide con las estaciones de cada línea.

TRAVEL_TIMES = {
    "Línea Central": [4, 5, 4, 3, 5],
    "Línea Costera": [5, 4, 6, 5, 4],
    "Línea Universitaria": [6, 5, 4, 6, 5]
}

TRANSFER_TIME = 4


def get_all_stations():
    """Retorna todas las estaciones únicas del sistema."""
    return sorted({
        station
        for stations in LINES.values()
        for station in stations
    })


def get_station_lines(station):
    """Retorna las líneas que pasan por una estación determinada."""
    return [
        line
        for line, stations in LINES.items()
        if station in stations
    ]


def is_transfer_station(station):
    """Verifica si una estación conecta dos o más líneas."""
    return len(get_station_lines(station)) > 1


def get_transfer_stations():
    """Retorna todas las estaciones donde los pasajeros pueden hacer transbordo."""
    return [
        station
        for station in get_all_stations()
        if is_transfer_station(station)
    ]


def resolve_station(name):
    """Encuentra una estación sin distinguir entre mayúsculas y minúsculas."""
    for station in get_all_stations():
        if station.casefold() == name.strip().casefold():
            return station

    raise ValueError(f"La estación '{name}' no existe.")
