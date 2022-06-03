FROM python:3.8-alpine
ENV PYTHONUNBUFFERED 1
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1

ENV PROJECT_PATH /srv/dreamer/

RUN mkdir $PROJECT_PATH
WORKDIR $PROJECT_PATH

RUN echo http://dl-2.alpinelinux.org/alpine/edge/community/ >> /etc/apk/repositories
RUN apk add --no-cache \
    postgresql-dev \
    jpeg-dev \
    libmagic \
    libxslt-dev \
    freetype-dev \
    shadow \
    lapack \
    libstdc++ \
    ffmpeg
RUN apk add --no-cache --virtual .build-deps \
    build-base \
    libffi-dev \
    zlib-dev \
    libxml2 \
    g++ \
    gfortran \
    linux-headers \
    musl-dev \
    lapack-dev
ADD ./requirements.txt /srv/dreamer/requirements.txt

RUN pip install --upgrade pip 
RUN pip install -r requirements.txt 

RUN rm -rf /root/.cache

#RUN find /usr/local \
#    \( -type d -a -name test -o -name tests \) \
#    -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
#    -exec rm -rf '{}' +
#RUN runDeps="$( \
#    scanelf --needed --nobanner --recursive /usr/local \
#    | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
#    | sort -u \
#    | xargs -r apk info --installed \
#    | sort -u \
#    )"
#RUN apk add --virtual .rundeps $runDeps
#RUN apk del .build-deps

RUN adduser -s /bin/sh -D dreamer
RUN usermod -u 1000 dreamer
RUN groupmod -g 1000 dreamer

RUN mkdir /var/log/celery
RUN mkdir /var/run/celery

RUN chown -R dreamer:dreamer /var/log/celery
RUN chown -R dreamer:dreamer /var/run/celery
RUN chown -R dreamer:dreamer $PROJECT_PATH

USER dreamer
