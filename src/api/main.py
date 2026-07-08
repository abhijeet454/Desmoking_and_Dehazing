from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import io
from PIL import Image
import os
import sys

# Ensure src module is discoverable
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from src.ml.inference import Dehazer

app = FastAPI(title="Dehazing API", description="API for image desmoking and dehazing using UNet", version="1.0.0")

# Setup CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Dehazer
# Looking for weights in a default location, or it will use uninitialized weights for demo
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'unet_dehazing_model.pth')
dehazer = Dehazer(model_path=MODEL_PATH)

@app.post("/api/dehaze", summary="Dehaze an uploaded image")
async def dehaze_image(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")

    try:
        # Read image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Process image
        dehazed_image = dehazer.process_image(image)
        
        # Convert back to bytes
        img_byte_arr = io.BytesIO()
        dehazed_image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        return StreamingResponse(img_byte_arr, media_type="image/png")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health", summary="Health check endpoint")
async def health_check():
    return {"status": "healthy"}
