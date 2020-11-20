#!/bin/bash
celery -A dreamer worker --loglevel=INFO --logfile=/var/log/celery/celery.log --time-limit=300 --autoscale=6,2