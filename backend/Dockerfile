FROM python:3.9.15-alpine3.17
WORKDIR /backend
COPY requirements.txt /backend/
RUN pip install -r requirements.txt
COPY . /backend
RUN python manage.py makemigrations 
RUN python manage.py migrate 
RUN python manage.py import_airports

