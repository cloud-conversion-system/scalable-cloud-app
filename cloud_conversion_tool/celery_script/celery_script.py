from celery import Celery

app = Celery('celery_script', include=['celery_script.tasks'], broker='redis://localhost:6379')
app.config_from_object('celery_script.celery_config')

app.conf.beat_schedule = {
    "run-me-every-ten-seconds":{
        "task": "tasks.check_database",
        "schedule": 10.0
    }
}

