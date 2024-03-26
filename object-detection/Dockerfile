FROM petrov-rtx:base as server
COPY /models/best.engine /app/models/
COPY /certs /app/certs
COPY /app /app
CMD [ "python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8013", "--ssl-keyfile", "/app/certs/key.pem", "--ssl-certfile", "/app/certs/cert.pem"]