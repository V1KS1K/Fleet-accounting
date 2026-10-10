class Driver:
    """Сущность водителя автобуса."""

    def __init__(self, driver_id: int, name: str) -> None:
        self.id = driver_id
        self.name = name

    def __str__(self) -> str:
        return self.name

    @classmethod
    def from_data(cls, data: dict) -> "Driver":
        return cls(driver_id=data["id"], name=data["name"])