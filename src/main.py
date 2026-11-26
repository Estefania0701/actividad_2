from src.knowledge_base import (
    get_all_stations,
    get_transfer_stations
)

from src.route_engine import find_best_route


def display_system_information():
    """Muestra información general sobre el sistema de transporte."""

    stations = get_all_stations()
    transfers = get_transfer_stations()

    print("\n========== NEXUS METRO ==========")
    print("Ciudad: Nova City")
    print("Líneas de transporte: 3")
    print(f"Estaciones únicas: {len(stations)}")
    print(f"Estaciones de transbordo: {len(transfers)}")

    print("\nEstaciones disponibles:")

    for station in stations:
        print(f"- {station}")

    print("=================================")


def display_route(route):
    """Muestra la ruta seleccionada y sus detalles."""

    print("\n========== RESULTADO DE LA RUTA ==========")

    print(f"Origen: {route['origin']}")
    print(f"Destino: {route['destination']}")

    print("\nRuta seleccionada:")

    print(" -> ".join(route["station_path"]))

    print("\nInstrucciones de viaje:")

    for step in route["steps"]:

        if step["type"] == "ride":
            print(
                f"Tomar {step['from_line']}: "
                f"{step['station']} -> {step['destination']} "
                f"({step['minutes']} min)"
            )

        else:
            print(
                f"Transbordo en {step['station']}: "
                f"{step['from_line']} -> {step['to_line']} "
                f"({step['minutes']} min)"
            )

    print("\nTiempo total de viaje:", route["total_minutes"], "minutos")
    print("Número de transbordos:", route["transfers"])

    print("==========================================")


def main():
    """Ejecuta la aplicación."""

    display_system_information()

    origin = input("\nIngrese la estación de origen: ")
    destination = input("Ingrese la estación de destino: ")

    try:
        route = find_best_route(origin, destination)
        display_route(route)

    except ValueError as error:
        print(f"\nError: {error}")


if __name__ == "__main__":
    main()
