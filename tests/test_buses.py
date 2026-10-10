from models import Bus, Driver, Route, Stop


def test_bus_creation():
    route = Route(1, "001", [Stop(1, "Центр")])
    driver = Driver(1, "Иванов И.И.")
    bus = Bus(1, "К743ФН", route, driver, on_the_way=True)
    assert bus.id == 1
    assert bus.plate == "К743ФН"
    assert bus.is_assigned is True
    assert bus.get_route_status() == "Автобус в пути"


def test_bus_interaction():
    route = Route(1, "002")
    driver = Driver(1, "Сидоров С.С.")
    bus = Bus(2, "В125ОВ", None, None, on_the_way=False)

    # 1. Валидация госномера
    assert Bus.validate_plate("В125ОВ") is True
    assert Bus.validate_plate("А1") is False

    # 2. Назначение на маршрут
    assert bus.is_assigned is False
    bus.assign_to_route(route, driver)
    assert bus.is_assigned is True
    assert bus.route is route
    assert bus.driver is driver

    # 3. Снятие с маршрута
    bus.release()
    assert bus.is_assigned is False
    assert bus.route is None