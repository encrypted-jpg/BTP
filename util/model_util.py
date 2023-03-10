import torch

# Save the model
def save_model(model, file_path):
    torch.save(model.state_dict(), file_path)

# Load the model
def load_model(model, file_path):
    model.load_state_dict(torch.load(file_path))
    return model

