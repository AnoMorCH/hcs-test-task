from django.http import HttpResponse
from django.views.generic import View
from .entity.building import BuildingEntity
from .entity.apartment import ApartmentEntity
from .entity.water_meter import WaterMeterEntity
from .entity.message import MessageEntity
from .entity.water_meter_log import WaterMeterLogEntity
# from .entity.communal_service_price import CommunalServicePrice
from .tasks import task_count_communal_service_price
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

            
class WaterMeterLogView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            WaterMeterLogEntity.create(data.get("water_meter_id"), data.get("month"), data.get("year"), data.get("consumed"))
            return HttpResponse(MessageEntity.get("A water meter log has been created."), content_type="application/json", status=200)
        except Exception as e:
            return HttpResponse(MessageEntity.get(str(e)), content_type="application/json", status=400)


class CountCommunalServicePriceView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            building_id, year, month = data.get("building_id"), data.get("year"), data.get("month")
            res = task_count_communal_service_price.delay(building_id, year, month)
            csp_value = res.get()
            # csp = CommunalServicePrice(data.get("building_id"), data.get("year"), data.get("month"))
            # csp_value = csp.count()
            message = {
                "building_id": building_id,
                "year": year,
                "month": month,
                "price": csp_value,
            }
            return HttpResponse(json.dumps(message), content_type="application/json", status=200)
        except Exception as e:
            return HttpResponse(MessageEntity.get(str(e)), content_type="application/json", status=400)
