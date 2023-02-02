import torch

def chamfer_distance(outputs, targets):
    batch_size = outputs.shape[0]
    # Calculate the pairwise distances between points in the two point clouds
    distances = torch.sum((outputs[:, None] - targets[None]) ** 2, dim=-1)

    # Calculate the minimum distance from each point in y_pred to a point in y_true
    min_distances_pred, _ = distances.min(dim=1)

    # Calculate the minimum distance from each point in y_true to a point in y_pred
    min_distances_true, _ = distances.min(dim=0)

    # Calculate the Chamfer distance as the mean of the minimum distances
    chamfer_distance = (torch.sum(min_distances_pred) + torch.sum(min_distances_true)) / (2 * batch_size * outputs.shape[1])

    return chamfer_distance
