import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "banka_ekstre_project.settings")

app = Celery("banka_ekstre_project")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
