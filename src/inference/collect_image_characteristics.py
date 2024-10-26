import cv2
import numpy as np
from skimage.feature import graycomatrix, graycoprops
import json


def collect_image_characteristics(image_file: bytes) -> str:
    # Load and convert image
    nparr = np.frombuffer(image_file, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2Lab)
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 1: Color metrics
    # 1.1: Brightness
    brightness_mean = np.mean(gray_image)
    brightness_std = np.std(gray_image)

    # 1.2 Colors
    mean, stddev = cv2.meanStdDev(image)
    color_mean = mean.flatten().tolist()
    color_std = stddev.flatten().tolist()

    # 1.3 Mean color values
    lab_means = cv2.mean(lab_image)
    hsv_means = cv2.mean(hsv_image)

    # 2: Structure metrics
    # 2.1 Canny edge detection
    edges = cv2.Canny(gray_image, 100, 200)
    edge_count = np.sum(edges > 0)

    # 2.2 Texture features (GLCM)
    glcm = graycomatrix(gray_image, [5], [0], 256, symmetric=True, normed=True)
    texture_features = {
        "contrast": graycoprops(glcm, 'contrast')[0, 0],
        "dissimilarity": graycoprops(glcm, 'dissimilarity')[0, 0],
        "homogeneity": graycoprops(glcm, 'homogeneity')[0, 0],
        "ASM": graycoprops(glcm, 'ASM')[0, 0],
        "energy": graycoprops(glcm, 'energy')[0, 0],
        "correlation": graycoprops(glcm, 'correlation')[0, 0]
    }

    # 2.3 Feature detection (ORB)
    orb = cv2.ORB_create()
    keypoints = orb.detect(gray_image, None)
    keypoint_count = len(keypoints)

    # 3: Convert and return results
    image_characteristics = {
        "brightness_mean": float(brightness_mean),
        "brightness_std": float(brightness_std),
        "color_mean": color_mean,
        "color_std": color_std,
        "lab_means": tuple(float(val) for val in lab_means),
        "hsv_means": tuple(float(val) for val in hsv_means),
        "edge_count": int(edge_count),
        "texture_features": {k: float(v) for k, v in texture_features.items()},
        "keypoint_count": int(keypoint_count)
    }
    image_characteristics_serializable = {
        key: value.tolist() if isinstance(value, np.ndarray) else value
        for key, value in image_characteristics.items()
    }
    return json.dumps(image_characteristics_serializable)
