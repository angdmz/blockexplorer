FROM python:3.6
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils
RUN apt-get update && apt-get -y upgrade && apt-get install -y apt-transport-https software-properties-common libsasl2-dev python-dev libldap2-dev libssl-dev unixodbc unixodbc-dev tdsodbc memcached
RUN apt-get install -y gettext
RUN mkdir -p /codigo/
WORKDIR /codigo
ADD requirements.txt /codigo/
RUN pip install -U pip
RUN pip install -r requirements.txt
RUN pip install ipython
ADD . /codigo/
