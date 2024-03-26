FROM petrov-rtx:base as server
COPY /models/best.engine /app/models/
COPY /app /app
CMD [ "python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8013"]