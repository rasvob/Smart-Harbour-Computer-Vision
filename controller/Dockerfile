FROM python:3.11-bookworm as builder

ENV DEBIAN_FRONTEND=noninteractive 

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 iputils-ping net-tools iproute2  -y

# Set the working directory in the container
WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --user --no-cache-dir wheel setuptools
RUN python -m pip install --user --no-cache-dir -r requirements.txt

FROM builder as runner
COPY /app .
CMD ["python", "main.py"]