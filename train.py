import torch
import torch.optim as optim
import torch.nn as nn
from torch.utils.data import DataLoader
from datasets.PCNDataset import PCNDataset
from models.GED import GAN
from models.PCN import PCN
from loss.cd import chamfer_distance
from extensions.chamfer_dist import ChamferDistanceL2
import time
from util.model_util import save_model

train_data = PCNDataset()
val_data = PCNDataset("val")

BATCH_SIZE = 4

train_dataloader = DataLoader(train_data, batch_size=BATCH_SIZE, shuffle=True)
val_dataloader = DataLoader(val_data, batch_size=BATCH_SIZE, shuffle=True)

input_size = 2048 * 3
hidden_size = 1024
latent_size = 128
output_size = 16384 * 3
# model = GAN(input_size, hidden_size, latent_size, output_size)
model = PCN()

# Define a loss function (e.g. Mean Squared Error)
criterion = ChamferDistanceL2()

# Define an optimizer (e.g. Adam)
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training loop

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Training on", device)
model.to(device)

num_epochs = 20
patience = 3
best_loss = float("inf")
early_stopping = 0

for epoch in range(num_epochs):
    start = time.time()
    running_loss = 0.0
    for i, data in enumerate(train_dataloader, 0):
        tax, id, (partial_cloud, complete_cloud) = data
        partial_cloud, complete_cloud = partial_cloud.to(device), complete_cloud.to(device)
        optimizer.zero_grad()
        coarse, outputs = model(partial_cloud)
        outputs = outputs.to(device)
        complete_cloud = complete_cloud.to(device)
        loss = criterion(outputs, complete_cloud)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
    train_loss = running_loss / len(train_dataloader)
    print(f"Epoch [{epoch+1}/{num_epochs}], Train Loss: {train_loss:.4f}, Time: {round(time.time() - start, 3)}s")
    
    if (epoch+1)%5 == 0:
        with torch.no_grad():
            val_loss = 0.0
            val_start = time.time()
            for data in val_dataloader:
                tax, id, (partial_cloud, complete_cloud) = data
                partial_cloud, complete_cloud = partial_cloud.to(device), complete_cloud.to(device)
                coarse, outputs = model(partial_cloud)
                outputs = outputs.to(device)
                complete_cloud = complete_cloud.to(device)
                loss = criterion(outputs, complete_cloud)
                val_loss += loss.item()
            val_loss = val_loss / len(val_dataloader)
            print(f"Epoch [{epoch+1}/{num_epochs}], Validation Loss: {val_loss:.4f}, Time: {round(time.time() - val_start, 3)}s")
        
        if val_loss < best_loss:
            best_loss = val_loss
            save_model(model, "model.pth")
            early_stopping = 0
        else:
            early_stopping += 1
            if early_stopping >= patience:
                break

