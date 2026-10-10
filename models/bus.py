from typing import Optional
from .driver import Driver
from .route import Route


class Bus:
    """Сущность автобуса автопарка."""

    def __init__(
        self,
        bus_id: int,
        plate: str,
        route: Optional[Route] = None,
        driver: Optional[Driver] = None,
        on_the_way: bool = False,
    ) -> None:
        self.id = bus_id
        self.plate = plate
        self.route = route
        self.driver = driver
        self.on_the_way = on_the_way

    @staticmethod
    def validate_plate(plate: str) -> bool:
        """Проверка корректности госномера."""
        return len(plate.strip()) >= 5

    @property
    def is_assigned(self) -> bool:
        """Свойство: назначен ли маршрут автобусу."""
        return self.route is not None

    def get_route_status(self) -> str:
        """Статус нахождения автобуса на линии."""
        return "Автобус в пути" if self.on_the_way else "Автобус в автопарке"

    def assign_to_route(
        self, route: Route, driver: Optional[Driver] = None
    ) -> None:
        """Назначение автобуса на маршрут и закрепление водителя."""
        self.route = route
        if driver is not None:
            self.driver = driver

    def release(self) -> None:
        """Снятие автобуса с маршрута."""
        self.route = None
        self.on_the_way = False

    def __str__(self) -> str:
        route_name = self.route.name if self.route else "Без маршрута"
        driver_name = self.driver.name if self.driver else "Без водителя"
        return (
            f"[{self.id}] Автобус {self.plate} | "
            f"Маршрут: {route_name} | Водитель: {driver_name} | "
            f"Статус: {self.get_route_status()}"
        )