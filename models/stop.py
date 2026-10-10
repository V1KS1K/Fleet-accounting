class Stop:
    """Сущность остановки общественного транспорта."""

    def __init__(self, stop_id: int, name: str) -> None:
        self.id = stop_id
        self.name = name

    def __str__(self) -> str:
        return self.name

    @classmethod
    def from_data(cls, data: dict) -> "Stop":
        return cls(stop_id=data["id"], name=data["name"])
