import cv2
import numpy as np
import matplotlib.pyplot as plt

def transform_image(img, scale=1.0, angle=0):
    h, w = img.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, scale)
    transformed = cv2.warpAffine(img, M, (w, h))
    return transformed

def harris_corners(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray, blockSize=2, ksize=3, k=0.04)
    dst = cv2.dilate(dst, None)
    img_copy = img.copy()
    img_copy[dst > 0.01 * dst.max()] = [0, 0, 255]
    return img_copy

def sift_keypoints(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    sift = cv2.SIFT_create(contrastThreshold=0.04, edgeThreshold=10)
    kp, des = sift.detectAndCompute(gray, None)
    return cv2.drawKeypoints(img, kp, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

def orb_keypoints(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    orb = cv2.ORB_create()
    kp, des = orb.detectAndCompute(gray, None)
    return cv2.drawKeypoints(img, kp, None)

def akaze_keypoints(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    akaze = cv2.AKAZE_create()
    kp, des = akaze.detectAndCompute(gray, None)
    return cv2.drawKeypoints(img, kp, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

def process_image(img_path, img_label):
    img_original = cv2.imread(img_path)
    transformations = [
        ('original', img_original),
        ('scale_0.5', transform_image(img_original, scale=0.5)),
        ('scale_2.0', transform_image(img_original, scale=2.0)),
        ('rotate_45', transform_image(img_original, angle=45)),
        ('rotate_90', transform_image(img_original, angle=90)),
    ]

    for suffix, transformed in transformations:
        fig, axs = plt.subplots(1, 4, figsize=(20, 5))
        fig.suptitle(f'{img_label} - {suffix}', fontsize=16)

        methods = [
            ('Harris', harris_corners),
            ('SIFT', sift_keypoints),
            ('ORB', orb_keypoints),
            ('AKAZE', akaze_keypoints),
        ]

        for ax, (name, method) in zip(axs, methods):
            result = method(transformed)
            result_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
            ax.imshow(result_rgb)
            ax.set_title(name)
            ax.axis('off')

        plt.tight_layout()
        plt.subplots_adjust(top=0.85)
        plt.savefig(f'{img_label}_{suffix}_features.jpg')  # Сохраняем коллаж
        plt.show()

# Обработка двух изображений
process_image('cat.jpg', 'cat')
process_image('mountains.jpg', 'mountains')
