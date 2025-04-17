import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# Загрузка данных из mnist.csv
df = pd.read_csv("mnist_train.csv")
# Извлечение первой строки данных (первая цифра)
first_digit = df.iloc[0]
# Извлечение метки (текстового значения цифры)
label = first_digit[0]
# Извлечение пикселей изображения
pixels = first_digit[1:].values
# Преобразование пикселей в двумерный массив 28x28
image = pixels.reshape(28, 28)
# Отображение изображения с помощью matplotlib
plt.imshow(image, cmap='gray')
plt.title(f"Цифра: {label}")
plt.show()

# Разделение данных на признаки (X) и метки (y)
X = df.iloc[:, 1:].values
y = df.iloc[:, 0].values
# Преобразование признаков в формат, подходящий для OpenCV
X = X.astype(np.float32)
# Создание и обучение kNN классификатора
knn = cv2.ml_KNearest.create()
knn.train(X, cv2.ml.ROW_SAMPLE, y.astype(np.float32))
# Пример использования: классификация первого изображения из тестового набора
test_image = X[0].reshape(1, -1)
ret, result, neighbours, dist = knn.findNearest(test_image, k=5) # k=5 - 5 ближайших соседей
print(f"Предсказанная цифра: {result[0][0]}")
print(f"Реальная цифра: {y[0]}")


# Загрузка данных
df_train = pd.read_csv("mnist_train.csv")
df_test = pd.read_csv("mnist_test.csv")

# Разделение на признаки и метки
X_train = df_train.iloc[:, 1:].values.astype(np.float32)
y_train = df_train.iloc[:, 0].values
X_test = df_test.iloc[:, 1:].values.astype(np.float32)
y_test = df_test.iloc[:, 0].values

# Нормализация данных (деление на 255)
X_train_normalized = X_train / 255.0
X_test_normalized = X_test / 255.0

# Создание и обучение kNN классификатора (на нормализованных данных)
knn = cv2.ml.KNearest_create()
knn.train(X_train_normalized, cv2.ml.ROW_SAMPLE, y_train.astype(np.float32))

# Эксперимент 1: Точность для разных значений k
k_values = [1, 3, 5, 7, 10, 20]
accuracies = []

for k in k_values:
    ret, results, neighbours, dist = knn.findNearest(X_test_normalized, k=k)
    accuracy = np.sum(results.flatten() == y_test) / len(y_test)
    accuracies.append(accuracy * 100)
    print(f"Точность для k={k}: {accuracy * 100:.2f}%")

# Построение графика зависимости точности от k
plt.figure(figsize=(10, 5))
plt.plot(k_values, accuracies, marker='o')
plt.xlabel('k')
plt.ylabel('Точность (%)')
plt.title('Зависимость точности от количества соседей (k)')
plt.grid()
plt.show()

# Эксперимент 2: Сравнение точности на нормализованных и ненормализованных данных
knn_non_normalized = cv2.ml.KNearest_create()
knn_non_normalized.train(X_train, cv2.ml.ROW_SAMPLE, y_train.astype(np.float32))

ret, results_non_normalized, _, _ = knn_non_normalized.findNearest(X_test, k=3)
accuracy_non_normalized = np.sum(results_non_normalized.flatten() == y_test) / len(y_test) * 100

ret, results_normalized, _, _ = knn.findNearest(X_test_normalized, k=3)
accuracy_normalized = np.sum(results_normalized.flatten() == y_test) / len(y_test) * 100

print(f"\nСравнение точности:")
print(f"Без нормализации: {accuracy_non_normalized:.2f}%")
print(f"С нормализацией: {accuracy_normalized:.2f}%")

# Эксперимент 3: Визуализация ближайших соседей
test_index = 0  # Индекс тестового изображения (можно изменить)
k = 5  # Количество соседей

# Предсказание для выбранного тестового изображения
test_image = X_test_normalized[test_index].reshape(1, -1)
ret, result, neighbours_indices, dist = knn.findNearest(test_image, k=k)

# Визуализация тестового изображения и его соседей
plt.figure(figsize=(15, 3))
plt.suptitle(f"Тестовое изображение (класс: {y_test[test_index]}) и его {k} ближайших соседей", y=1.05)

# Тестовое изображение
plt.subplot(1, k + 1, 1)
plt.imshow(X_test[test_index].reshape(28, 28), cmap='gray')
plt.title(f"Тест: {y_test[test_index]}")
plt.axis('off')

# Ближайшие соседи из тренировочного набора
for i, neighbour_idx in enumerate(neighbours_indices.flatten()):
    plt.subplot(1, k + 1, i + 2)
    plt.imshow(X_train[neighbour_idx].reshape(28, 28), cmap='gray')
    plt.title(f"Сосед: {y_train[neighbour_idx]}")
    plt.axis('off')

plt.tight_layout()
plt.show()

# Анализ соседей
print("\nМетки ближайших соседей:", y_train[neighbours_indices.flatten().astype(int)])