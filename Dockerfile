FROM python:3.9-alpine

COPY requirements.txt /app/requirements.txt

RUN pip install -r app/requirements.txt

COPY jenkins_client app/jenkins_client

WORKDIR /app/jenkins_client

ENTRYPOINT ["python", "client.py", "start_job"]