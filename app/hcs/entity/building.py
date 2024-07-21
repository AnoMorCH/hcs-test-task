from ..models import Building
from .apartment import ApartmentEntity


class BuildingEntity:
    @staticmethod
    def get_info_about_all():
        info = []
        all_buildings = Building.objects.all().values()
        for building in all_buildings:
            building_info = building
            building_info["apartments"] = ApartmentEntity.get_info_by(building["id"])
            info.append(building_info)
        return info