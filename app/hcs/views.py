from django.http import HttpResponse
from django.views.generic import View
from .entity.building import BuildingEntity
from .entity.apartment import ApartmentEntity
from .entity.water_meter import WaterMeterEntity
from .entity.message import MessageEntity
import json


class BuildingView(View):
    def get(self, request):
        data = BuildingEntity.get_info_about_all()
        return HttpResponse(json.dumps(data), content_type="application/json", status=200)

    def post(self, request):
        try:
            data = json.loads(request.body)
            BuildingEntity.create(data.get("number"), data.get("address"))
            return HttpResponse(MessageEntity.get("A building has been created."), content_type="application/json", status=200)
        except Exception as e:
            return HttpResponse(MessageEntity.get(str(e)), content_type="application/json", status=400)


class ApartmentView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            ApartmentEntity.create(data.get("number"), data.get("building_id"), data.get("size_m2"))
            return HttpResponse(MessageEntity.get("An apartment has been created."), content_type="application/json", status=200)
        except Exception as e:
            return HttpResponse(MessageEntity.get(str(e)), content_type="application/json", status=400)

            
class WaterMeterView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            WaterMeterEntity.create(data.get("apartment_id"))
            return HttpResponse(MessageEntity.get("A water meter has been created."), content_type="application/json", status=200)
        except Exception as e:
            return HttpResponse(MessageEntity.get(str(e)), content_type="application/json", status=400)
