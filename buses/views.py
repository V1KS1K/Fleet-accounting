import sqlite3
from django.shortcuts import render

DB_PATH = "data/fleet.sqlite"


def buses_list(request):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    buses = conn.execute("""
        SELECT 
            b.id, 
            b.plate, 
            b.on_the_way,
            r.name AS route_name,
            d.name AS driver_name
        FROM buses b
        LEFT JOIN routes r ON b.route_id = r.id
        LEFT JOIN drivers d ON b.driver_id = d.id
        ORDER BY b.plate;
    """).fetchall()
    conn.close()
    context = {
        "buses": buses,
    }
    return render(
        request,
        "buses/bus_list.html",
        context,
    )


def bus_detail(request, bus_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    bus = conn.execute("""
        SELECT 
            b.id, 
            b.plate, 
            b.on_the_way,
            r.id AS route_id,
            r.name AS route_name,
            d.id AS driver_id,
            d.name AS driver_name
        FROM buses b
        LEFT JOIN routes r ON b.route_id = r.id
        LEFT JOIN drivers d ON b.driver_id = d.id
        WHERE b.id = ?;
    """, (bus_id,)).fetchone()  
    stops = []
    if bus and bus["route_id"]:
        stops = conn.execute("""
            SELECT s.name 
            FROM stops s
            JOIN route_stops rs ON s.id = rs.stop_id
            WHERE rs.route_id = ?;
        """, (bus["route_id"],)).fetchall()
    conn.close() 
    context = {
        "bus": bus,
        "stops": stops,
    }
    return render(
        request,
        "buses/bus_detail.html",
        context,
        status=404 if bus is None else 200,
    )