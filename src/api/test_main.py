import pytest
from fastapi.testclient import TestClient
import io
from PIL import Image
import os
import sys

# Ensure src module is discoverable for testing
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from src.api.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_dehaze_image_invalid_file():
    # Test with non-image file
    response = client.post(
        "/api/dehaze",
        files={"file": ("test.txt", b"this is a text file", "text/plain")}
    )
    assert response.status_code == 400
    assert "File must be an image" in response.json()["detail"]

def test_dehaze_image_success():
    # Create a dummy image
    img = Image.new('RGB', (100, 100), color = 'red')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    
    response = client.post(
        "/api/dehaze",
        files={"file": ("test.png", img_byte_arr, "image/png")}
    )
    
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    
    # Check if the returned byte stream is actually a valid image
    result_img = Image.open(io.BytesIO(response.content))
    assert result_img.size == (100, 100)
