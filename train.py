from ultralytics import YOLO

# Load YOLOv8 Nano pretrained model
model = YOLO("yolov8n.pt")

# Train on our pothole dataset
results = model.train(
    data="data/pothole_dataset/extracted/data.yaml",
    epochs=20,
    imgsz=416,
    batch=4,
    workers=0,
    device="cpu",
    project="outputs",
    name="pothole_model",
    patience=5
)

print("Training completed!")
