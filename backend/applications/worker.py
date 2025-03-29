from celery import Celery, Task
from flask import current_app as app

def celery_init_app():
    class FlaskTask(Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(__name__)
    celery_app.Task = FlaskTask
    return celery_app
celery = celery_init_app()

