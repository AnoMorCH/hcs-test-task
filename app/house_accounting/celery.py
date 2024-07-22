from celery import Celery
import os


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "house_accounting.settings")

app = Celery("house_accounting")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
