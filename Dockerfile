FROM python:3
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY manage.py /code/
COPY laboratiry_work_1 /code/laboratiry_work_1
COPY db.sqlite3 /code/
COPY final_project /code/final_project
