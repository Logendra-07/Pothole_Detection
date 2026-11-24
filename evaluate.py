from ultralytics import YOLO

model = YOLO("models/best.pt")

results = model.val(
    data="data/pothole_dataset/extracted/data.yaml",
    split="test",
    imgsz=416,
    device="cpu"
)

print("\nTest evaluation completed!")
print("Precision:", results.box.mp)
print("Recall:", results.box.mr)
print("mAP50:", results.box.map50)
print("mAP50-95:", results.box.map)
