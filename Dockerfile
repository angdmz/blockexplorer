FROM python:3.5-alpine
RUN apk --update add \
    build-base \
    postgresql \
    postgresql-dev \
    libpq
RUN apk add --no-cache \
    git \
    libffi-dev
RUN mkdir -p /opt/project
WORKDIR /opt/project
COPY requirements.txt /opt/project
RUN pip install -U pip
RUN pip install -r requirements.txt
RUN pip install ipython
RUN pip install coverage
RUN pip install django-discover-runner
ADD . /opt/project
