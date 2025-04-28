import cv2
import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report
import time

def load_data(train_path, test_path):
    train_data = pd.read_csv(train_path)
    y_train = train_data['label'].values
    X_train = train_data.drop('label', axis=1).values
    
    test_data = pd.read_csv(test_path)
    y_test = test_data['label'].values
    X_test = test_data.drop('label', axis=1).values
    
    return X_train, y_train, X_test, y_test

train_path = "C:\\Users\\admin\\Desktop\\data\\mnist_train.csv"
test_path = "C:\\Users\\admin\\Desktop\\data\\mnist_test.csv"
X_train, y_train, X_test, y_test = load_data(train_path, test_path)

def extract_sift_features(images):
    sift = cv2.SIFT_create()
    descriptors_list = []
    for img in images:
        img = img.reshape(28, 28).astype(np.uint8)
        _, descriptors = sift.detectAndCompute(img, None)
        if descriptors is not None:
            descriptors = np.mean(descriptors, axis=0)
        else:
            descriptors = np.zeros(128)
        descriptors_list.append(descriptors)
    return np.array(descriptors_list)

def extract_haar_features(images):
    haar_features = []
    for img in images:
        img = img.reshape(28, 28).astype(np.uint8)
        img = cv2.resize(img, (14, 14))
        img = cv2.equalizeHist(img)
        haar_features.append(img.flatten())
    return np.array(haar_features)

def evaluate_knn(X_train_feat, X_test_feat, y_train, y_test, method_name):
    start = time.time()
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(X_train_feat, y_train)
    y_pred = knn.predict(X_test_feat)
    acc = accuracy_score(y_test, y_pred)
    time_elapsed = time.time() - start
    
    print(f"\nМетод: {method_name}")
    print(f"Точность: {acc:.4f}")
    print(f"Время выполнения: {time_elapsed:.2f} сек")
    print(classification_report(y_test, y_pred))
    
    return acc, time_elapsed

print("=== Векторное представление ===")
acc_vector, time_vector = evaluate_knn(X_train, X_test, y_train, y_test, "Vector")

print("\n=== SIFT признаки ===")
sample_size = 2000 
X_train_sift = extract_sift_features(X_train[:sample_size])
X_test_sift = extract_sift_features(X_test[:sample_size//5])
acc_sift, time_sift = evaluate_knn(X_train_sift, X_test_sift, 
                                 y_train[:sample_size], y_test[:sample_size//5], "SIFT")

print("\n=== Хаара признаки ===")
X_train_haar = extract_haar_features(X_train)
X_test_haar = extract_haar_features(X_test)
acc_haar, time_haar = evaluate_knn(X_train_haar, X_test_haar, y_train, y_test, "Haar")

def compare_implementations(X_train, y_train, X_test, y_test):
    X_train_float = X_train.astype(np.float32)
    y_train_int = y_train.astype(int)
    X_test_float = X_test.astype(np.float32)
    
    start = time.time()
    knn_sk = KNeighborsClassifier(n_neighbors=5)
    knn_sk.fit(X_train, y_train)
    y_pred_sk = knn_sk.predict(X_test)
    sk_time = time.time() - start
    sk_acc = accuracy_score(y_test, y_pred_sk)
    
    start = time.time()
    knn_cv = cv2.ml.KNearest_create()
    knn_cv.train(X_train_float, cv2.ml.ROW_SAMPLE, y_train_int)
    retval, results, neighborResponses, dist = knn_cv.findNearest(X_test_float, k=5)
    y_pred_cv = results.ravel().astype(int)
    cv_time = time.time() - start
    cv_acc = accuracy_score(y_test, y_pred_cv)
    
    print("\n=== Сравнение реализаций ===")
    print(f"Sklearn - Точность: {sk_acc:.4f}, Время: {sk_time:.2f} сек")
    print(f"OpenCV - Точность: {cv_acc:.4f}, Время: {cv_time:.2f} сек")

compare_implementations(X_train, y_train, X_test, y_test)