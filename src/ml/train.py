import os
import argparse
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader

from models.cnn import UNet
from data.dataset import HazyDataset, default_transform

def train(args):
    # Setup device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")

    # Dataset and DataLoader
    dataset = HazyDataset(args.data_dir, transform=default_transform)
    dataloader = DataLoader(dataset, batch_size=args.batch_size, shuffle=True)

    # Model, Loss, Optimizer
    model = UNet().to(device)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=args.learning_rate)

    # Training Loop
    for epoch in range(args.num_epochs):
        model.train()
        running_loss = 0.0
        for hazy, gt in dataloader:
            hazy, gt = hazy.to(device), gt.to(device)
            
            optimizer.zero_grad()
            outputs = model(hazy)
            loss = criterion(outputs, gt)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item() * hazy.size(0)

        epoch_loss = running_loss / len(dataset)
        print(f'Epoch [{epoch+1}/{args.num_epochs}], Loss: {epoch_loss:.4f}')

    # Save the model
    os.makedirs(args.save_dir, exist_ok=True)
    save_path = os.path.join(args.save_dir, 'unet_dehazing_model.pth')
    torch.save(model.state_dict(), save_path)
    print(f"Model saved to {save_path}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Train UNet for Image Dehazing")
    parser.add_argument('--data_dir', type=str, required=True, help='Directory containing the dataset')
    parser.add_argument('--batch_size', type=int, default=4, help='Batch size for training')
    parser.add_argument('--learning_rate', type=float, default=0.001, help='Learning rate')
    parser.add_argument('--num_epochs', type=int, default=50, help='Number of training epochs')
    parser.add_argument('--save_dir', type=str, default='checkpoints', help='Directory to save the trained model')
    
    args = parser.parse_args()
    train(args)
