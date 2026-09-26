import json
import os


def load_buses(filename: str) -> list[dict]:
    """Загружает список автобусов из JSON-файла."""
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def save_buses(filename: str, buses: list[dict]) -> None:
    """Сохраняет список автобусов в JSON-файл."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(buses, f, ensure_ascii=False, indent=4)
