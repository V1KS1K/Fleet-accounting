from django.db import models
from buses.models import Bus, Route


class Schedule(models.Model):
    bus = models.ForeignKey(
        Bus,
        on_delete=models.PROTECT,
        related_name="schedules",
        verbose_name="Автобус",
    )
    route = models.ForeignKey(
        Route,
        on_delete=models.PROTECT,
        related_name="schedules",
        verbose_name="Маршрут",
    )
    departure_time = models.CharField(
        max_length=10,
        verbose_name="Время отправления (ЧЧ:ММ)",
    )
    is_cancelled = models.BooleanField(
        default=False,
        verbose_name="Рейс отменен",
    )

    def cancel(self):
        self.is_cancelled = True
        self.save(update_fields=["is_cancelled"])

    def __str__(self):
        return f"Рейс #{self.pk}: Маршрут {self.route.name} ({self.departure_time})"

    class Meta:
        ordering = ["departure_time", "pk"]
        verbose_name = "Рейс"
        verbose_name_plural = "Расписание рейсов"