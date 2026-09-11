from datetime import datetime

class Bus:
    name = "1"
    stops = ["пр. Третье кольцо", "пр. Второе кольцо", "пр. Первое кольцо", "ул. Речная"]
    number = "375"
    price_ticket = 71
    on_the_way = True

def Get_route(on_the_way):
    if on_the_way:
        return "Автобус в пути"
    return "Автобус в автопарке"

def Bus_stops():
    route = ""                 
    for stops in Bus.stops:
        route = route + stops + ", "
    route = route[:-2] + "."
    return route

def Arr_time():
    minutes = datetime.now().minute
    arrving =  minutes
    if arrving != 0:
        return f":автобус приедет через {arrving} минут к остановке"
    return "автобус прибывает к останоке"

print(f"Автобус {Bus.number} следует по маршруту '{Bus.name}'.")
print(f"Остановки на маршруте: {Bus_stops()}")
print(Arr_time())
print(Get_route(Bus.on_the_way))

