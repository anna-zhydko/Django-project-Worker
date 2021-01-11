FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


WORKDIR /usr/src/workerapp

COPY requirements.txt /usr/src/requirements.txt
RUN pip install -r /usr/src/requirements.txt

COPY . /usr/src/workerapp

# EXPOSE 8000
#
# CMD ["python", "manage.py", "makemigrations"]
# CMD ["python", "manage.py", "migrate"]
# CMD ["python", "manage.py", "runserver", "127.0.0.1:8000"]



