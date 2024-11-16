from PIL import Image
import numpy as np
from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget
from pytorch_grad_cam.utils.image import show_cam_on_image

def compute_gradcam(model, input_image, input_tensor, pred_label):
    labels = ['glioma', 'meningioma', 'notumor', 'pituitary']
    image_resized = input_image.resize((224, 224))
    image_np = np.array(image_resized).astype(np.float32) / 255.0

    target_layers = [model.features[-1]]
    targets = [ClassifierOutputTarget(labels.index(pred_label))]

    with GradCAM(model=model, target_layers=target_layers) as cam:
        # You can also pass aug_smooth=True and eigen_smooth=True, to apply smoothing.
        grayscale_cam = cam(input_tensor=input_tensor, targets=targets)
        # In this example grayscale_cam has only one image in the batch:
        grayscale_cam = grayscale_cam[0, :]
        visualization = show_cam_on_image(image_np, grayscale_cam, use_rgb=True)
        # You can also get the model outputs without having to redo inference
        model_outputs = cam.outputs
    
    gradcam_image = Image.fromarray(visualization)

    return image_resized, gradcam_image