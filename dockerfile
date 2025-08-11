FROM python:3.11-slim


ENV PYTHONDONTWRITEBYTECODE=1
#Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1 


WORKDIR /app


COPY requirements.txt /app/



RUN pip3 install --upgrade pip


RUN pip install --no-cache-dir -r requirements.txt 


COPY ./core /app

