import os
import torch
from torchvision import transforms
from PIL import Image
import numpy as np

# Adjust import assuming inference.py is run from src/ml or imported by api
from src.ml.models.cnn import UNet

class Dehazer:
    def __init__(self, model_path, device=None):
        if device is None:
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        else:
            self.device = device
            
        self.model = UNet().to(self.device)
        
        # Load weights if model exists
        if os.path.exists(model_path):
            # map_location ensures we can load a cuda model on cpu
            self.model.load_state_dict(torch.load(model_path, map_location=self.device))
            self.model.eval()
        else:
            print(f"Warning: Model weights not found at {model_path}. Using uninitialized weights.")
            self.model.eval()

        self.transform = transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.ToTensor()
        ])

    def process_image(self, image: Image.Image) -> Image.Image:
        """
        Takes a PIL Image, processes it through the UNet, and returns the dehazed PIL Image.
        """
        # Ensure image is RGB
        image = image.convert("RGB")
        original_size = image.size
        
        # Preprocess
        input_tensor = self.transform(image).unsqueeze(0).to(self.device)
        
        # Inference
        with torch.no_grad():
            output_tensor = self.model(input_tensor)
            
        # Postprocess
        output_tensor = output_tensor.squeeze(0).cpu()
        output_image = transforms.ToPILImage()(output_tensor)
        
        # Resize back to original size
        output_image = output_image.resize(original_size, Image.Resampling.LANCZOS)
        
        return output_image
