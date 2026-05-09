from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil

# Import your core logic
from encoder import encode_image
from decoder import decode_image

app = FastAPI(title="Phishnet Sentinel - Steganography API")

# Allow the frontend to talk to this API (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, change this to your actual frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

# Ensure directories exist
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/api/encode")
async def api_encode(
    file: UploadFile = File(...),
    message: str = Form(...),
    password: str = Form(...)
):
    print(f"[API] Received encode request for: {file.filename}")
    
    # 1. Save the uploaded file temporarily
    input_path = os.path.join(UPLOAD_DIR, file.filename)
    output_filename = f"encoded_{file.filename.split('.')[0]}.png"
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 2. Run the Steganography Encoder
    success = encode_image(input_path, message, password, output_path)

    # 3. Clean up the original upload and return the result
    os.remove(input_path) 

    if success:
        # Send the file back to the browser for download
        return FileResponse(output_path, media_type="image/png", filename=output_filename)
    else:
        raise HTTPException(status_code=400, detail="Encoding failed. Image may be too small.")

@app.post("/api/decode")
async def api_decode(
    file: UploadFile = File(...),
    password: str = Form(...)
):
    print(f"[API] Received decode request for: {file.filename}")
    
    # 1. Save the uploaded file temporarily
    input_path = os.path.join(UPLOAD_DIR, file.filename)
    
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 2. Run the Steganography Decoder
    result = decode_image(input_path, password)

    # 3. Clean up the uploaded file
    os.remove(input_path)

    if "[ERROR]" in result or "No hidden message" in result:
        raise HTTPException(status_code=400, detail=result)
    
    # Return the secret text as JSON
    return {"status": "success", "secret_message": result}