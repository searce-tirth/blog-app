# Use a base image with Python pre-installed
FROM python:3.9-slim-buster

WORKDIR /app
COPY . /app

# install requirements.txt
RUN pip install -r requirements.txt

# Run Python command
CMD ["python3", "main.py"]
