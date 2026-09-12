from datetime import datetime

class Bus:
    name = "001"
    stops = ["пр. Третье кольцо", "пр. Второе кольцо", "пр. Первое кольцо", "ул. Речная"]

    
def Get_route(on_the_way):
    if on_the_way:
        return "Автобус в пути"
    return "Автобус в автопарке"


def Bus_stops():
    route = ""                 
    for i in Bus.stops:
        route = route + i + ", "
    route = route[:-2] + "."
    return route


def Arr_time():
    arrving = 60 - datetime.now().minute
    if arrving != 0:
        return f"Автобус приедет через {arrving} минут к начальной остановке"
    return "Автобус прибывает к останоке"


print(f"Автобус следует по маршруту '{Bus.name}'.")
print(f"Остановки на маршруте: {Bus_stops()}")
print("Автобус следует по маршруту с интервалом раз в час")
print(Arr_time())
print(Get_route(Bus.on_the_way))

