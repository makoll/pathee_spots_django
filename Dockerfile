FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir -p /var/www/docker_django
WORKDIR /var/www/docker_django
ADD requirements.txt /var/www/docker_django/
RUN pip install -r requirements.txt
ADD . /var/www/docker_django/
