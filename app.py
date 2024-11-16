
import streamlit as st
from PIL import Image
import io
import torch
from utils.preprocess import preprocess_image
from utils.inference import load_checkpoint, make_prediction
from utils.gradcam import compute_gradcam

import base64

st.title("Brain Tumor Detection")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
checkpoint_path =  "./models/efficientnet_b0_20241116_121021.pth"
model = load_checkpoint(checkpoint_path)

def image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    return img_str

if uploaded_file:
    image = Image.open(io.BytesIO(uploaded_file.read())).convert("RGB")
    image_tensor = preprocess_image(image)
    label, probs = make_prediction(model, image_tensor)
    image_resized, gradcam_image = compute_gradcam(model, image, image_tensor, label)
    img_str = image_to_base64(image)
    gradcam_str = image_to_base64(gradcam_image)
    st.markdown(
        f"""
        <div style="display: flex; flex-direction: column; align-items: center;">
            <div style="display: flex; flex-direction: row; align-items: center; gap: 20px;">
                <div style="display: flex; flex-direction: column; align-items: center;">
                    <img src="data:image/jpeg;base64,{img_str}" style="width: 300px; height: 300px; border-radius: 10px;">
                    <p style="text-align: center;">Original</p>
                </div>
                <div style="display: flex; flex-direction: column; align-items: center;">
                    <img src="data:image/jpeg;base64,{gradcam_str}" style="width: 300px; height: 300px; border-radius: 10px;">
                    <p style="text-align: center;">Saliency Map</p>
                </div>
            </div>
            <div style="display: flex; flex-direction: row; gap: 150px;">
                <div style="display: flex; flex-direction: column;">
                    <p style="text-align: center; font-size: 25px; font-weight: semibold; opacity: 0.75; margin-bottom: 0px;">Prediction</p>
                    <p style="text-align: center; font-size: 45px; font-weight: bold; text-transform: capitalize; margin-top: -10px;">{label}</p>
                </div>
                <div style="display: flex; flex-direction: column;">
                    <p style="text-align: center; font-size: 25px; font-weight: semibold; opacity: 0.75; margin-bottom: 0px;">Confidence</p>
                    <p style="text-align: center; font-size: 45px; font-weight: bold; margin-top: -10px;">{max(probs):.2%}</p>
                </div>
            </div>
        </div>
        """.strip(),
        unsafe_allow_html=True
    )