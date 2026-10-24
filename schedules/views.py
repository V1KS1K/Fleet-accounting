import sqlite3
from django.shortcuts import render

DB_PATH = "data/fleet.sqlite"


def schedules_list(request):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    schedules = conn.execute("""
        SELECT 
            s.id, 
            s.departure_time, 
            s.is_cancelled,
            r.name AS route_name,
            b.plate AS bus_plate
        FROM schedules s
        JOIN routes r ON s.route_id = r.id
        JOIN buses b ON s.bus_id = b.id
        ORDER BY s.departure_time;
    """).fetchall()
    conn.close()
    context = {
        "schedules": schedules,
    }
    return render(
        request,
        "schedules/schedule_list.html",
        context,
    )


def schedule_detail(request, schedule_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    schedule = conn.execute("""
        SELECT 
            s.id, 
            s.departure_time, 
            s.is_cancelled,
            r.name AS route_name,
            b.plate AS bus_plate
        FROM schedules s
        JOIN routes r ON s.route_id = r.id
        JOIN buses b ON s.bus_id = b.id
        WHERE s.id = ?;
    """, (schedule_id,)).fetchone()
    conn.close()
    context = {
        "schedule": schedule,
    }
    return render(
        request,
        "schedules/schedule_detail.html",
        context,
        status=404 if schedule is None else 200,
    )