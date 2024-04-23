#!/bin/bash
ffmpeg -re -stream_loop 1 -i $VIDEO_FILE -c copy -f rtsp $STREAM_URL