# Use an official Python runtime as the base image
FROM python:3.11.0-slim-bullseye

# Set the working directory in the container
WORKDIR /app

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
