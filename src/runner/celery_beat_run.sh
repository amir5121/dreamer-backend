#!/bin/bash
celery -A dreamer beat --logfile=/var/log/celery/beat.log --loglevel=INFO --schedule=/var/run/celery/celerybeat-schedule
