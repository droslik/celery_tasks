import time
from celery.exceptions import Reject
from dotenv import load_dotenv
from celery import Celery
from celery.utils.log import get_task_logger
import celeryconfig

logger = get_task_logger(__name__)
load_dotenv()

celery_app = Celery(__name__)
celery_app.config_from_object(celeryconfig)
celery_app.autodiscover_tasks()


@celery_app.task(bind=True, acks_late=True)
def division(self, x, y):
    time.sleep(5)
    logger.info(f'Division {x} on {y}')
    try:
        return x / y
    except TypeError as exc:
        raise Reject(exc, requeue=False)
    except ZeroDivisionError as exc:
        #raise Reject(exc, requeue=False)
        raise self.retry(exc=exc, countdown=1, max_retries=3)


@celery_app.task(bind=True, acks_late=True)
def multiply(self, x, y):
    time.sleep(5)
    logger.info(f'Multiplying {x} by {y}')
    try:
        return x * y
    except TypeError as exc:
        raise Reject(exc, requeue=False)


@celery_app.task(bind=True, acks_late=True)
def multiply2(self, x, y):
    time.sleep(5)
    logger.info(f'Multiplying {x} by {y}')
    try:
        return x * y
    except TypeError as exc:
        raise Reject(exc, requeue=False)


@celery_app.task(bind=True, acks_late=True)
def add(self, x, y):
    time.sleep(5)
    logger.info(f'Adding {x} to {y}')
    try:
        return x + y
    except TypeError as exc:
        raise Reject(exc, requeue=False)


@celery_app.task(bind=True)
def sum_of_nums(self, numbers):
    return sum(numbers)

