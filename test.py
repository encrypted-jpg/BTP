import os
import torch
import torch.optim as optim
import torch.nn as nn
from torch.utils.data import DataLoader
from datasets.PCNDataset import PCNDataset
from models.GED import GAN
from models.PCN import PCN
from loss.mse import MSELoss
from loss.cd import chamfer_distance
from extensions.chamfer_dist import ChamferDistanceL2
import time
from util.model_util import load_model
from util.pcd_util import save_pcd


test_data = PCNDataset("test")

test_dataloader = DataLoader(test_data, batch_size=2, shuffle=True)

input_size = 2048 * 3
hidden_size = 1024
latent_size = 128
output_size = 16384 * 3
# model = GAN(input_size, hidden_size, latent_size, output_size)
model = PCN()
model = load_model(model, "model.pth")

# Define a loss function (e.g. Mean Squared Error)
criterion = ChamferDistanceL2()

# Define an optimizer (e.g. Adam)
optimizer = optim.Adam(model.parameters(), lr=0.001)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Training on", device)
model.to(device)

test_output = os.path.join(os.getcwd(), "test_output")
SAVE_FILES = True

if not os.path.exists(test_output) and SAVE_FILES:
    os.makedirs(test_output)

with torch.no_grad():
    val_loss = 0.0
    start = time.time()
    for data in test_dataloader:
        tax, id, (partial_cloud, complete_cloud) = data
        partial_cloud, complete_cloud = partial_cloud.to(device), complete_cloud.to(device)
        coarse, outputs = model(partial_cloud)
        outputs = outputs.to(device)
        complete_cloud = complete_cloud.to(device)
        loss = criterion(outputs, complete_cloud)
        val_loss += loss.item()
        if SAVE_FILES:
            for idx in range(partial_cloud.shape[0]):
                pc = partial_cloud[idx].detach().cpu().numpy()
                cc = complete_cloud[idx].detach().cpu().numpy()
                out = outputs[idx].detach().cpu().numpy()
                save_pcd(os.path.join(test_output, f"{id[idx]}_input.pcd"), pc)
                save_pcd(os.path.join(test_output, f"{id[idx]}_gt.pcd"), cc)
                save_pcd(os.path.join(test_output, f"{id[idx]}_output.pcd"), out)
    val_loss = val_loss / len(test_dataloader)
    print(f"Test Loss: {val_loss:.4f}, Time: {round(time.time() - start, 3)}s")


