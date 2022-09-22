#!/bin/sh

sleep 3

celery -A celery_manager worker -Q multiply -l info
