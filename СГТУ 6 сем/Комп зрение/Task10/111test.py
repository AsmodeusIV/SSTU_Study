import os
import pandas as pd
from PIL import Image
from torch.utils.data import Dataset, DataLoader
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import transforms, models
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score, precision_score, recall_score, f1_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import time
import psutil
from tqdm import tqdm


# Определение класса датасета
class AnimalDataset(Dataset):
    def __init__(self, dataframe, transform=None):
        self.dataframe = dataframe
        self.transform = transform
        self.classes = sorted(dataframe['label'].unique())
        self.class_to_idx = {cls: idx for idx, cls in enumerate(self.classes)}

    def __len__(self):
        return len(self.dataframe)

    def __getitem__(self, idx):
        img_path = self.dataframe.iloc[idx]['filepath']
        label = self.dataframe.iloc[idx]['label']

        try:
            image = Image.open(img_path).convert('RGB')
        except Exception as e:
            print(f"Error loading image {img_path}: {e}")
            image = Image.new('RGB', (224, 224), color='black')
            label = 'cane'  # default label

        if self.transform:
            image = self.transform(image)

        label_idx = self.class_to_idx[label]
        return image, label_idx


# Загрузка и подготовка данных
def load_data():
    path = "C:/Users/Admin/Downloads/raw-img/"
    labels = os.listdir(path)
    print("Labels:", labels)

    data = []
    for label in labels:
        folder_path = os.path.join(path, label)
        if os.path.isdir(folder_path):
            for img_file in os.listdir(folder_path):
                if img_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    img_path = os.path.join(folder_path, img_file)
                    data.append((img_path, label))

    df = pd.DataFrame(data, columns=['filepath', 'label'])
    print("Dataframe head:\n", df.head())

    train_df, test_df = train_test_split(df, test_size=0.2, stratify=df['label'], random_state=42)
    print("Train size:", len(train_df))
    print("Test size:", len(test_df))

    train_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(10),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    test_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    train_dataset = AnimalDataset(train_df, transform=train_transform)
    test_dataset = AnimalDataset(test_df, transform=test_transform)

    return train_dataset, test_dataset


# Инициализация модели
def initialize_model(num_classes, device):
    model = models.densenet121(pretrained=True)
    num_ftrs = model.classifier.in_features
    model.classifier = nn.Linear(num_ftrs, num_classes)
    model = model.to(device)
    return model


# Обучение модели
def train_model(model, train_loader, test_loader, criterion, optimizer, num_epochs, device, scheduler=None):
    train_loss_history = []
    train_acc_history = []
    test_loss_history = []
    test_acc_history = []
    memory_usage = []
    time_per_epoch = []

    best_acc = 0.0
    best_model_wts = None

    for epoch in range(num_epochs):
        print(f'Epoch {epoch + 1}/{num_epochs}')
        print('-' * 10)

        start_time = time.time()

        # Тренировочная фаза
        model.train()
        running_loss = 0.0
        running_corrects = 0

        for inputs, labels in tqdm(train_loader, desc=f"Epoch {epoch + 1}"):
            inputs = inputs.to(device)
            labels = labels.to(device)

            optimizer.zero_grad()

            with torch.set_grad_enabled(True):
                outputs = model(inputs)
                _, preds = torch.max(outputs, 1)
                loss = criterion(outputs, labels)

                loss.backward()
                optimizer.step()

            running_loss += loss.item() * inputs.size(0)
            running_corrects += torch.sum(preds == labels.data)

        if scheduler:
            scheduler.step()

        epoch_loss = running_loss / len(train_loader.dataset)
        epoch_acc = running_corrects.double() / len(train_loader.dataset)

        train_loss_history.append(epoch_loss)
        train_acc_history.append(epoch_acc.cpu().numpy())

        # Тестовая фаза
        test_loss, test_acc, _ = evaluate_model(model, test_loader, criterion, device)
        test_loss_history.append(test_loss)
        test_acc_history.append(test_acc)

        # Проверка на лучшую модель
        if test_acc > best_acc:
            best_acc = test_acc
            best_model_wts = model.state_dict()

        # Замер памяти и времени
        memory_usage.append(psutil.Process().memory_info().rss / (1024 ** 2))  # в MB
        epoch_time = time.time() - start_time
        time_per_epoch.append(epoch_time)

        print(f'Train Loss: {epoch_loss:.4f} Acc: {epoch_acc:.4f}')
        print(f'Test Loss: {test_loss:.4f} Acc: {test_acc:.4f}')
        print(f'Time: {epoch_time:.2f}s')
        print(f'Memory: {memory_usage[-1]:.2f}MB')

    # Загрузка лучших весов модели
    model.load_state_dict(best_model_wts)

    return {
        'model': model,
        'train_loss_history': train_loss_history,
        'train_acc_history': train_acc_history,
        'test_loss_history': test_loss_history,
        'test_acc_history': test_acc_history,
        'memory_usage': memory_usage,
        'time_per_epoch': time_per_epoch
    }


# Оценка модели
def evaluate_model(model, dataloader, criterion, device):
    model.eval()
    running_loss = 0.0
    running_corrects = 0
    all_preds = []
    all_labels = []
    all_probs = []

    for inputs, labels in dataloader:
        inputs = inputs.to(device)
        labels = labels.to(device)

        with torch.set_grad_enabled(False):
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)
            loss = criterion(outputs, labels)
            probs = torch.softmax(outputs, dim=1)

        running_loss += loss.item() * inputs.size(0)
        running_corrects += torch.sum(preds == labels.data)
        all_preds.extend(preds.cpu().numpy())
        all_labels.extend(labels.cpu().numpy())
        all_probs.extend(probs.cpu().numpy())

    loss = running_loss / len(dataloader.dataset)
    acc = running_corrects.double() / len(dataloader.dataset)

    return loss, acc.cpu().numpy(), (all_labels, all_preds, all_probs)


# Расчет метрик
def calculate_metrics(true_labels, pred_labels, pred_probs, class_names):
    # Для многоклассовой классификации нам нужно использовать one-vs-rest подход для AUC
    try:
        auc = roc_auc_score(true_labels, pred_probs, multi_class='ovr')
    except:
        auc = float('nan')

    precision = precision_score(true_labels, pred_labels, average='weighted')
    recall = recall_score(true_labels, pred_labels, average='weighted')
    f1 = f1_score(true_labels, pred_labels, average='weighted')
    acc = accuracy_score(true_labels, pred_labels)

    cm = confusion_matrix(true_labels, pred_labels)

    metrics = {
        'accuracy': acc,
        'auc': auc,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'confusion_matrix': cm
    }

    return metrics


# Визуализация результатов
def plot_results(results, class_names, save_dir='results'):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Потери
    plt.figure(figsize=(10, 5))
    plt.plot(results['train_loss_history'], label='Train Loss')
    plt.plot(results['test_loss_history'], label='Test Loss')
    plt.title('Training and Validation Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.savefig(os.path.join(save_dir, 'loss_curve.png'))
    plt.close()

    # Точность
    plt.figure(figsize=(10, 5))
    plt.plot(results['train_acc_history'], label='Train Accuracy')
    plt.plot(results['test_acc_history'], label='Test Accuracy')
    plt.title('Training and Validation Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.savefig(os.path.join(save_dir, 'accuracy_curve.png'))
    plt.close()

    # Память и время
    plt.figure(figsize=(10, 5))
    plt.plot(results['memory_usage'], label='Memory Usage (MB)')
    plt.title('Memory Usage During Training')
    plt.xlabel('Epoch')
    plt.ylabel('Memory (MB)')
    plt.legend()
    plt.savefig(os.path.join(save_dir, 'memory_usage.png'))
    plt.close()

    plt.figure(figsize=(10, 5))
    plt.plot(results['time_per_epoch'], label='Time per epoch (s)')
    plt.title('Training Time per Epoch')
    plt.xlabel('Epoch')
    plt.ylabel('Time (s)')
    plt.legend()
    plt.savefig(os.path.join(save_dir, 'training_time.png'))
    plt.close()

    # Матрица ошибок
    metrics = results['metrics']
    cm = metrics['confusion_matrix']
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=class_names,
                yticklabels=class_names)
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.savefig(os.path.join(save_dir, 'confusion_matrix.png'))
    plt.close()


# Сохранение метрик в таблицу
def save_metrics_to_table(metrics, save_path='results/metrics_table.csv'):
    metrics_df = pd.DataFrame({
        'Metric': ['Accuracy', 'AUC', 'Precision', 'Recall', 'F1-score'],
        'Value': [metrics['accuracy'], metrics['auc'],
                  metrics['precision'], metrics['recall'],
                  metrics['f1_score']]
    })
    metrics_df.to_csv(save_path, index=False)


# Основная функция
def main():
    # Проверка доступности GPU
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # Параметры
    batch_size = 32
    num_epochs = 10
    learning_rate = 0.005
    num_classes = 10

    # Загрузка данных
    train_dataset, test_dataset = load_data()
    class_names = train_dataset.classes

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=4)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=4)

    # Инициализация модели
    model = initialize_model(num_classes, device)

    # Критерий и оптимизатор
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.1)

    # Обучение модели
    results = train_model(
        model, train_loader, test_loader, criterion,
        optimizer, num_epochs, device, scheduler
    )

    # Оценка модели
    _, _, (true_labels, pred_labels, pred_probs) = evaluate_model(
        model, test_loader, criterion, device
    )

    # Расчет метрик
    metrics = calculate_metrics(true_labels, pred_labels, np.array(pred_probs), class_names)
    results['metrics'] = metrics

    # Вывод метрик
    print("\nFinal Metrics:")
    print(f"Accuracy: {metrics['accuracy']:.4f}")
    print(f"AUC: {metrics['auc']:.4f}")
    print(f"Precision: {metrics['precision']:.4f}")
    print(f"Recall: {metrics['recall']:.4f}")
    print(f"F1-score: {metrics['f1_score']:.4f}")

    # Визуализация и сохранение результатов
    plot_results(results, class_names)
    save_metrics_to_table(metrics)

    # Сохранение модели
    torch.save(model.state_dict(), 'results/densenet121_finetuned.pth')


if __name__ == '__main__':
    main()