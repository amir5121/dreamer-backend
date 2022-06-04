#!/bin/bash
celery -A dreamer worker --loglevel=INFO --logfile=/var/log/dreamer/celery/celery.log --time-limit=300 --autoscale=3,1
