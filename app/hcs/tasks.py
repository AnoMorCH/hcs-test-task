from house_accounting.celery import app
from .entity.communal_service_price import CommunalServicePrice


@app.task
def task_count_communal_service_price(building_id, year, month):
    csp = CommunalServicePrice(building_id, year, month)
    return csp.count()
