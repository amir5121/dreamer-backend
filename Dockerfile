FROM python:3.7-alpine
ENV PYTHONUNBUFFERED 1

ENV PROJECT_PATH /srv/dreamer/

RUN mkdir $PROJECT_PATH
WORKDIR $PROJECT_PATH
COPY requirements.txt $PROJECT_PATH

RUN apk add --no-cache  postgresql-dev jpeg-dev libmagic libxslt-dev freetype-dev
RUN apk add --no-cache --virtual .build-deps build-base libffi-dev zlib-dev libxml2 g++ jpeg-dev

ADD ./requirements.txt /srv/dreamer/requirements.txt

RUN pip install --upgrade pip 
RUN pip install -r requirements.txt 

RUN find /usr/local \
    \( -type d -a -name test -o -name tests \) \
    -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
    -exec rm -rf '{}' + 

RUN runDeps="$( \
    scanelf --needed --nobanner --recursive /usr/local \
    | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
    | sort -u \
    | xargs -r apk info --installed \
    | sort -u \
    )" 

RUN apk add --virtual .rundeps $runDeps 

RUN apk del .build-deps

RUN echo http://dl-2.alpinelinux.org/alpine/edge/community/ >> /etc/apk/repositories
RUN apk --no-cache add shadow
RUN adduser -s /bin/sh -D dreamer
RUN usermod -u 1000 dreamer
RUN groupmod -g 1000 dreamer

RUN mkdir /var/log/celery
RUN mkdir /var/run/celery

RUN chown -R dreamer:dreamer /var/log/celery
RUN chown -R dreamer:dreamer /var/run/celery
RUN chown -R dreamer:dreamer $PROJECT_PATH

USER dreamer
