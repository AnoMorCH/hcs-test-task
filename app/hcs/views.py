from django.http import HttpResponse
from .entity.building import BuildingEntity
import json


def get_all_buildings(request):
    data = BuildingEntity.get_info_about_all()
    return HttpResponse(json.dumps(data), content_type="application/json")
