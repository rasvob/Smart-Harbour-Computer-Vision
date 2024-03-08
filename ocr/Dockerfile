# Use an official Python runtime as a parent image
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive 

# Set the working directory in the container
WORKDIR /app

RUN apt-get update && apt-get install -y vim python3.11 python3-pip python3.11-dev python3.11-venv python3.11-distutils
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
RUN apt-get install -y python3-dotenv python3-opencv

RUN adduser --disabled-password --gecos '' appuser && chown -R appuser:appuser /app
USER appuser

RUN python -m pip install --user --upgrade pip
RUN python -m pip install --user opencv-python

# # Copy the requirements file into the container
COPY requirements.txt .

RUN python -m pip install --user --no-cache-dir wheel setuptools
#RUN python -m pip install --user --no-cache-dir tensorrt==8.6.1
RUN python -m pip install --user --no-cache-dir -r requirements.txt

# # Copy the rest of the application code into the container
COPY . .


# Make port available to the world outside this container
EXPOSE 5000

CMD ["./run.sh"]


# For fixing ImportError: libGL.so.1: cannot open shared object file: No such file or directory
# RUN apt-get update
# RUN apt install -y libgl1-mesa-glx libglib2.0-0 libsm6 libxrender1 libxext6
