# Базовый легкий образ Linux с Python
FROM python:3.10-slim

# Устанавливаем системные зависимости для работы OpenCV и графики YOLO
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /code

# Копируем файл зависимостей
COPY ./requirements.txt /code/requirements.txt

# Устанавливаем библиотеки
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Копируем код приложения
COPY ./app /code/app

# Открываем порт 8000
EXPOSE 8000

# Запускаем FastAPI через Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]