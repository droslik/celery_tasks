import pytest
from celery_manager import celery_app


@pytest.fixture(scope='session')
def celeryapp(request):
    celery_app.conf.update(CELERY_ALWAYS_EAGER=True)
    return celery_app


@pytest.fixture(scope='session')
def celery_worker():
    return {
        'broker_url': 'amqp://',
        'result_backend': 'redis://'
    }
