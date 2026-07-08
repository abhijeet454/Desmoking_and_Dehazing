import os
import cv2
import torch
from torch.utils.data import Dataset
from torchvision import transforms

class HazyDataset(Dataset):
    def __init__(self, image_dir, transform=None):
        self.image_dir = image_dir
        self.transform = transform
        self.image_pairs = self._get_image_pairs()

    def _get_image_pairs(self):
        images = sorted([f for f in os.listdir(self.image_dir) if f.endswith('.png')])
        hazy_images = [img for img in images if img.endswith('_hazy.png')]
        gt_images = [img for img in images if img.endswith('_GT.png')]
        image_pairs = []
        for hazy_img in hazy_images:
            base_name = hazy_img.split('_hazy')[0]
            gt_img = base_name + '_GT.png'
            if gt_img in gt_images:
                image_pairs.append((hazy_img, gt_img))
        return image_pairs

    def __len__(self):
        return len(self.image_pairs)

    def __getitem__(self, idx):
        hazy_img, gt_img = self.image_pairs[idx]
        hazy_path = os.path.join(self.image_dir, hazy_img)
        gt_path = os.path.join(self.image_dir, gt_img)

        hazy = cv2.imread(hazy_path)
        gt = cv2.imread(gt_path)
        
        # OpenCV loads as BGR, convert to RGB
        if hazy is not None:
            hazy = cv2.cvtColor(hazy, cv2.COLOR_BGR2RGB)
        if gt is not None:
            gt = cv2.cvtColor(gt, cv2.COLOR_BGR2RGB)

        if self.transform:
            hazy = self.transform(hazy)
            gt = self.transform(gt)

        return hazy, gt

# Default Transformation pipeline
default_transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((256, 256)),
    transforms.ToTensor()
])
