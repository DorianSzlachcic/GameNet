FROM python:3.10

COPY . ./

RUN pip install -r requirements.txt

EXPOSE 8080

RUN python manage.py collectstatic --noinput
CMD exec gunicorn --bind :8080 --workers 1 --threads 8 --timeout 0 GameNet.wsgi
