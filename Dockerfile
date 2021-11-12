FROM python:3.9-alpine

COPY requirements.txt /requirements.txt

RUN pip install -r requirements.txt

COPY jenkins_client/client.py /client.py

ENTRYPOINT ["python", "/client.py", "start_job"]