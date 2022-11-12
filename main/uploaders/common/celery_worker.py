from main.uploaders.common.celery import celery
from main import create_app

app = create_app()
app.app_context().push()

from main.uploaders.run_faceyelp import start
