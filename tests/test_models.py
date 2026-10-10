from models import Driver, Route, Stop


def test_stop_creation():
    stop = Stop(1, "Площадь Победы")
    assert stop.id == 1
    assert str(stop) == "Площадь Победы"


def test_stop_from_data():
    data = {"id": 2, "name": "ул. Ленина"}
    stop = Stop.from_data(data)
    assert stop.id == 2
    assert stop.name == "ул. Ленина"


def test_driver_creation():
    driver = Driver(1, "Иванов И.И.")
    assert driver.id == 1
    assert str(driver) == "Иванов И.И."


def test_driver_from_data():
    data = {"id": 2, "name": "Петров П.П."}
    driver = Driver.from_data(data)
    assert driver.id == 2
    assert driver.name == "Петров П.П."


def test_route_creation():
    stop1 = Stop(1, "Остановка 1")
    stop2 = Stop(2, "Остановка 2")
    route = Route(1, "101", [stop1, stop2])
    assert route.id == 1
    assert route.name == "101"
    assert "Остановка 1, Остановка 2." == route.get_stops_str()
    assert "101" in str(route)
