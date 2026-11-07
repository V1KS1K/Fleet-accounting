from django.core.paginator import Paginator
from django.db.models import Count, F, Q
from django.shortcuts import get_object_or_404, render
from buses.models import Bus, Route
from schedules.models import Schedule


def schedules_list(request):
    departure_time = request.GET.get("time", "").strip()
    route_id = request.GET.get("route", "").strip()
    bus_id = request.GET.get("bus", "").strip()
    sort = request.GET.get("sort", "time")
    error = None

    schedules_data = Schedule.objects.filter(is_cancelled=False)

    if departure_time:
        parts = departure_time.split(":")
        if (
            len(parts) != 2
            or not (parts[0].isdigit() and parts[1].isdigit())
            or not (0 <= int(parts[0]) <= 23 and 0 <= int(parts[1]) <= 59)
        ):
            error = "Укажите корректное время в формате ЧЧ:ММ."
        else:
            schedules_data = schedules_data.filter(departure_time=departure_time)

    if route_id.isdigit():
        schedules_data = schedules_data.filter(route_id=int(route_id))
    if bus_id.isdigit():
        schedules_data = schedules_data.filter(bus_id=int(bus_id))

    schedules_data = schedules_data.annotate(
        route_name=F("route__name"),
        bus_plate=F("bus__plate"),
    )

    sort_fields = {
        "time": "departure_time",
        "route": "route__name",
        "bus": "bus__plate",
    }
    sort_field = sort_fields.get(sort, "departure_time")
    schedules_data = schedules_data.order_by(sort_field, "id")

    schedules_data = schedules_data.values(
        "id",
        "departure_time",
        "is_cancelled",
        "route_name",
        "bus_plate",
    )

    paginator = Paginator(schedules_data, 5)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "schedules": page_obj,
        "page_obj": page_obj,
        "departure_time": departure_time,
        "selected_route": route_id,
        "selected_bus": bus_id,
        "sort": sort,
        "routes": Route.objects.order_by("name"),
        "buses": Bus.objects.order_by("plate"),
        "error": error,
    }
    return render(
        request,
        "schedules/schedule_list.html",
        context,
    )


def schedule_detail(request, schedule_id):
    schedule = get_object_or_404(
        Schedule.objects.select_related("bus", "route", "bus__driver"),
        pk=schedule_id,
    )
    context = {
        "schedule": schedule,
    }
    return render(
        request,
        "schedules/schedule_detail.html",
        context,
    )


def statistics(request):
    statistics_data = (
        Route.objects.annotate(
            schedules_count=Count(
                "schedules",
                filter=Q(schedules__is_cancelled=False),
            ),
            route_name=F("name"),
        )
        .values(
            "route_name",
            "schedules_count",
        )
        .order_by("-schedules_count", "route_name")
    )

    summary = Schedule.objects.aggregate(
        total_count=Count("id"),
        active_count=Count("id", filter=Q(is_cancelled=False)),
    )

    context = {
        "statistics": statistics_data,
        "summary": summary,
    }
    return render(
        request,
        "schedules/statistics.html",
        context,
    )