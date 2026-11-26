import pytest

from src.route_engine import find_best_route


def test_direct_route_without_transfers():
    """El sistema debe encontrar una ruta directa."""

    route = find_best_route("Aurora", "Puerto Norte")

    assert route["total_minutes"] == 21
    assert route["transfers"] == 0

    assert route["station_path"] == [
        "Aurora",
        "Central Park",
        "Distrito Financiero",
        "Plaza Mayor",
        "Universidad",
        "Puerto Norte"
    ]


def test_route_with_transfers():
    """El sistema debe considerar los costos de transbordo."""

    route = find_best_route("Aurora", "Colinas")

    assert route["transfers"] == 2
    assert route["total_minutes"] == 38

    assert "Plaza Mayor" in route["station_path"]
    assert "Museo" in route["station_path"]


def test_same_origin_and_destination():
    """El tiempo de viaje debe ser cero para la misma estación."""

    route = find_best_route("Universidad", "Universidad")

    assert route["total_minutes"] == 0
    assert route["transfers"] == 0
    assert route["station_path"] == ["Universidad"]


def test_invalid_station():
    """El sistema debe rechazar estaciones desconocidas."""

    with pytest.raises(ValueError):
        find_best_route("Unknown Station", "Aurora")
