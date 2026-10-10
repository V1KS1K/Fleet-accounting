from models import Bus, Route, Schedule


def test_schedule_creation():
    route = Route(1, "001")
    bus = Bus(1, "К743ФН", route)
    sch = Schedule(1, bus, route, "08:30")
    assert sch.id == 1
    assert sch.bus is bus
    assert sch.route is route
    assert sch.departure_time == "08:30"
    assert sch.is_active is True
    assert sch.is_cancelled is False


def test_schedule_validation_and_cancellation():
    route = Route(1, "001")
    bus = Bus(1, "К743ФН", route)
    sch = Schedule(1, bus, route, "08:30")

    # 1. Валидация формата времени
    assert Schedule.validate_time("08:30") is True
    assert Schedule.validate_time("25:00") is False
    assert Schedule.validate_time("abc") is False

    # 2. Отмена рейса
    sch.cancel()
    assert sch.is_cancelled is True
    assert sch.is_active is False
    assert "ОТМЕНЕН" in str(sch)

    # 3. Возобновление рейса
    sch.restore()
    assert sch.is_cancelled is False
    assert sch.is_active is True