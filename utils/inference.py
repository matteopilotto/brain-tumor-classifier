
import torch
from torch import nn
from torchvision.models import efficientnet_b0

labels = ["glioma", "meningioma", "notumor", "pituitary"]
checkpoint_filename = "./models/efficientnet_b0_20241116_121021.pth"

if torch.cuda.is_available():
    device = torch.device("cuda")
elif torch.backends.mps.is_available():
    device = torch.device("mps")
else:
    device = torch.device("cpu")


def load_checkpoint(checkpoint_filename):
    model = efficientnet_b0(weights=None)
    model.classifier[1] = nn.Linear(1280, 4)
    model.load_state_dict(torch.load(checkpoint_filename, map_location="cpu", weights_only=True))
    model = model.to(device)

    return model


def make_prediction(model, image_tensor):
    model.eval()
    with torch.inference_mode():
        logits = model(image_tensor)
        probs = torch.softmax(logits, dim=-1).detach().cpu().squeeze().numpy().tolist()
        pred_idx = torch.argmax(logits, dim=-1).item()
        pred_label = labels[pred_idx]

    return pred_label, probs