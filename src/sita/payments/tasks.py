from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from .utils import generate_payment

logger = get_task_logger(__name__)

@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="generate_payment_task",
    ignore_result=True
)
def generate_payment_task():
    """"""

    logger.info("Saved image from Flickr")
    return generate_payment()
