from fastapi import FastAPI, HTTPException
import base64
from src.ocr_model import OCRModel
from src.dto import ImageModel
from contextlib import asynccontextmanager

app_services = {
    'OCRModel': None   
}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the ML models
    app_services['OCRModel'] = OCRModel()
    yield
    # Clean up the ML models and release the resources

app = FastAPI(lifespan=lifespan)

@app.get('/')
def read_root():
    return {'Message': 'OCR module up and running.'}

@app.post("/serve")
async def serve(data: ImageModel):
    try:
        # Decode the base64 string
        image_data = base64.b64decode(data.image)
        result = app_services['OCRModel'].readtext_postprocess(image_data)
        return result
    except Exception as e:
        # logger.exception(e)
        print(e)
        raise HTTPException(status_code=400, detail="Invalid base64 image data")
