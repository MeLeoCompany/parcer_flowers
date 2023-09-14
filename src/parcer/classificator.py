import io

import torch
import torchvision.models as models
import torchvision.transforms as transforms
import torch.nn as nn
import torch.nn.functional as F
from PIL import Image
from .consts import CLASSIFICATOR_MODEL_PASS

def varify_pics(image):
    # Загрузка модели
    model = models.resnet18()  # Здесь замените на ваш класс модели
    model.fc = nn.Linear(512, 2)
    model.load_state_dict(torch.load(CLASSIFICATOR_MODEL_PASS, map_location=torch.device('cpu')))
    model.eval()  # Переключение в режим оценки, если это необходимо
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    image_buffer = io.BytesIO(image)
    image = Image.open(image_buffer)
    image = image.convert('RGB') 
    input_image = transform(image).unsqueeze(0)

    with torch.no_grad():
        output = model(input_image)
    
    # Получение предсказания класса
    probabilities = F.softmax(output, dim=1)
    
    _, predicted = torch.max(probabilities, 1)
    
    # Опционально: интерпретация предсказания
    class_names = [True, False] 
    confirm = class_names[predicted.item()]
    return confirm
