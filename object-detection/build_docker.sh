#!/bin/bash
docker build -t petrov-rtx:base -f Dockerfile.base .
docker build -t petrov-rtx:export -f Dockerfile.export .
docker run --gpus all --volume $(pwd)/models:/app/models petrov-rtx:export
docker compose build