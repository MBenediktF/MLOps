import numpy as np
from sklearn.utils import shuffle


def preprocess_data(images, labels, uids, test_split=0.2, seed=0):
    # Check input data
    if np.any(images < 0) or np.any(images > 255):
        raise ValueError("Input data must be between 0 and 255")

    # Normalize data
    images = images / 255.0

    # shuffle dataset
    images, labels, uids = shuffle(images, labels, uids, random_state=seed)

    # split dataset
    index = round(images.shape[0] * test_split)
    test_x, test_y, test_uids = images[0:index], labels[0:index], uids[0:index]
    train_x, train_y, train_uids = images[index:], labels[index:], uids[index:]

    return train_x, train_y, train_uids, test_x, test_y, test_uids
