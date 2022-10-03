from dotenv import load_dotenv
import os
from kombu import Exchange, Queue

load_dotenv()

broker_url = os.getenv('CELERY_BROKER_URL')
result_backend = os.getenv('CELERY_RESULT_BACKEND')

accept_content = [os.getenv('CELERY_ACCEPT_CONTENT')]
result_serializer = os.getenv('CELERY_RESULT_SERIALIZER')
task_serializer = os.getenv('CELERY_TASK_SERIALIZER')

default_queue_name = 'celery'
default_exchange_name = 'celery'
default_routing_key = 'celery'

division_queue_name = 'division'
division_routing_key = 'division'

multiply_queue_name = 'multiply'
multiply_routing_key = 'multiply'

default_exchange = Exchange(default_exchange_name, type='direct')
default_queue = Queue(
    default_queue_name,
    default_exchange,
    routing_key=default_routing_key
)

division_queue = Queue(
    division_queue_name,
    default_exchange,
    routing_key=division_routing_key,
)
multiply_queue = Queue(
    multiply_queue_name,
    default_exchange,
    routing_key=multiply_routing_key
)

task_queues = (default_queue, division_queue, multiply_queue)

task_routes = (
    [('celery_manager.division', {'queue': division_queue}),
    ('celery_manager.multiply', {'queue': multiply_queue}),
    ('celery_manager.*', {'queue': default_queue})],
)

result_backend_transport_options = {
    'retry_policy': {
       'timeout': 5.0
    }
}

beat_schedule = {
    'multiply-every-15-seconds': {
        'task': 'celery_manager.multiply2',
        'schedule': 60.0,
        'args': (10, 4)
    },
}

timezone = 'UTC'

