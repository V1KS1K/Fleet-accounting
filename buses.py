from typing import Optional


class Stop:
    """Остановка общественного транспорта."""
    def __init__(self, stop_id: int, name: str) -> None:
        self.id = stop_id
        self.name = name

    def __str__(self) -> str:
        return self.name


class Route:
    """Маршрут, состоящий из объектов остановок."""
    def __init__(self, route_id: int, name: str, stops: list[Stop]) -> None:
        self.id = route_id
        self.name = name
        self.stops = stops  # Здесь лежат объекты Stop, а не строки!

    def get_stops_str(self) -> str:
        if not self.stops:
            return "Остановок нет."
        return ", ".join([stop.name for stop in self.stops]) + "."

    def __str__(self) -> str:
        return f"Маршрут '{self.name}' (ID: {self.id})"


class Driver:
    """Водитель автобуса."""
    def __init__(self, driver_id: int, name: str) -> None:
        self.id = driver_id
        self.name = name

    def __str__(self) -> str:
        return self.name


class Bus:
    """Объект автобуса со ссылками на маршрут и водителя."""
    def __init__(self, bus_id: int, plate: str, route: Optional[Route], driver: Optional[Driver], on_the_way: bool) -> None:
        self.id = bus_id
        self.plate = plate
        self.route = route      
        self.driver = driver    
        self.on_the_way = on_the_way

    def get_route_status(self) -> str:
        return "Автобус в пути" if self.on_the_way else "Автобус в автопарке"

    def __str__(self) -> str:
        route_info = self.route.name if self.route else "Без маршрута"
        driver_info = self.driver.name if self.driver else "Без водителя"
        return f"Автобус {self.plate} (Маршрут: {route_info}, Водитель: {driver_info})"


def find_bus(buses: list[Bus], query: str) -> list[Bus]:
    """Найти автобус по номеру маршрута."""
    return [bus for bus in buses if bus.route and query.lower() in bus.route.name.lower()]