from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from buses.models import Bus
from schedules.models import Schedule


def buses_list(request):
    query = request.GET.get("q", "").strip()
    status_filter = request.GET.get("on_the_way", "").strip()

    buses_qs = Bus.objects.select_related("route", "driver").order_by("plate")

    if query:
        buses_qs = buses_qs.filter(
            Q(plate__icontains=query) | Q(route__name__icontains=query)
        )

    if status_filter == "1":
        buses_qs = buses_qs.filter(on_the_way=True)
    elif status_filter == "0":
        buses_qs = buses_qs.filter(on_the_way=False)

    context = {
        "buses": buses_qs,
        "query": query,
        "status_filter": status_filter,
    }
    return render(
        request,
        "buses/bus_list.html",
        context,
    )


def bus_detail(request, bus_id):
    bus = get_object_or_404(
        Bus.objects.select_related("route", "driver").prefetch_related("route__stops"),
        pk=bus_id,
    )
    stops = bus.route.stops.all() if bus.route else []
    active_schedules = bus.schedules.filter(is_cancelled=False).select_related("route")

    context = {
        "bus": bus,
        "stops": stops,
        "active_schedules": active_schedules,
    }
    return render(
        request,
        "buses/bus_detail.html",
        context,
    )


def available_buses(request):
    departure_time = request.GET.get("time", "").strip()
    buses_list_data = []
    error = None

    if departure_time:
        parts = departure_time.split(":")
        if (
            len(parts) != 2
            or not (parts[0].isdigit() and parts[1].isdigit())
            or not (0 <= int(parts[0]) <= 23 and 0 <= int(parts[1]) <= 59)
        ):
            error = "Укажите корректное время в формате ЧЧ:ММ."
        else:
            busy_bus_ids = Schedule.objects.filter(
                departure_time=departure_time,
                is_cancelled=False,
            ).values_list(
                "bus_id",
                flat=True,
            )
            buses_list_data = (
                Bus.objects.exclude(
                    pk__in=busy_bus_ids,
                )
                .select_related("route", "driver")
                .order_by("plate")
            )

    context = {
        "buses": buses_list_data,
        "departure_time": departure_time,
        "error": error,
    }
    return render(
        request,
        "buses/available.html",
        context,
    )