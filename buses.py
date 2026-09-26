def get_route_status(bus: dict) -> str:
    """Проверяет, в пути ли автобус."""
    if bus.get("on_the_way"):
        return "Автобус в пути"
    return "Автобус в автопарке"


def get_bus_stops(bus: dict) -> str:
    """Возвращает список остановок строкой."""
    stops = bus.get("stops", [])
    if not stops:
        return "Остановок нет."
    return ", ".join(stops) + "."


def find_bus(buses: list[dict], query: str) -> list[dict]:
    """Найти маршрут по названию."""
    return [bus for bus in buses if query.lower() in bus.get("name", "").lower()]