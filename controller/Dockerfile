FROM python:3.11-bookworm as builder

ENV DEBIAN_FRONTEND=noninteractive 
ENV PDM_CHECK_UPDATE=false

WORKDIR /app
RUN mkdir -p /app/data
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 iputils-ping net-tools iproute2  -y
RUN pip install -U pip setuptools wheel
RUN pip install -U pdm

COPY pyproject.toml pdm.lock /app/
RUN pdm config python.use_venv False
RUN pdm install --check --prod --no-editable

FROM builder as runner
COPY /src /app/src
CMD ["pdm", "run", "start-production"]
# CMD ["python", "main.py"]
# CMD [ "/bin/bash" ]