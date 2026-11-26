import heapq

from src.knowledge_base import (
    LINES,
    TRAVEL_TIMES,
    TRANSFER_TIME,
    get_all_stations,
    get_station_lines,
    resolve_station
)


def build_graph():
    """
    Construye un grafo ponderado utilizando la base de conocimiento.

    Reglas:
    1. Las estaciones consecutivas en la misma línea están conectadas.
    2. Las conexiones son bidireccionales.
    3. Los transbordos solo se permiten en estaciones compartidas.
    """

    graph = {}

    def add_connection(origin, destination, minutes, connection_type):
        graph.setdefault(origin, [])
        graph.setdefault(destination, [])

        graph[origin].append({
            "destination": destination,
            "minutes": minutes,
            "type": connection_type
        })

        graph[destination].append({
            "destination": origin,
            "minutes": minutes,
            "type": connection_type
        })

    # Regla 1: Conectar estaciones consecutivas en cada línea.
    for line, stations in LINES.items():
        times = TRAVEL_TIMES[line]

        for index in range(len(stations) - 1):
            origin = (stations[index], line)
            destination = (stations[index + 1], line)

            add_connection(
                origin,
                destination,
                times[index],
                "ride"
            )

    # Regla 2: Permitir transbordos solo en estaciones compartidas.
    for station in get_all_stations():
        station_lines = get_station_lines(station)

        for index in range(len(station_lines)):
            for other_index in range(index + 1, len(station_lines)):
                origin = (station, station_lines[index])
                destination = (station, station_lines[other_index])

                add_connection(
                    origin,
                    destination,
                    TRANSFER_TIME,
                    "transfer"
                )

    return graph


def find_best_route(origin, destination):
    """
    Encuentra la ruta con el menor tiempo total de viaje
    utilizando el algoritmo de Dijkstra.
    """

    origin = resolve_station(origin)
    destination = resolve_station(destination)

    # Caso especial: origen y destino son la misma estación.
    if origin == destination:
        return {
            "origin": origin,
            "destination": destination,
            "total_minutes": 0,
            "transfers": 0,
            "station_path": [origin],
            "steps": []
        }

    graph = build_graph()

    # Iniciar desde cada línea que pase por la estación de origen.
    start_nodes = [
        (origin, line)
        for line in get_station_lines(origin)
    ]

    distances = {}
    previous = {}

    priority_queue = []

    for node in start_nodes:
        distances[node] = 0
        heapq.heappush(priority_queue, (0, node))

    target = None

    # Algoritmo de Dijkstra.
    while priority_queue:
        current_distance, current_node = heapq.heappop(
            priority_queue
        )

        if current_distance != distances[current_node]:
            continue

        # Detenerse cuando se alcance el destino.
        if current_node[0] == destination:
            target = current_node
            break

        for connection in graph[current_node]:
            neighbor = connection["destination"]

            new_distance = (
                current_distance + connection["minutes"]
            )

            if new_distance < distances.get(neighbor, float("inf")):
                distances[neighbor] = new_distance

                previous[neighbor] = (
                    current_node,
                    connection
                )

                heapq.heappush(
                    priority_queue,
                    (new_distance, neighbor)
                )

    if target is None:
        raise ValueError("No existe una ruta entre estas estaciones.")

    # Reconstruir la ruta seleccionada.
    transitions = []
    current_node = target

    while current_node in previous:
        previous_node, connection = previous[current_node]

        transitions.append({
            "origin": previous_node,
            "destination": current_node,
            "type": connection["type"],
            "minutes": connection["minutes"]
        })

        current_node = previous_node

    transitions.reverse()

    # Generar la secuencia de estaciones sin duplicados.
    station_path = [origin]

    for transition in transitions:
        station = transition["destination"][0]

        if station != station_path[-1]:
            station_path.append(station)

    # Contar transbordos.
    transfers = sum(
        1
        for transition in transitions
        if transition["type"] == "transfer"
    )

    return {
        "origin": origin,
        "destination": destination,
        "total_minutes": distances[target],
        "transfers": transfers,
        "station_path": station_path,
        "steps": [
            {
                "type": transition["type"],
                "station": transition["origin"][0],
                "destination": transition["destination"][0],
                "from_line": transition["origin"][1],
                "to_line": transition["destination"][1],
                "minutes": transition["minutes"]
            }
            for transition in transitions
        ]
    }
