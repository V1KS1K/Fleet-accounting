from datetime import datetime
from storage import load_data, save_data
from buses import Bus, find_bus
from utils import input_int


def show_buses(buses: list[Bus]) -> None:
    """Выводит список всех автобусов."""
    if not buses:
        print("Автопарк пуст.")
        return
    for bus in buses:
        # Проверяем, назначен ли маршрут
        if bus.route:
            print(f"Автобус {bus.plate} следует по маршруту '{bus.route.name}'.")
            print(f"Остановки на маршруте: {bus.route.get_stops_str()}")
        else:
            print(f"Автобус {bus.plate} не имеет назначенного маршрута.")  
        print(bus.get_route_status())  
        arriving = 60 - datetime.now().minute
        if arriving != 0:
            print(f"Автобус приедет через {arriving} минут к начальной остановке.")
        else:
            print("Автобус прибывает к остановке.")
        print("-" * 30)


def main() -> None:
    """Точка запуска приложения."""
    data_dir = "data"  
    stops, routes, drivers, buses = load_data(data_dir)

    while True:
        print("\n Система учета общественного транспорта ")
        print("2. Найти маршрут")
        print("1. Показать список маршрутов")
        print("0. Выход")       
        choice = input_int("Выберите действие: ")        
        if choice == 1:
            show_buses(buses)
        elif choice == 0:
            save_data(data_dir, stops, routes, drivers, buses)
            print("Данные сохранены. Работа завершена.")
            break
        elif choice == 2:
            query = input("Введите номер маршрута для поиска: ")
            found = find_bus(buses, query)
            show_buses(found)
        else:
            print("Неизвестная команда, попробуйте еще раз.")


if __name__ == "__main__":
    main()