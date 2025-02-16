import os
import sys
from celery import Celery


celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",  # Address of the Redis broker to be used for task queues
    backend="redis://localhost:6379/0"  # Redis address to be used as backend for storing task results
)

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


celery_app.conf.update(
    task_track_started=True,  # Setting to track task status
    result_expires=3600,  # The results' lifetime (in seconds) after which they will be deleted
    timezone='UTC',  # Set time zone
)

celery_app.autodiscover_tasks(['app.tasks'])

celery_app.conf.update(
    worker_max_tasks_per_child=100,  # Number of tasks after which the worker will be restarted
    task_acks_late=True,  # Configure the confirmation of tasks after they are completed
)



