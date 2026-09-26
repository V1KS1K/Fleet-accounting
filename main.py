from datetime import datetime
from storage import load_buses
from buses import get_route_status, get_bus_stops, find_bus
from utils import input_int


def show_buses(buses: list[dict]) -> None:
    """Выводит список всех маршрутов."""
    if not buses:
        print("Автопарк пуст.")
        return   
    for bus in buses:
        print(f"Автобус следует по маршруту '{bus.get('name')}'.")
        print(f"Остановки на маршруте: {get_bus_stops(bus)}")
        print(get_route_status(bus))       
        arriving = 60 - datetime.now().minute
        if arriving != 0:
            print(f"Автобус приедет через {arriving} минут к начальной остановке.")
        else:
            print("Автобус прибывает к остановке.")
        print("-" * 30)


def main() -> None:
    """Точка запуска приложения."""
    filename = "data/buses.json"
    buses = load_buses(filename)

    while True:
        print("\n=== Система учета общественного транспорта ===")
        print("2. Найти маршрут")
        print("1. Показать список маршрутов")
        print("0. Выход")       
        choice = input_int("Выберите действие: ")        
        if choice == 1:
            show_buses(buses)
        elif choice == 0:
            print("Работа завершена.")
            break
        elif choice == 2:
            query = input("Введите название маршрута для поиска: ")
            found = find_bus(buses, query)
            show_buses(found)
        else:
            print("Неизвестная команда, попробуйте еще раз.")


if __name__ == "__main__":
    main()