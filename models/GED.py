import torch
import torch.nn as nn


class Encoder(nn.Module):
    def __init__(self, input_size, hidden_size, latent_size):
        super().__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, latent_size)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = x.view(-1, 2048 * 3)  # Reshape x to handle the batch size correctly
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return x


class Decoder(nn.Module):
    def __init__(self, latent_size, hidden_size, output_size):
        super().__init__()
        self.fc1 = nn.Linear(latent_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, output_size)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        x = x.view(-1, 16384, 3)
        return x


class GAN(nn.Module):
    def __init__(self, input_size, hidden_size, latent_size, output_size):
        super().__init__()
        self.encoder = Encoder(input_size, hidden_size, latent_size)
        self.decoder = Decoder(latent_size, hidden_size, output_size)

    def forward(self, x):
        x = self.encoder(x)
        x = self.decoder(x)
        return x
