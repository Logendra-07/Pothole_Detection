from pathlib import Path
from ultralytics import YOLO
from PIL import Image
import numpy as np
import streamlit as st

MODEL_PATH = Path(__file__).resolve().parent / "models" / "best.pt"

@st.cache_resource(show_spinner="Loading YOLOv8 pothole detection model...")
def get_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
    return YOLO(str(MODEL_PATH))

def detect_potholes(image, confidence=0.25):

    model = get_model()
    image_array = np.array(image.convert("RGB"))

    results = model.predict(
        source=image_array,
        conf=confidence,
        imgsz=416,
        device="cpu",
        verbose=False
    )

    result = results[0]

    detected_image = result.plot()
    detected_image = Image.fromarray(detected_image[:, :, ::-1])

    detections = []

    for box in result.boxes:
        detections.append({
            "class": model.names[int(box.cls[0])],
            "confidence": round(float(box.conf[0]) * 100, 2)
        })

    return detected_image, detections
