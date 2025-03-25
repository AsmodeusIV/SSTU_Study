import numpy as np
import cv2
from sklearn.cluster import DBSCAN 
"""
def mean_shift_segmentation(image, spatial_radius, color_radius, max_level):
    # Преобразование изображения в лабораторное цветовое пространство
    image_lab = cv2.cvtColor(image, cv2.COLOR_BGR2Lab)
    
    # Выполнение сегментации Mean Shift
    segmented_image = cv2.pyrMeanShiftFiltering(image_lab, spatial_radius, color_radius, maxLevel=max_level)
    
    # Преобразование обратно в BGR
    segmented_image = cv2.cvtColor(segmented_image, cv2.COLOR_Lab2BGR)
    
    # Находим уникальные цвета (центры кластеров)
    unique_colors = np.unique(segmented_image.reshape(-1, 3), axis=0)
    
    # Создаем изображение с синими кластерами
    colored_clusters = np.zeros_like(segmented_image)
    
    # Фиксированная палитра ярких цветов
    palette = [
        (255, 0, 0),    # Красный
        (0, 255, 0),    # Зеленый
        (0, 0, 255),    # Синий
        (255, 255, 0),  # Желтый
        (255, 0, 255),  # Пурпурный
        (0, 255, 255),  # Голубой
        (128, 0, 0),    # Темно-красный
        (0, 128, 0),    # Темно-зеленый
        (0, 0, 128),    # Темно-синий
        (128, 128, 0),  # Оливковый
        (128, 0, 128),  # Фиолетовый
        (0, 128, 128)   # Темно-голубой
    ]
    
    # Циклически используем цвета из палитры
    for i, color in enumerate(unique_colors):
        mask = cv2.inRange(segmented_image, color, color)
        colored_clusters[mask > 0] = palette[i % len(palette)]
    
    return colored_clusters
# Загрузка изображения
image=cv2. imread("test.jpg") # чтение изображения в переменную img
# Параметры Mean Shift
spatial_radius = 60
color_radius = 40
max_level = 2

# Сегментация
segmented_image = mean_shift_segmentation(image, spatial_radius, color_radius, max_level)
cv2.imshow('AKAZE Keypoints111', image)

cv2.imshow('AKAZE Keypoints', segmented_image)

# Загрузка изображения
image=cv2. imread("test2.jpg") # чтение изображения в переменную img
# Параметры Mean Shift
spatial_radius = 60
color_radius = 40
max_level = 5

# Сегментация
segmented_image = mean_shift_segmentation(image, spatial_radius, color_radius, max_level)

cv2.imshow('AKAZE Keypoints11', image)

cv2.imshow('AKAZE Keypoints1', segmented_image)

"""
import numpy as np
import cv2
from sklearn.cluster import DBSCAN 

image=cv2. imread("test2.jpg") # чтение изображения в переменную img

pixels = image.reshape(-1, 3) 
# Создание объекта 
dbscan = DBSCAN(eps=3, min_samples=10) 
# Производим кластеризацию пикселей 
labels = dbscan.fit_predict(pixels) 
# Преобразуем метки в изображение 
segmented_image = labels.reshape(image.shape[0], image.shape[1])


cv2.imshow('AKAZE Keypoints1', segmented_image)

cv2.waitKey(0)
