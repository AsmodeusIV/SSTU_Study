import tensorflow as tf
from tensorflow.keras import layers, models
import pandas as pd
import numpy as np

# Загрузка данных
train_df = pd.read_csv("..\\..\\..\\data\\sign_mnist_train.csv")
test_df = pd.read_csv("..\\..\\..\\data\\sign_mnist_test.csv")

# Выбор 5 классов (A, B, C, D, E)
selected_labels = [0, 1, 2, 3, 4]
train_df = train_df[train_df['label'].isin(selected_labels)]
test_df = test_df[test_df['label'].isin(selected_labels)]

# Разделение на признаки и метки
y_train = train_df['label'].values
y_test = test_df['label'].values
X_train = train_df.drop('label', axis=1).values.reshape(-1, 28, 28, 1)
X_test = test_df.drop('label', axis=1).values.reshape(-1, 28, 28, 1)

# Нормализация
X_train = X_train / 255.0
X_test = X_test / 255.0

model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    layers.BatchNormalization(),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.BatchNormalization(),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.BatchNormalization(),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(5, activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

history = model.fit(X_train, y_train, epochs=10, validation_data=(X_test, y_test))

# TensorFlow
test_loss, test_acc = model.evaluate(X_test, y_test, verbose=2)
print(f"Test accuracy: {test_acc}")
