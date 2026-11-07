from django.db import models


class Stop(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Название остановки",
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Остановка"
        verbose_name_plural = "Остановки"


class Route(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Название маршрута",
    )
    stops = models.ManyToManyField(
        Stop,
        related_name="routes",
        blank=True,
        verbose_name="Остановки",
    )

    def get_stops_str(self):
        stops_qs = self.stops.all()
        if not stops_qs:
            return "Остановок нет."
        return ", ".join([stop.name for stop in stops_qs]) + "."

    def __str__(self):
        return f"Маршрут '{self.name}'"

    class Meta:
        ordering = ["name"]
        verbose_name = "Маршрут"
        verbose_name_plural = "Маршруты"


class Driver(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="ФИО водителя",
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Водитель"
        verbose_name_plural = "Водители"


class Bus(models.Model):
    plate = models.CharField(
        max_length=50,
        verbose_name="Госномер автобуса",
    )
    route = models.ForeignKey(
        Route,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="buses",
        verbose_name="Маршрут",
    )
    driver = models.ForeignKey(
        Driver,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="buses",
        verbose_name="Водитель",
    )
    on_the_way = models.BooleanField(
        default=False,
        verbose_name="В пути",
    )

    def get_route_status(self):
        return "Автобус в пути" if self.on_the_way else "Автобус в автопарке"

    def __str__(self):
        return f"Автобус {self.plate}"

    class Meta:
        ordering = ["plate"]
        verbose_name = "Автобус"
        verbose_name_plural = "Автобусы"