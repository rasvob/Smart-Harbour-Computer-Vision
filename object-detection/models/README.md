# Models tested on RTX 3090 24GB and 4080 16GB

| Model     | VRAM   | No boat (ms) | Boat (ms) |
|-----------|--------|--------------|-----------|
| YOLOv8x - RT    | 2,5 GB    | 100  | 150      |
| **YOLOv8x - RT - HalfP**    | 1,6 GB    | 30  | 30      |
| **YOLOv8x - Docker - RT - HalfP - RTX 4080**    | 1,1 GB    | 21 (50 full-pipeline)  | 21      |
| **YOLOv8x - Docker - RT - HalfP**    | 1,6 GB    | 30  | 30      |
| **YOLOv8x - 2x Docker 1 GPU - RT - HalfP**    | 1,6 GB    | 60  | 60      |
| YOLOv8x - Torch    | 3,5 GB    | 70  | 80    |
| YOLOv8x - Torch - RTX 4080    | 2 GB    | 50  | 50    |
| YOLOv8x - ONNX    | 17 GB    | 130  | 180     |
| YOLOv8m - ONNX    | 4,2 GB    | 70  | 90     |
| YOLOv8m - Torch    | 2,4 GB    | 26  | 28     |