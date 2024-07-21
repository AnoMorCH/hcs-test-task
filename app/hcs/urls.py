from django.urls import path
from . import views


app_name = "hcs"

urlpatterns = [
    path("building/", views.BuildingView.as_view()),
    path("apartment/", views.ApartmentView.as_view()),
    path("water_meter/", views.WaterMeterView.as_view()),
]
