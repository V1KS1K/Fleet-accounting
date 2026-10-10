from typing import List, Optional
from .stop import Stop


class Route:
    """Сущность маршрута следования."""

    def __init__(
        self,
        route_id: int,
        name: str,
        stops: Optional[List[Stop]] = None,
    ) -> None:
        self.id = route_id
        self.name = name
        self.stops = stops if stops is not None else []

    def get_stops_str(self) -> str:
        """Строковое перечисление остановок."""
        if not self.stops:
            return "Остановок нет."
        return ", ".join([stop.name for stop in self.stops]) + "."

    def __str__(self) -> str:
        return f"Маршрут '{self.name}' (ID: {self.id})"