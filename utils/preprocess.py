import PIL
import torch
from torchvision.models.efficientnet import EfficientNet_B0_Weights

if torch.cuda.is_available():
    device = torch.device("cuda")
elif torch.backends.mps.is_available():
    device = torch.device("mps")
else:
    device = torch.device("cpu")

weights = EfficientNet_B0_Weights.IMAGENET1K_V1
preprocess = weights.transforms()

def preprocess_image(image: PIL.Image) -> torch.Tensor:
    image_tensor = preprocess(image)
    return image_tensor.to(device).unsqueeze(0)