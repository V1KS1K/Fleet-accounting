-- 1. Получение списка всех автобусов
SELECT id, plate, on_the_way 
FROM buses 
ORDER BY plate;

-- 2. Фильтрация автобусов в пути (WHERE)
SELECT id, plate 
FROM buses 
WHERE on_the_way = 1;

-- 3. Список всех водителей
SELECT id, name 
FROM drivers 
ORDER BY name;

-- 4. Список всех маршрутов
SELECT id, name 
FROM routes;

-- 5. Список всех остановок
SELECT id, name 
FROM stops;

-- 6. Соединение таблиц (JOIN) для получения информации об автобусах, маршрутах и водителях
SELECT 
    b.id AS bus_id, 
    b.plate, 
    r.name AS route_name, 
    d.name AS driver_name, 
    b.on_the_way 
FROM buses b
LEFT JOIN routes r ON b.route_id = r.id
LEFT JOIN drivers d ON b.driver_id = d.id
ORDER BY b.id;

-- 7. Активные рейсы с соединением таблиц (JOIN)
SELECT 
    s.id AS schedule_id, 
    r.name AS route_name, 
    b.plate, 
    s.departure_time 
FROM schedules s
JOIN routes r ON s.route_id = r.id
JOIN buses b ON s.bus_id = b.id
WHERE s.is_cancelled = 0
ORDER BY s.departure_time;

-- 8. Агрегирующая функция: общее количество автобусов (COUNT)
SELECT COUNT(*) AS total_buses 
FROM buses;

-- 9. Группировка (GROUP BY): количество рейсов по маршрутам
SELECT 
    r.name AS route_name, 
    COUNT(s.id) AS schedules_count
FROM routes r
LEFT JOIN schedules s ON r.id = s.route_id AND s.is_cancelled = 0
GROUP BY r.id, r.name
ORDER BY schedules_count DESC;

-- 10. Фильтрация групп (HAVING): маршруты с активными рейсами >= 1
SELECT 
    r.name AS route_name, 
    COUNT(s.id) AS schedules_count
FROM routes r
JOIN schedules s ON r.id = s.route_id
WHERE s.is_cancelled = 0
GROUP BY r.id, r.name
HAVING COUNT(s.id) >= 1
ORDER BY schedules_count DESC;