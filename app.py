
import streamlit as st
from PIL import Image
import io
import torch
from utils.preprocess import preprocess_image
from utils.inference import load_checkpoint, make_prediction

import base64

st.title("Brain Tumor Detection")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
checkpoint_path =  "./models/efficientnet_b0_20241109_140235.pth"
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
    # st.image(image, caption="Uploaded Image")
    img_str = image_to_base64(image)
    st.markdown(
        f"""
        <div style="display: flex; flex-direction: column; align-items: center;">
            <div style="display: flex; flex-direction: column; align-items: center;">
                <img src="data:image/jpeg;base64,{img_str}" alt="Uploaded Image" style="width: 400px; height: 400px; border-radius: 10px;">
                <p style="text-align: center;">Uploaded Image</p>
            </div>
            <div style="display: flex; flex-direction: row; gap: 70px;">
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