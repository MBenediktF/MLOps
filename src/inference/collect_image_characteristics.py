import cv2
import numpy as np
from skimage.feature import graycomatrix, graycoprops


def collect_image_characteristics(image_file: bytes) -> dict:
    # Load and convert image
    nparr = np.frombuffer(image_file, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2Lab)
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 1: Color metrics
    # 1.1: Brightness
    brightness_mean = round(float(np.mean(gray_image)), 2)
    brightness_std = round(float(np.std(gray_image)), 2)

    # 1.2 Colors RGB
    mean, stddev = cv2.meanStdDev(image)
    color_mean = [round(float(val), 2) for val in mean.flatten()]
    color_std = [round(float(val), 2) for val in stddev.flatten()]

    # 1.3 Colors LAB and HSV
    lab_means = tuple(round(float(val), 2) for val in cv2.mean(lab_image))
    hsv_means = tuple(round(float(val), 2) for val in cv2.mean(hsv_image))

    # 2: Structure metrics
    # 2.1 Canny edge detection
    edges = cv2.Canny(gray_image, 100, 200)
    edge_count = int(np.sum(edges > 0))

    # 2.2 Texture features (GLCM)
    glcm = graycomatrix(gray_image, [5], [0], 256, symmetric=True, normed=True)
    contrast = round(float(graycoprops(glcm, 'contrast')[0, 0]), 2)
    dissimilarity = round(float(graycoprops(glcm, 'dissimilarity')[0, 0]), 2)
    homogeneity = round(float(graycoprops(glcm, 'homogeneity')[0, 0]), 2)
    ASM = round(float(graycoprops(glcm, 'ASM')[0, 0]), 2)
    energy = round(float(graycoprops(glcm, 'energy')[0, 0]), 2)
    correlation = round(float(graycoprops(glcm, 'correlation')[0, 0]), 2)

    # 2.3 Feature detection (ORB)
    orb = cv2.ORB_create()
    keypoints = orb.detect(gray_image, None)
    keypoint_count = int(len(keypoints))

    # 3: Return results as dictionary
    image_characteristics = {
        "brightness_mean": brightness_mean,
        "brightness_std": brightness_std,
        "red_mean": color_mean[0],
        "green_mean": color_mean[1],
        "blue_mean": color_mean[2],
        "red_std": color_std[0],
        "green_std": color_std[1],
        "blue_std": color_std[2],
        "lab_L": lab_means[0],
        "lab_A": lab_means[1],
        "lab_B": lab_means[2],
        "hsv_H": hsv_means[0],
        "hsv_S": hsv_means[1],
        "hsv_V": hsv_means[2],
        "hsv_means": hsv_means,
        "edge_count": edge_count,
        "contrast": contrast,
        "dissimilarity": dissimilarity,
        "homogeneity": homogeneity,
        "ASM": ASM,
        "energy": energy,
        "correlation": correlation,
        "keypoint_count": keypoint_count
    }
    return image_characteristics
