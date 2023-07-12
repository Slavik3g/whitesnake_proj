FROM python:3.11.1
MAINTAINER Slava Chebotarev "chebotarev.vs02@gmail.com"

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY ./CarshowroomProject /app

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
