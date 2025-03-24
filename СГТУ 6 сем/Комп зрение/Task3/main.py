import cv2
import numpy as np

# Загрузка изображения
img = cv2.imread('cat.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = np.float32(gray)

# Применение детектора Harris
dst = cv2.cornerHarris(gray, blockSize=2, ksize=3, k=0.04)
dst = cv2.dilate(dst, None)

# Пороговое значение для выделения углов
img[dst > 0.01 * dst.max()] = [0, 0, 255]

# Отображение результата
cv2.imshow('Harris Corners', img)



img = cv2.imread('cat.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Создание объекта SIFT
sift = cv2.SIFT_create(contrastThreshold=0.04, edgeThreshold=10)

# Обнаружение ключевых точек
kp, des = sift.detectAndCompute(gray, None)

# Визуализация
img_sift = cv2.drawKeypoints(img, kp, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
cv2.imshow('SIFT Keypoints', img_sift)



orb = cv2.ORB_create()
kp_orb, des_orb = orb.detectAndCompute(gray, None)
img_orb = cv2.drawKeypoints(img, kp_orb, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
cv2.imshow('ORB Keypoints', img_orb)



akaze = cv2.AKAZE_create()
kp_akaze, des_akaze = akaze.detectAndCompute(gray, None)
img_akaze = cv2.drawKeypoints(img, kp_akaze, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
cv2.imshow('AKAZE Keypoints', img_akaze)
cv2.waitKey(0)