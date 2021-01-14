#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

mkdir "/var/log/dreamer"
mkdir "/var/log/dreamer/celery"
mkdir "/var/log/dreamer/postgresql_docker_dreamer"
mkdir "/etc/postgresql_docker_dreamer"
