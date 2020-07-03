FROM python:3.8-slim

RUN apt-get update -q && \
    apt-get install -yq default-libmysqlclient-dev python3-dev libssl-dev build-essential

ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip

WORKDIR /app

COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]