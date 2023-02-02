import torch

def MSELoss(outputs, targets):
    return torch.mean(torch.norm(outputs - targets, dim=2))
