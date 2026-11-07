import os
import sys
import sqlite3
from pathlib import Path
import django
from django.db import transaction

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
SOURCE_DB = BASE_DIR / "data" / "fleet.sqlite"

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fleet_project.settings")
django.setup()

from buses.models import Bus, Driver, Route, Stop  # noqa: E402
from schedules.models import Schedule  # noqa: E402


def main():
    if not SOURCE_DB.exists():
        raise FileNotFoundError(f"Исходная база не найдена: {SOURCE_DB}")

    with sqlite3.connect(SOURCE_DB) as connection:
        connection.row_factory = sqlite3.Row
        stops = connection.execute("SELECT id, name FROM stops ORDER BY id").fetchall()
        routes = connection.execute("SELECT id, name FROM routes ORDER BY id").fetchall()
        route_stops = connection.execute(
            "SELECT route_id, stop_id FROM route_stops"
        ).fetchall()
        drivers = connection.execute(
            "SELECT id, name FROM drivers ORDER BY id"
        ).fetchall()
        buses = connection.execute(
            "SELECT id, plate, route_id, driver_id, on_the_way FROM buses ORDER BY id"
        ).fetchall()
        schedules = connection.execute(
            "SELECT id, bus_id, route_id, departure_time, is_cancelled "
            "FROM schedules ORDER BY id"
        ).fetchall()

    with transaction.atomic():
        for row in stops:
            Stop.objects.update_or_create(
                pk=row["id"],
                defaults={"name": row["name"]},
            )

        for row in routes:
            Route.objects.update_or_create(
                pk=row["id"],
                defaults={"name": row["name"]},
            )

        for r_obj in Route.objects.all():
            stop_ids = [
                rs["stop_id"] for rs in route_stops if rs["route_id"] == r_obj.pk
            ]
            r_obj.stops.set(stop_ids)

        for row in drivers:
            Driver.objects.update_or_create(
                pk=row["id"],
                defaults={"name": row["name"]},
            )

        for row in buses:
            Bus.objects.update_or_create(
                pk=row["id"],
                defaults={
                    "plate": row["plate"],
                    "route_id": row["route_id"],
                    "driver_id": row["driver_id"],
                    "on_the_way": bool(row["on_the_way"]),
                },
            )

        for row in schedules:
            Schedule.objects.update_or_create(
                pk=row["id"],
                defaults={
                    "bus_id": row["bus_id"],
                    "route_id": row["route_id"],
                    "departure_time": row["departure_time"],
                    "is_cancelled": bool(row["is_cancelled"]),
                },
            )

    print("Перенос данных завершён.")
    print(f"Остановок: {Stop.objects.count()}")
    print(f"Маршрутов: {Route.objects.count()}")
    print(f"Водителей: {Driver.objects.count()}")
    print(f"Автобусов: {Bus.objects.count()}")
    print(f"Рейсов: {Schedule.objects.count()}")


if __name__ == "__main__":
    main()
    