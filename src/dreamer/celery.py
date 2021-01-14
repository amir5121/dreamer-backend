import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dreamer.settings")

app = Celery(
    "dreamer",
    broker=settings.CELERY_BROKER,
    # backend='amqp://',
    include=["post.tasks"],
)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

if __name__ == "__main__":
    app.start()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")


app.conf.beat_schedule = {
    "health_check": {
        "task": "post.tasks.health_check",
        "schedule": crontab(minute='*/1'),
    },
}
