import json
import os
from buses import Stop, Route, Driver, Bus


def load_data(data_dir: str) -> tuple[list[Stop], list[Route], list[Driver], list[Bus]]:
    """Единая функция загрузки всех объектов и создания связей между ними.""" 
    # 1. Загрузка остановок
    stops = []
    if os.path.exists(f"{data_dir}/stops.json"):
        with open(f"{data_dir}/stops.json", 'r', encoding='utf-8') as f:
            stops = [Stop(d["id"], d["name"]) for d in json.load(f)]       
    # 2. Загрузка водителей
    drivers = []
    if os.path.exists(f"{data_dir}/drivers.json"):
        with open(f"{data_dir}/drivers.json", 'r', encoding='utf-8') as f:
            drivers = [Driver(d["id"], d["name"]) for d in json.load(f)]

    # 3. Загрузка маршрутов
    routes = []
    if os.path.exists(f"{data_dir}/routes.json"):
        with open(f"{data_dir}/routes.json", 'r', encoding='utf-8') as f:
            for d in json.load(f):
                route_stops = [s for s in stops if s.id in d.get("stop_ids", [])]
                routes.append(Route(d["id"], d["name"], route_stops))

    # 4. Загрузка автобусов
    buses = []
    if os.path.exists(f"{data_dir}/buses.json"):
        with open(f"{data_dir}/buses.json", 'r', encoding='utf-8') as f:
            for d in json.load(f):
                bus_route = next((r for r in routes if r.id == d.get("route_id")), None)
                bus_driver = next((dr for dr in drivers if dr.id == d.get("driver_id")), None)
                buses.append(Bus(d["id"], d["plate"], bus_route, bus_driver, d.get("on_the_way", False)))      
    return stops, routes, drivers, buses


def save_data(data_dir: str, stops: list[Stop], routes: list[Route], drivers: list[Driver], buses: list[Bus]) -> None:
    """Сохранение объектов в JSON (в файлах хранятся только ID связей)."""
    with open(f"{data_dir}/stops.json", 'w', encoding='utf-8') as f:
        json.dump([{"id": s.id, "name": s.name} for s in stops], f, ensure_ascii=False, indent=4) 
    with open(f"{data_dir}/drivers.json", 'w', encoding='utf-8') as f:
        json.dump([{"id": d.id, "name": d.name} for d in drivers], f, ensure_ascii=False, indent=4)  
    with open(f"{data_dir}/routes.json", 'w', encoding='utf-8') as f:
        json.dump([{"id": r.id, "name": r.name, "stop_ids": [s.id for s in r.stops]} for r in routes], f, ensure_ascii=False, indent=4)     
    with open(f"{data_dir}/buses.json", 'w', encoding='utf-8') as f:
        json.dump([{
            "id": b.id, 
            "plate": b.plate, 
            "route_id": b.route.id if b.route else None, 
            "driver_id": b.driver.id if b.driver else None, 
            "on_the_way": b.on_the_way
        } for b in buses], f, ensure_ascii=False, indent=4)