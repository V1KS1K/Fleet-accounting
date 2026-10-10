import json
import os
from typing import List, Optional, Tuple
from models import Bus, Driver, Route, Schedule, Stop


def load_raw_json(filepath: str) -> list:
    """Чтение сырых данных из JSON с защитой от ошибок."""
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def save_raw_json(filepath: str, data: list) -> None:
    """Запись данных в JSON."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_all_data() -> Tuple[
    List[Stop], List[Route], List[Driver], List[Bus], List[Schedule]
]:
    """Загрузка всех сущностей и построение объектных связей."""
    stops_data = load_raw_json("data/stops.json")
    routes_data = load_raw_json("data/routes.json")
    drivers_data = load_raw_json("data/drivers.json")
    buses_data = load_raw_json("data/buses.json")
    schedules_data = load_raw_json("data/schedules.json")

    stops = [Stop.from_data(s) for s in stops_data]
    stop_map = {s.id: s for s in stops}

    drivers = [Driver.from_data(d) for d in drivers_data]
    driver_map = {d.id: d for d in drivers}

    routes: List[Route] = []
    for r in routes_data:
        route_stops = [
            stop_map[sid] for sid in r.get("stop_ids", []) if sid in stop_map
        ]
        routes.append(Route(r["id"], r["name"], route_stops))
    route_map = {r.id: r for r in routes}

    buses: List[Bus] = []
    for b in buses_data:
        r_obj: Optional[Route] = route_map.get(b.get("route_id"))
        dr_obj: Optional[Driver] = driver_map.get(b.get("driver_id"))
        buses.append(
            Bus(
                bus_id=b["id"],
                plate=b["plate"],
                route=r_obj,
                driver=dr_obj,
                on_the_way=b.get("on_the_way", False),
            )
        )
    bus_map = {b.id: b for b in buses}

    schedules: List[Schedule] = []
    for sch in schedules_data:
        b_obj = bus_map.get(sch.get("bus_id"))
        r_obj = route_map.get(sch.get("route_id"))
        if b_obj and r_obj:
            schedules.append(
                Schedule(
                    schedule_id=sch["id"],
                    bus=b_obj,
                    route=r_obj,
                    departure_time=sch.get("departure_time", "08:00"),
                    is_cancelled=sch.get("is_cancelled", False),
                )
            )

    return stops, routes, drivers, buses, schedules


def save_buses(buses: List[Bus]) -> None:
    """Сохранение объектов Bus в JSON с сохранением ID связей."""
    data = []
    for b in buses:
        data.append(
            {
                "id": b.id,
                "plate": b.plate,
                "route_id": b.route.id if b.route else None,
                "driver_id": b.driver.id if b.driver else None,
                "on_the_way": b.on_the_way,
            }
        )
    save_raw_json("data/buses.json", data)


def save_schedules(schedules: List[Schedule]) -> None:
    """Сохранение объектов Schedule в JSON с сохранением ID связей."""
    data = []
    for s in schedules:
        data.append(
            {
                "id": s.id,
                "bus_id": s.bus.id,
                "route_id": s.route.id,
                "departure_time": s.departure_time,
                "is_cancelled": s.is_cancelled,
            }
        )
    save_raw_json("data/schedules.json", data)


def save_all_data(
    stops: List[Stop],
    routes: List[Route],
    drivers: List[Driver],
    buses: List[Bus],
    schedules: List[Schedule],
) -> None:
    """Сохранение всех измененных сущностей."""
    save_raw_json(
        "data/stops.json", [{"id": s.id, "name": s.name} for s in stops]
    )
    save_raw_json(
        "data/drivers.json", [{"id": d.id, "name": d.name} for d in drivers]
    )
    save_raw_json(
        "data/routes.json",
        [
            {
                "id": r.id,
                "name": r.name,
                "stop_ids": [s.id for s in r.stops],
            }
            for r in routes
        ],
    )
    save_buses(buses)
    save_schedules(schedules)