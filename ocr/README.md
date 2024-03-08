# EasyOCR


During the initial experiment and testing of the architecture, the observations are as follows:

The EasyOCR runs behind the FlaskAPI, base64 image is the parameter.

The first experiments processed the whole 1920x1080 pictures, without cropping or any other operation.
In case of GPU=False, the approximate ~3 sec per frame was needed.
In case of GPU=True, the approximate time was  ~0.25 sec per frame. With the allocation of ~3.3 GB GPU memory.

In case of 1/4 of the immage (960x540), the GPU inference time was about ~0.12sec per frame with ~1 GB GPU memory
