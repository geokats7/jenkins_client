# Use a slim version of Python 3.10 as base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy only the requirements file for poetry to the working directory
COPY ./poetry-requirements.txt poetry-requirements.txt

# Install Python dependencies from the poetry requirements file
RUN pip install --no-cache-dir -r poetry-requirements.txt

# Copy the project metadata files to the working directory
COPY pyproject.toml poetry.lock* ./

# Configure poetry to not create a virtual environment
RUN poetry config virtualenvs.create false

# Install project dependencies using poetry with caching enabled
RUN --mount=type=cache,target=/root/.cache/pypoetry poetry install --no-interaction --no-root

# Copy your application code
COPY jenkins_client/client.py /app/client.py

# Set the entrypoint
ENTRYPOINT ["python", "-u", "/app/client.py", "start_job"]
