#!/bin/bash
celery -A dreamer beat --logfile=/var/log/dreamer/celery/beat.log --loglevel=INFO --schedule=/var/run/celery/celerybeat-schedule
