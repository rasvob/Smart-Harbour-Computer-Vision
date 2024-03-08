#!/bin/bash

# Start the server in the background
python src/flask_api.py &

# Wait for the server to start
sleep 30

# Run the testing script
python test_ocr.py