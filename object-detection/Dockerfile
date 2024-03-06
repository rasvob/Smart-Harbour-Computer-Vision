# Use an official Python runtime as the base image
# FROM python:3.11.0-slim-bullseye as builder
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive 

# Set the working directory in the container
WORKDIR /app

RUN adduser --disabled-password --gecos '' appuser && chown -R appuser /app
USER appuser

RUN apt-get update && apt-get install -y vim python3.11 python3-pip python3.11-dev python3.11-venv python3.11-distutils python3-dotenv python3-opencv
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1
RUN pip install -user --upgrade pip
RUN pip install -user opencv-python

# # Copy the requirements file into the container
COPY requirements.txt .

RUN pip install -user --no-cache-dir wheel setuptools
RUN pip install -user --no-cache nvidia-tensorrt --index-url https://pypi.ngc.nvidia.com
RUN pip install -user --no-cache-dir -r requirements.txt

# CMD [ "/bin/bash" ]


# # Copy the rest of the application code into the container
COPY . .

RUN rm .env
RUN mv .env.docker .env

# Set the command to run when the container starts
CMD [ "python", "test_model_on_video_file.py" ]
