from django.urls import path
from . import views


app_name = "hcs"

urlpatterns = [
    path("building/", views.get_all_buildings)
]
