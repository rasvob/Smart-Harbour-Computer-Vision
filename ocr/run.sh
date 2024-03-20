#!/bin/bash

# Start the server in the background
python -m uvicorn run:app --host 0.0.0.0 --port 5000 &

# Wait for the server to start
sleep 30

# Run the testing script
python test_ocr.py