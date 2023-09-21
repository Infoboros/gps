FROM --platform=linux/amd64 python:3.8

RUN touch /var/run/uwsgi-touch-reload
COPY . .
RUN pip install --no-cache-dir -r requirements
