from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Проверяем, что эндпоинт /health доступен и возвращает 200"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_predict_empty_file():
    """Проверяем, что отправка пустого файла возвращает ошибку 400 Bad Request"""
    # Отправляем пустые байты вместо картинки
    files = {"file": ("empty.jpg", b"", "image/jpeg")}
    response = client.post("/predict", files=files)
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Empty file uploaded"