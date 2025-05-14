import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from tensorflow.keras.datasets import mnist
from tensorflow import keras
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, Dropout, LeakyReLU, ELU
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.regularizers import l2
from tensorflow.keras.optimizers import SGD, RMSprop, Adagrad, AdamW
import time
import os

import tensorflow as tf
print(tf.config.list_physical_devices('GPU'))

# Создаем папку для сохранения результатов
os.makedirs('reports', exist_ok=True)

# Загрузка данных
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train = x_train / 255.0
x_test = x_test / 255.0
x_train = np.expand_dims(x_train, axis=-1)
x_test = np.expand_dims(x_test, axis=-1)
y_train_cat = keras.utils.to_categorical(y_train, 10)
y_test_cat = keras.utils.to_categorical(y_test, 10)

# Callback для Early Stopping
early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)


# Функция для обучения и оценки модели
def train_and_evaluate(model, x_train, y_train, x_test, y_test, epochs=10, batch_size=64):
    start_time = time.time()
    history = model.fit(
        x_train, y_train,
        batch_size=batch_size,
        epochs=epochs,
        validation_split=0.2,
        callbacks=[early_stopping],
        verbose=0
    )
    train_time = time.time() - start_time
    test_loss, test_acc = model.evaluate(x_test, y_test, verbose=0)
    return history, test_acc, test_loss, train_time


# Функция для сохранения графиков
def save_plots(history, filename):
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], label='Train Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='Train Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()

    plt.savefig(f'reports/{filename}.png')
    plt.close()


# Задание 1: Изменение архитектуры сети
def task1_architecture():
    architectures = [
        {'name': 'Original (32,3x3,2 layers)', 'filters': [32, 64], 'kernel_sizes': [(3, 3), (3, 3)],
         'dense_units': 128},
        {'name': '64 filters,5x5,3 layers', 'filters': [64, 64, 128], 'kernel_sizes': [(5, 5), (5, 5), (3, 3)],
         'dense_units': 256},
        {'name': '128 filters,3x3,2 layers', 'filters': [128, 128], 'kernel_sizes': [(3, 3), (3, 3)],
         'dense_units': 512},
        {'name': '64 filters,7x7,2 layers', 'filters': [64, 64], 'kernel_sizes': [(7, 7), (7, 7)], 'dense_units': 64},
    ]

    results = []
    for arch in architectures:
        model = keras.Sequential()
        for i, (filters, kernel_size) in enumerate(zip(arch['filters'], arch['kernel_sizes'])):
            if i == 0:
                model.add(Conv2D(filters, kernel_size, padding='same', activation='relu', input_shape=(28, 28, 1)))
            else:
                model.add(Conv2D(filters, kernel_size, padding='same', activation='relu'))
            model.add(MaxPooling2D((2, 2)))
            model.add(Dropout(0.25))

        model.add(Flatten())
        model.add(Dense(arch['dense_units'], activation='relu', kernel_regularizer=l2(0.01)))
        model.add(Dropout(0.5))
        model.add(Dense(10, activation='softmax'))

        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

        history, test_acc, test_loss, train_time = train_and_evaluate(model, x_train, y_train_cat, x_test, y_test_cat)
        num_params = model.count_params()
        results.append({
            'Architecture': arch['name'],
            'Parameters': num_params,
            'Test Accuracy': test_acc,
            'Test Loss': test_loss,
            'Training Time (s)': train_time
        })

        save_plots(history, f'task1_{arch["name"]}')

    df = pd.DataFrame(results)
    df.to_csv('reports/task1_results.csv', index=False)
    print("Task 1 results saved to reports/task1_results.csv")


# Задание 2: Эксперименты с функциями активации
def task2_activation():
    activations = ['relu', 'sigmoid', 'tanh', 'elu', 'leaky_relu']

    results = []
    for activation in activations:
        model = keras.Sequential([
            Conv2D(32, (3, 3), padding='same', activation=activation, input_shape=(28, 28, 1)),
            MaxPooling2D((2, 2)),
            Dropout(0.25),
            Conv2D(64, (3, 3), padding='same', activation=activation),
            MaxPooling2D((2, 2)),
            Dropout(0.25),
            Flatten(),
            Dense(128, activation=activation, kernel_regularizer=l2(0.01)),
            Dropout(0.5),
            Dense(10, activation='softmax')
        ])

        if activation == 'leaky_relu':
            model = keras.Sequential([
                Conv2D(32, (3, 3), padding='same', input_shape=(28, 28, 1)),
                LeakyReLU(alpha=0.1),
                MaxPooling2D((2, 2)),
                Dropout(0.25),
                Conv2D(64, (3, 3), padding='same'),
                LeakyReLU(alpha=0.1),
                MaxPooling2D((2, 2)),
                Dropout(0.25),
                Flatten(),
                Dense(128, kernel_regularizer=l2(0.01)),
                LeakyReLU(alpha=0.1),
                Dropout(0.5),
                Dense(10, activation='softmax')
            ])

        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

        history, test_acc, test_loss, train_time = train_and_evaluate(model, x_train, y_train_cat, x_test, y_test_cat)
        results.append({
            'Activation': activation,
            'Test Accuracy': test_acc,
            'Test Loss': test_loss,
            'Training Time (s)': train_time
        })

        save_plots(history, f'task2_{activation}')

    df = pd.DataFrame(results)
    df.to_csv('reports/task2_results.csv', index=False)
    print("Task 2 results saved to reports/task2_results.csv")


# Задание 3: Эксперименты с оптимизаторами
def task3_optimizers():
    optimizers = [
        {'name': 'Adam', 'optimizer': keras.optimizers.Adam(learning_rate=0.001)},
        {'name': 'SGD', 'optimizer': SGD(learning_rate=0.01, momentum=0.9)},
        {'name': 'RMSprop', 'optimizer': RMSprop(learning_rate=0.001)},
        {'name': 'Adagrad', 'optimizer': Adagrad(learning_rate=0.01)},
        {'name': 'AdamW', 'optimizer': AdamW(learning_rate=0.001)},
    ]

    results = []
    for opt in optimizers:
        model = keras.Sequential([
            Conv2D(32, (3, 3), padding='same', activation='relu', input_shape=(28, 28, 1)),
            MaxPooling2D((2, 2)),
            Dropout(0.25),
            Conv2D(64, (3, 3), padding='same', activation='relu'),
            MaxPooling2D((2, 2)),
            Dropout(0.25),
            Flatten(),
            Dense(128, activation='relu', kernel_regularizer=l2(0.01)),
            Dropout(0.5),
            Dense(10, activation='softmax')
        ])

        model.compile(optimizer=opt['optimizer'], loss='categorical_crossentropy', metrics=['accuracy'])

        history, test_acc, test_loss, train_time = train_and_evaluate(model, x_train, y_train_cat, x_test, y_test_cat)
        results.append({
            'Optimizer': opt['name'],
            'Test Accuracy': test_acc,
            'Test Loss': test_loss,
            'Training Time (s)': train_time
        })

        save_plots(history, f'task3_{opt["name"]}')

    df = pd.DataFrame(results)
    df.to_csv('reports/task3_results.csv', index=False)
    print("Task 3 results saved to reports/task3_results.csv")


# Запуск всех заданий
if __name__ == '__main__':
    print("Running Task 1: Architecture Experiments...")
    task1_architecture()

    print("\nRunning Task 2: Activation Functions...")
    task2_activation()

    print("\nRunning Task 3: Optimizers...")
    task3_optimizers()

    print("\nAll tasks completed! Results saved in the 'reports' folder.")