from django.urls import path
from . import views

app_name = "schedules"

urlpatterns = [
    path("", views.schedules_list, name="schedules"),
    path("<int:schedule_id>/", views.schedule_detail, name="detail"),
]