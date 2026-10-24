import json
from db.database import get_connection

STOPS_FILE = "data/stops.json"
ROUTES_FILE = "data/routes.json"
DRIVERS_FILE = "data/drivers.json"
BUSES_FILE = "data/buses.json"
SCHEDULES_FILE = "data/schedules.json"


def load_json(filename):
    with open(filename, encoding="utf-8") as file:
        return json.load(file)


def import_stops(conn):
    stops = load_json(STOPS_FILE)
    conn.executemany(
        """
        INSERT OR REPLACE INTO stops (id, name)
        VALUES (?, ?)
        """,
        [(s["id"], s["name"]) for s in stops]
    )


def import_routes(conn):
    routes = load_json(ROUTES_FILE)
    for r in routes:
        conn.execute(
            """
            INSERT OR REPLACE INTO routes (id, name)
            VALUES (?, ?)
            """,
            (r["id"], r["name"])
        )
        for stop_id in r.get("stop_ids", []):
            conn.execute(
                """
                INSERT INTO route_stops (route_id, stop_id)
                VALUES (?, ?)
                """,
                (r["id"], stop_id)
            )


def import_drivers(conn):
    drivers = load_json(DRIVERS_FILE)
    conn.executemany(
        """
        INSERT OR REPLACE INTO drivers (id, name)
        VALUES (?, ?)
        """,
        [(d["id"], d["name"]) for d in drivers]
    )


def import_buses(conn):
    buses = load_json(BUSES_FILE)
    conn.executemany(
        """
        INSERT OR REPLACE INTO buses (id, plate, route_id, driver_id, on_the_way)
        VALUES (?, ?, ?, ?, ?)
        """,
        [
            (
                b["id"],
                b["plate"],
                b.get("route_id"),
                b.get("driver_id"),
                int(b.get("on_the_way", False))
            )
            for b in buses
        ]
    )


def import_schedules(conn):
    schedules = load_json(SCHEDULES_FILE)
    conn.executemany(
        """
        INSERT OR REPLACE INTO schedules (id, bus_id, route_id, departure_time, is_cancelled)
        VALUES (?, ?, ?, ?, ?)
        """,
        [
            (
                s["id"],
                s["bus_id"],
                s["route_id"],
                s["departure_time"],
                int(s.get("is_cancelled", False))
            )
            for s in schedules
        ]
    )


def main():
    conn = get_connection()
    conn.execute("DELETE FROM route_stops")
    try:
        import_stops(conn)
        import_routes(conn)
        import_drivers(conn)
        import_buses(conn)
        import_schedules(conn)
        conn.commit()
        print("Импорт данных из JSON в SQLite успешно завершен.")
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()