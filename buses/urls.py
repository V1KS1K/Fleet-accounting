from django.urls import path
from . import views

app_name = "buses"

urlpatterns = [
    path("", views.buses_list, name="list"),
    path("<int:bus_id>/", views.bus_detail, name="detail"),
]