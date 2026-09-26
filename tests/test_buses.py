from buses import get_route_status, get_bus_stops


def test_get_route_status_on_way():
    bus = {"on_the_way": True}
    assert get_route_status(bus) == "Автобус в пути"


def test_get_route_status_in_park():
    bus = {"on_the_way": False}
    assert get_route_status(bus) == "Автобус в автопарке"


def test_get_bus_stops_exist():
    bus = {"stops": ["Остановка 1", "Остановка 2"]}
    assert get_bus_stops(bus) == "Остановка 1, Остановка 2."


def test_get_bus_stops_empty():
    bus = {"stops": []}
    assert get_bus_stops(bus) == "Остановок нет."


def find_bus(buses: list[dict], query: str) -> list[dict]:
    """Найти маршрут по названию."""
    return [bus for bus in buses if query.lower() in bus.get("name", "").lower()]