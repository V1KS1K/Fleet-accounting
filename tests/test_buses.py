from buses import Stop, Route, Driver, Bus


def test_bus_route_status_on_way():
    stop = Stop(1, "Остановка 1")
    route = Route(1, "101", [stop])
    driver = Driver(1, "Иванов И.И.")
    bus = Bus(1, "А123АА", route, driver, True)
    assert bus.get_route_status() == "Автобус в пути"


def test_bus_route_status_in_park():
    bus = Bus(2, "В456ВВ", None, None, False)
    assert bus.get_route_status() == "Автобус в автопарке"


def test_route_get_stops_exist():
    stop1 = Stop(1, "Остановка 1")
    stop2 = Stop(2, "Остановка 2")
    route = Route(1, "103", [stop1, stop2])
    assert route.get_stops_str() == "Остановка 1, Остановка 2."