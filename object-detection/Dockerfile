# Use an official Python runtime as the base image
FROM python:3.11.0-slim-bullseye as builder

# Set the working directory in the container
WORKDIR /app

RUN apt-get update && apt-get install -y python3-opencv
RUN pip install opencv-python

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

RUN rm .env
RUN mv .env.docker .env

# Set the command to run when the container starts
CMD [ "python", "test_model_on_video_file.py" ]
