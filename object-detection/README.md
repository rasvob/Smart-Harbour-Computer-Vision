# Object detection API using fine-tuned YOLOv8x

## Build
* Put `<model>.pt` PyTorch model into the `./models` directory
    * Modify filenames in `.env.docker.build` if needed
    * Exported model name should be `best.engine` - otherwise it is needed to modity `Dockerfile` with different filename

* Run `build_docker.sh` script to export the TensorRT model
* Serve the API
    * Run the server: `docker compose up` or `docker compose up -d`