FROM python:3.5-alpine
RUN apk --update add \
    build-base \
    postgresql \
    postgresql-dev \
    libpq
RUN apk add --no-cache \
    git \
    libffi-dev
RUN mkdir -p /opt/project/staticfiles
WORKDIR /opt/project
COPY requirements.txt /opt/project
RUN pip install -U pip
RUN pip install -r requirements.txt
RUN pip install gunicorn
ADD . /opt/project
ENV HOME=/opt/project
ENV APP_HOME=/opt/project