from fastapi import FastAPI, UploadFile, File, HTTPException, status
from ultralytics import YOLO
import io
from PIL import Image

app = FastAPI(title="Bellissimo Pizza Quality Control API")

# Загружаем маленькую модель (она скачается автоматически при первом запуске)
# В проде веса будут лежать локально или подтягиваться из MLflow
model = YOLO("yolov8n.pt") 

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/predict")
async def predict_pizza(file: UploadFile = File(...)):
    # Проверяем, что файл не пустой
    contents = await file.read()
    if len(contents) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Empty file uploaded"
        )
    
    try:
        # Читаем картинку из байт
        image = Image.open(io.BytesIO(contents))
        
        # Запускаем инференс (на Маке будет использоваться CPU/MPS, в докере - CPU)
        results = model(image)
        
        # Собираем результаты детекции
        detections = []
        for box in results[0].boxes:
            detections.append({
                "class": model.names[int(box.cls[0])],
                "confidence": float(box.conf[0]),
                "bbox": [float(x) for x in box.xyxy[0]]
            })
            
        return {"detections": detections}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Error processing image: {str(e)}"
        )