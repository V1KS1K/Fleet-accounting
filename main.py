from typing import List
from models import Bus, Driver, Route, Schedule, Stop
from storage import load_all_data, save_all_data
from utils import input_int


def show_buses(buses: List[Bus]) -> None:
    """Отображение всех автобусов через метод __str__."""
    if not buses:
        print("Список автобусов пуст.")
        return
    print("\n--- СПИСОК АВТОБУСОВ ---")
    for b in buses:
        print(b)
        if b.route:
            print(f"  Остановки маршрута: {b.route.get_stops_str()}")


def add_new_bus(
    routes: List[Route],
    drivers: List[Driver],
    buses: List[Bus],
) -> None:
    """Сценарий создания нового объекта Bus."""
    print("\n--- Добавление нового автобуса ---")
    plate = input("Введите госномер автобуса: ").strip()
    if not Bus.validate_plate(plate):
        print("Ошибка: номер должен содержать не менее 5 символов.")
        return

    print("\nВыберите маршрут (0 - без маршрута):")
    for r in routes:
        print(f"{r.id}. {r.name}")
    r_id = input_int("Номер маршрута: ")
    route = next((r for r in routes if r.id == r_id), None)

    print("\nВыберите водителя (0 - без водителя):")
    for d in drivers:
        print(f"{d.id}. {d.name}")
    d_id = input_int("ID водителя: ")
    driver = next((d for d in drivers if d.id == d_id), None)

    new_id = max([b.id for b in buses], default=0) + 1
    new_bus = Bus(new_id, plate, route, driver, on_the_way=route is not None)
    buses.append(new_bus)
    print(f"Автобус {plate} успешно добавлен в автопарк!")


def assign_bus_scenario(
    routes: List[Route],
    drivers: List[Driver],
    buses: List[Bus],
) -> None:
    """Сценарий закрепления автобуса за маршрутом и водителем."""
    bus_id = input_int("Введите ID автобуса: ")
    bus = next((b for b in buses if b.id == bus_id), None)
    if not bus:
        print("Автобус не найден.")
        return

    print("\nВыберите маршрут (0 - снять автобус с маршрута):")
    for r in routes:
        print(f"{r.id}. {r.name}")
    r_id = input_int("ID маршрута: ")
    if r_id == 0:
        bus.release()
        print(f"Автобус {bus.plate} успешно снят с маршрута и отправлен в автопарк!")
        return    
    route = next((r for r in routes if r.id == r_id), None)
    if not route:
        print("Маршрут не найден.")
        return

    print("\nВыберите водителя:")
    for d in drivers:
        print(f"{d.id}. {d.name}")
    d_id = input_int("ID водителя: ")
    driver = next((d for d in drivers if d.id == d_id), None)

    bus.assign_to_route(route, driver)
    print(f"Автобус {bus.plate} успешно назначен на маршрут {route.name}!")


def show_schedules_scenario(schedules: List[Schedule]) -> None:
    """Просмотр расписания рейсов."""
    if not schedules:
        print("Расписание рейсов пусто.")
        return
    print("\n--- РАСПИСАНИЕ РЕЙСОВ ---")
    for item in schedules:
        print(item)


def add_schedule_scenario(
    buses: List[Bus],
    routes: List[Route],
    schedules: List[Schedule],
) -> None:
    """Создание рейса в расписании."""
    print("\n--- Добавление рейса в расписание ---")
    bus_id = input_int("Введите ID автобуса: ")
    bus = next((b for b in buses if b.id == bus_id), None)
    if not bus:
        print("Автобус не найден.")
        return

    route_id = input_int("Введите ID маршрута: ")
    route = next((r for r in routes if r.id == route_id), None)
    if not route:
        print("Маршрут не найден.")
        return

    dep_time = input("Введите время отправления (ЧЧ:ММ): ").strip()
    if not Schedule.validate_time(dep_time):
        print("Ошибка: укажите корректное время в формате ЧЧ:ММ.")
        return

    for item in schedules:
        if (
            item.bus.id == bus.id
            and item.departure_time == dep_time
            and item.is_active
        ):
            print("Ошибка: этот автобус уже занят рейсом на это время!")
            return

    new_id = max([s.id for s in schedules], default=0) + 1
    new_sch = Schedule(new_id, bus, route, dep_time)
    schedules.append(new_sch)
    print(f"Рейс успешно добавлен: {new_sch}")


def cancel_schedule_scenario(schedules: List[Schedule]) -> None:
    """Отмена рейса в расписании."""
    show_schedules_scenario(schedules)
    sch_id = input_int("Введите ID рейса для отмены: ")
    item = next((s for s in schedules if s.id == sch_id), None)
    if not item:
        print("Рейс не найден.")
        return
    if not item.is_active:
        print("Рейс уже был отменен ранее.")
        return

    item.cancel()
    print(f"Рейс #{sch_id} успешно отменен!")


def show_stops_and_routes(stops: List[Stop], routes: List[Route]) -> None:
    """Просмотр остановок и маршрутов."""
    print("\n--- МАРШРУТЫ И ОСТАНОВКИ ---")
    for r in routes:
        print(f"{r} -> Остановки: {r.get_stops_str()}")


def main() -> None:
    """Точка запуска приложения."""
    stops, routes, drivers, buses, schedules = load_all_data()

    while True:
        print("\n=== УЧЕТ АВТОПАРКА И РАСПИСАНИЯ (ООП) ===")
        print("1. Показать список автобусов")
        print("2. Добавить новый автобус")
        print("3. Назначить автобус на маршрут")
        print("4. Показать маршруты и остановки")
        print("5. Показать расписание рейсов")
        print("6. Добавить рейс в расписание")
        print("7. Отменить рейс из расписания")
        print("0. Выход")

        choice = input("Выберите действие: ").strip()
        if choice == "1":
            show_buses(buses)
        elif choice == "2":
            add_new_bus(routes, drivers, buses)
        elif choice == "3":
            assign_bus_scenario(routes, drivers, buses)
        elif choice == "4":
            show_stops_and_routes(stops, routes)
        elif choice == "5":
            show_schedules_scenario(schedules)
        elif choice == "6":
            add_schedule_scenario(buses, routes, schedules)
        elif choice == "7":
            cancel_schedule_scenario(schedules)
        elif choice == "0":
            # Сохранение всех данных только перед выходом из программы
            save_all_data(stops, routes, drivers, buses, schedules)
            print("Данные успешно сохранены. Работа завершена.")
            break
        else:
            print("Некорректный выбор, попробуйте еще раз.")


if __name__ == "__main__":
    main()

#  flake8
#  python -m pytest -v
#  python manage.py migrate
#  python manage.py runserver