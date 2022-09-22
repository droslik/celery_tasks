from celery import chain, group, chord
from flask import Flask
from celery_manager import division, multiply, add, sum_of_nums

app = Flask(__name__)


@app.route('/')
def run_tasks():
    symbols = [4, 0, 'k']
    for i in range(len(symbols)):
        # simple task1
        task1 = division.apply_async(
            (10, symbols[i]),
            queue='division', priority=5)
        # simple task2
        task2 = multiply.apply_async(
            (10, symbols[i]),
            queue='multiply', priority=10)
        # group tasks
        job = group(
            [add.s(symbols[i], symbols[i]), add.s(10, symbols[i])]
        ).apply_async()
        # chain tasks
        task4 = chain(
            multiply.s(10, symbols[i]), division.s(symbols[i])
        ).apply_async()
    # chord tasks
    callback = sum_of_nums.s()
    header = [add.s(5, 5), add.s(3, 6), multiply.s(5, 2)]
    res = chord(header, callback)()
    return f'Tasks are running...'
