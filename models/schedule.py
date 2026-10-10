from .bus import Bus
from .route import Route


class Schedule:
    """Сущность расписания рейса."""

    def __init__(
        self,
        schedule_id: int,
        bus: Bus,
        route: Route,
        departure_time: str,
        is_cancelled: bool = False,
    ) -> None:
        self.id = schedule_id
        self.bus = bus
        self.route = route
        self.departure_time = departure_time
        self.is_cancelled = is_cancelled

    @staticmethod
    def validate_time(time_str: str) -> bool:
        """Проверка формата времени (ЧЧ:ММ)."""
        parts = time_str.split(":")
        if len(parts) != 2:
            return False
        if not (parts[0].isdigit() and parts[1].isdigit()):
            return False
        h, m = int(parts[0]), int(parts[1])
        return 0 <= h <= 23 and 0 <= m <= 59

    @property
    def is_active(self) -> bool:
        """Свойство: активен ли рейс по расписанию."""
        return not self.is_cancelled

    def cancel(self) -> None:
        """Отмена рейса."""
        self.is_cancelled = True

    def restore(self) -> None:
        """Возобновление рейса."""
        self.is_cancelled = False

    def __str__(self) -> str:
        status = "ОТМЕНЕН" if self.is_cancelled else "АКТИВЕН"
        return (
            f"Рейс #{self.id}: Маршрут {self.route.name} | "
            f"Автобус {self.bus.plate} | Время: {self.departure_time} "
            f"[{status}]"
        )
