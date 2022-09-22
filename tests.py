from time import sleep
from celery import chain, chord
from celery.result import AsyncResult
from celery_manager import add, division, multiply, sum_of_nums
from fixtures import celeryapp, celery_worker


def test_add(celery_worker):
    task = division.delay(3, 0)
    sleep(30)
    assert task.state == 'FAILURE'
    assert isinstance(task.result, ZeroDivisionError)


def test_some_task(celery_worker):
    assert add.delay(4, 5).get() == 9


def test_chain(celery_worker):
    assert chain(add.s(3, 3), division.s(3)).apply_async().get() == 2
    task = chain(add.s(3, 3), division.s(3)).apply_async()
    sleep(15)
    assert AsyncResult(task.id)._get_task_meta()['status'] == 'SUCCESS'


def test_multiply(celery_worker):
    assert chord([multiply.s(3, 3), division.s(3, 3)], sum_of_nums.s())().get() == 10
    assert isinstance(multiply(5, 'k'), str)
    task = chord([multiply.s(3, 'k'), division.s(3, 3)], sum_of_numbers.s())()
    sleep(15)
    assert task.state == 'FAILURE'
    assert isinstance(task.result, TypeError)

