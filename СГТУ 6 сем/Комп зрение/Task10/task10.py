import os
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from torchvision import transforms, models
from torch.optim.lr_scheduler import ReduceLROnPlateau
from torchvision.datasets import CIFAR100

print(torch.cuda.is_available())

# Настройки
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
os.makedirs('results', exist_ok=True)
os.makedirs('plots', exist_ok=True)

# Загрузка данных
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])

train_dataset = CIFAR100(root='./data', train=True, download=True, transform=transform)
test_dataset = CIFAR100(root='./data', train=False, download=True, transform=transform)

train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False)

# Аугментация данных
train_transform_aug = transforms.Compose([
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(15),
    transforms.RandomResizedCrop(32, scale=(0.9, 1.1)),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])

train_dataset_aug = CIFAR100(root='./data', train=True, download=True, transform=train_transform_aug)
train_loader_aug = DataLoader(train_dataset_aug, batch_size=64, shuffle=True)


# Функция для создания моделей
def create_model(model_type):
    if model_type == 'DenseNet121':
        model = models.densenet121(pretrained=False)
        model.classifier = nn.Linear(1024, 100)
    elif model_type == 'VGG16':
        model = models.vgg16(pretrained=False)
        model.classifier[6] = nn.Linear(4096, 100)
    elif model_type == 'ResNet50':
        model = models.resnet50(pretrained=False)
        model.fc = nn.Linear(2048, 100)

    return model.to(device)


# Функция обучения
def train_model(model, train_loader, test_loader, name, epochs=20):
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    scheduler = ReduceLROnPlateau(optimizer, mode='min', factor=0.2, patience=3, min_lr=1e-6)

    history = {'train_loss': [], 'train_acc': [], 'val_loss': [], 'val_acc': []}
    best_loss = float('inf')
    best_model = None

    start_time = time.time()

    for epoch in range(epochs):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0

        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()

        train_loss = running_loss / len(train_loader)
        train_acc = 100. * correct / total

        # Валидация
        val_loss, val_acc = evaluate_model(model, test_loader, criterion)

        # Сохранение истории
        history['train_loss'].append(train_loss)
        history['train_acc'].append(train_acc)
        history['val_loss'].append(val_loss)
        history['val_acc'].append(val_acc)

        # Early stopping
        if val_loss < best_loss:
            best_loss = val_loss
            best_model = model.state_dict()
            torch.save(best_model, f'results/{name}_best_model.pth')
        torch.save(best_model, f'results/{name}_{epoch}_best_model.pth')

        scheduler.step(val_loss)

        print(
            f'Epoch {epoch + 1}/{epochs} - Train Loss: {train_loss:.4f}, Acc: {train_acc:.2f}% | Val Loss: {val_loss:.4f}, Acc: {val_acc:.2f}%')

    training_time = time.time() - start_time

    # Загрузка лучшей модели
    model.load_state_dict(torch.load(f'results/{name}_best_model.pth'))

    return model, history, training_time


# Функция оценки
def evaluate_model(model, loader, criterion):
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0

    with torch.no_grad():
        for inputs, labels in loader:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            loss = criterion(outputs, labels)

            running_loss += loss.item()
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()

    loss = running_loss / len(loader)
    acc = 100. * correct / total

    return loss, acc


# Обучение моделей
models_dict = {
   # 'DenseNet121': create_model('DenseNet121'),
   # 'VGG16': create_model('VGG16'),
    'ResNet50': create_model('ResNet50')
}

history_dict = {}
metrics_dict = {}
training_times = {}

for name, model in models_dict.items():
    print(f"\nTraining {name}...")
    trained_model, history, training_time = train_model(model, train_loader_aug, test_loader, name)
    training_times[name] = training_time

    # Оценка модели
    y_true = []
    y_pred = []
    y_probs = []

    with torch.no_grad():
        for inputs, labels in test_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = trained_model(inputs)
            _, predicted = outputs.max(1)

            y_true.extend(labels.cpu().numpy())
            y_pred.extend(predicted.cpu().numpy())
            y_probs.extend(torch.softmax(outputs, dim=1).cpu().numpy())

    # Сохранение метрик
    report = classification_report(y_true, y_pred, output_dict=True, zero_division=0)
    metrics_dict[name] = {
        'Accuracy': report['accuracy'],
        'Precision_macro': report['macro avg']['precision'],
        'Recall_macro': report['macro avg']['recall'],
        'F1_macro': report['macro avg']['f1-score'],
        'Training_time': training_time,
        'Params': sum(p.numel() for p in model.parameters())
    }

    # ROC AUC
    try:
        roc_auc = roc_auc_score(pd.get_dummies(y_true), y_probs, multi_class='ovr')
        metrics_dict[name]['ROC_AUC'] = roc_auc
    except Exception as e:
        print(f"ROC AUC calculation failed for {name}: {str(e)}")
        metrics_dict[name]['ROC_AUC'] = None

    # Сохранение истории обучения
    history_dict[name] = history

    # Визуализация матрицы ошибок
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=False, fmt='d', cmap='Blues')
    plt.title(f'Confusion Matrix - {name}')
    plt.savefig(f'plots/confusion_matrix_{name}.png', bbox_inches='tight')
    plt.close()

# Сохранение метрик в Excel
metrics_df = pd.DataFrame.from_dict(metrics_dict, orient='index')
metrics_df.to_excel('results/model_metrics.xlsx')

# Визуализация истории обучения
plt.figure(figsize=(12, 6))
for name in models_dict.keys():
    plt.plot(history_dict[name]['val_acc'], label=f'{name} Val')
plt.title('Validation Accuracy Comparison')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.savefig('plots/val_accuracy_comparison.png', bbox_inches='tight')
plt.close()

plt.figure(figsize=(12, 6))
for name in models_dict.keys():
    plt.plot(history_dict[name]['val_loss'], label=f'{name} Val')
plt.title('Validation Loss Comparison')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.savefig('plots/val_loss_comparison.png', bbox_inches='tight')
plt.close()

# Сравнение времени обучения
plt.figure(figsize=(8, 5))
plt.bar(training_times.keys(), training_times.values())
plt.title('Training Time Comparison')
plt.ylabel('Time (seconds)')
plt.savefig('plots/training_time_comparison.png', bbox_inches='tight')
plt.close()

# Сравнение параметров
params = {name: sum(p.numel() for p in model.parameters()) for name, model in models_dict.items()}
plt.figure(figsize=(8, 5))
plt.bar(params.keys(), params.values())
plt.title('Number of Parameters Comparison')
plt.ylabel('Parameters')
plt.savefig('plots/parameters_comparison.png', bbox_inches='tight')
plt.close()

print("\nAll results saved in 'results/' and 'plots/' directories!")