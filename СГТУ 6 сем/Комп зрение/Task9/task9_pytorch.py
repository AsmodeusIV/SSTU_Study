import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from torchvision.datasets import MNIST
from torchvision.transforms import ToTensor
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import time
import os
from tqdm import tqdm

print(torch.cuda.is_available())
# Создаем папку для сохранения результатов
os.makedirs('reports_torch', exist_ok=True)

# Загрузка данных
train_data = MNIST(root='data', train=True, download=True, transform=ToTensor())
test_data = MNIST(root='data', train=False, download=True, transform=ToTensor())

train_loader = DataLoader(train_data, batch_size=32, shuffle=True)
test_loader = DataLoader(test_data, batch_size=32, shuffle=False)

# Устройство (CPU/GPU)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")


# Функция для обучения и оценки модели
def train_and_evaluate(model, train_loader, test_loader, optimizer, criterion, epochs=10):
    train_losses = []
    train_accs = []
    val_losses = []
    val_accs = []
    start_time = time.time()

    for epoch in range(epochs):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0

        for images, labels in tqdm(train_loader, desc=f'Epoch {epoch + 1}/{epochs}'):
            images, labels = images.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

        train_loss = running_loss / len(train_loader)
        train_acc = correct / total
        train_losses.append(train_loss)
        train_accs.append(train_acc)

        # Валидация
        model.eval()
        val_loss = 0.0
        correct = 0
        total = 0

        with torch.no_grad():
            for images, labels in test_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                loss = criterion(outputs, labels)

                val_loss += loss.item()
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()

        val_loss = val_loss / len(test_loader)
        val_acc = correct / total
        val_losses.append(val_loss)
        val_accs.append(val_acc)

        print(
            f'Epoch {epoch + 1}: Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.4f}, Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.4f}')

    train_time = time.time() - start_time
    return {
        'train_losses': train_losses,
        'train_accs': train_accs,
        'val_losses': val_losses,
        'val_accs': val_accs,
        'train_time': train_time,
        'final_val_acc': val_accs[-1],
        'final_val_loss': val_losses[-1]
    }


# Функция для сохранения графиков
def save_plots(history, filename):
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 2, 1)
    plt.plot(history['train_accs'], label='Train Accuracy')
    plt.plot(history['val_accs'], label='Validation Accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(history['train_losses'], label='Train Loss')
    plt.plot(history['val_losses'], label='Validation Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()

    plt.savefig(f'reports_torch/{filename}.png')
    plt.close()


# Задание 1: Изменение архитектуры сети
def task1_architecture():
    class CNN(nn.Module):
        def __init__(self, filters, kernel_sizes, dense_units):
            super(CNN, self).__init__()
            self.conv_layers = nn.ModuleList()
            in_channels = 1

            for out_channels, kernel_size in zip(filters, kernel_sizes):
                self.conv_layers.append(
                    nn.Sequential(
                        nn.Conv2d(in_channels, out_channels, kernel_size, padding='same'),
                        nn.ReLU(),
                        nn.MaxPool2d(2),
                        nn.Dropout(0.25)
                    )
                )
                in_channels = out_channels

            self.flatten = nn.Flatten()

            # Calculate the size after convolutions and pooling
            self.fc_input_size = self._get_fc_input_size()

            self.fc = nn.Sequential(
                nn.Linear(self.fc_input_size, dense_units),
                nn.ReLU(),
                nn.Dropout(0.5),
                nn.Linear(dense_units, 10)
            )

        def _get_fc_input_size(self):
            # Create a dummy input to calculate the size
            with torch.no_grad():
                dummy_input = torch.zeros(1, 1, 28, 28)
                for layer in self.conv_layers:
                    dummy_input = layer(dummy_input)
                return int(torch.prod(torch.tensor(dummy_input.size()[1:])))

        def forward(self, x):
            for layer in self.conv_layers:
                x = layer(x)
            x = self.flatten(x)
            x = self.fc(x)
            return x

    architectures = [
        {'name': 'Original (32,3x3,2 layers)', 'filters': [32, 64], 'kernel_sizes': [3, 3], 'dense_units': 128},
        {'name': '64 filters,5x5,3 layers', 'filters': [64, 64, 128], 'kernel_sizes': [5, 5, 3], 'dense_units': 256},
        {'name': '128 filters,3x3,2 layers', 'filters': [128, 128], 'kernel_sizes': [3, 3], 'dense_units': 512},
        {'name': '64 filters,7x7,2 layers', 'filters': [64, 64], 'kernel_sizes': [7, 7], 'dense_units': 64},
    ]

    results = []
    for arch in architectures:
        print(f"\nTraining architecture: {arch['name']}")
        model = CNN(arch['filters'], arch['kernel_sizes'], arch['dense_units']).to(device)
        optimizer = optim.Adam(model.parameters())
        criterion = nn.CrossEntropyLoss()

        history = train_and_evaluate(model, train_loader, test_loader, optimizer, criterion)
        num_params = sum(p.numel() for p in model.parameters())

        results.append({
            'Architecture': arch['name'],
            'Parameters': num_params,
            'Test Accuracy': history['final_val_acc'],
            'Test Loss': history['final_val_loss'],
            'Training Time (s)': history['train_time']
        })

        save_plots(history, f'task1_{arch["name"]}')

    df = pd.DataFrame(results)
    df.to_csv('reports_torch/task1_results.csv', index=False)
    print("Task 1 results saved to reports_torch/task1_results.csv")


# Задание 2: Эксперименты с функциями активации
def task2_activation():
    class CNN(nn.Module):
        def __init__(self, activation):
            super(CNN, self).__init__()
            self.activation = activation

            self.conv1 = nn.Conv2d(1, 32, 3, padding='same')
            self.conv2 = nn.Conv2d(32, 64, 3, padding='same')
            self.fc1 = nn.Linear(64 * 7 * 7, 128)
            self.fc2 = nn.Linear(128, 10)

            self.dropout1 = nn.Dropout(0.25)
            self.dropout2 = nn.Dropout(0.5)
            self.pool = nn.MaxPool2d(2)

            if activation == 'leaky_relu':
                self.act = nn.LeakyReLU(0.1)
            elif activation == 'elu':
                self.act = nn.ELU()
            else:
                self.act = {
                    'relu': nn.ReLU(),
                    'sigmoid': nn.Sigmoid(),
                    'tanh': nn.Tanh()
                }[activation]

        def forward(self, x):
            x = self.act(self.conv1(x))
            x = self.pool(x)
            x = self.dropout1(x)

            x = self.act(self.conv2(x))
            x = self.pool(x)
            x = self.dropout1(x)

            x = torch.flatten(x, 1)
            x = self.act(self.fc1(x))
            x = self.dropout2(x)
            x = self.fc2(x)
            return x

    activations = ['relu', 'sigmoid', 'tanh', 'elu', 'leaky_relu']
    results = []

    for activation in activations:
        print(f"\nTraining with activation: {activation}")
        model = CNN(activation).to(device)
        optimizer = optim.Adam(model.parameters())
        criterion = nn.CrossEntropyLoss()

        history = train_and_evaluate(model, train_loader, test_loader, optimizer, criterion)

        results.append({
            'Activation': activation,
            'Test Accuracy': history['final_val_acc'],
            'Test Loss': history['final_val_loss'],
            'Training Time (s)': history['train_time']
        })

        save_plots(history, f'task2_{activation}')

    df = pd.DataFrame(results)
    df.to_csv('reports_torch/task2_results.csv', index=False)
    print("Task 2 results saved to reports_torch/task2_results.csv")


# Задание 3: Эксперименты с оптимизаторами
def task3_optimizers():
    class CNN(nn.Module):
        def __init__(self):
            super(CNN, self).__init__()
            self.conv1 = nn.Conv2d(1, 32, 3, padding='same')
            self.conv2 = nn.Conv2d(32, 64, 3, padding='same')
            self.fc1 = nn.Linear(64 * 7 * 7, 128)
            self.fc2 = nn.Linear(128, 10)

            self.dropout1 = nn.Dropout(0.25)
            self.dropout2 = nn.Dropout(0.5)
            self.pool = nn.MaxPool2d(2)
            self.act = nn.ReLU()

        def forward(self, x):
            x = self.act(self.conv1(x))
            x = self.pool(x)
            x = self.dropout1(x)

            x = self.act(self.conv2(x))
            x = self.pool(x)
            x = self.dropout1(x)

            x = torch.flatten(x, 1)
            x = self.act(self.fc1(x))
            x = self.dropout2(x)
            x = self.fc2(x)
            return x

    optimizers = [
        {'name': 'Adam', 'optimizer': optim.Adam, 'lr': 0.001},
        {'name': 'SGD', 'optimizer': optim.SGD, 'lr': 0.01, 'momentum': 0.9},
        {'name': 'RMSprop', 'optimizer': optim.RMSprop, 'lr': 0.001},
        {'name': 'Adagrad', 'optimizer': optim.Adagrad, 'lr': 0.01},
        {'name': 'AdamW', 'optimizer': optim.AdamW, 'lr': 0.001},
    ]

    results = []
    for opt in optimizers:
        print(f"\nTraining with optimizer: {opt['name']}")
        model = CNN().to(device)
        optimizer = opt['optimizer'](model.parameters(), lr=opt['lr'],
                                     **({k: v for k, v in opt.items() if k not in ['name', 'optimizer', 'lr']}))
        criterion = nn.CrossEntropyLoss()

        history = train_and_evaluate(model, train_loader, test_loader, optimizer, criterion)

        results.append({
            'Optimizer': opt['name'],
            'Test Accuracy': history['final_val_acc'],
            'Test Loss': history['final_val_loss'],
            'Training Time (s)': history['train_time']
        })

        save_plots(history, f'task3_{opt["name"]}')

    df = pd.DataFrame(results)
    df.to_csv('reports_torch/task3_results.csv', index=False)
    print("Task 3 results saved to reports_torch/task3_results.csv")


# Запуск всех заданий
if __name__ == '__main__':
    print("Running Task 1: Architecture Experiments...")
    task1_architecture()

    print("\nRunning Task 2: Activation Functions...")
    task2_activation()

    print("\nRunning Task 3: Optimizers...")
    task3_optimizers()

    print("\nAll tasks completed! Results saved in the 'reports_torch' folder.")