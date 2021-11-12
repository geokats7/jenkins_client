FROM python:3.9-alpine

COPY requirements.txt /app/requirements.txt

RUN pip install -r app/requirements.txt

COPY jenkins_client /app/jenkins_client

ENTRYPOINT ["python", "app/jenkins_client/client.py", "start_job"]