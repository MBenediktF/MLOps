import numpy as np
from sklearn.utils import shuffle

max_input_value = 350


def preprocess_data(images, labels, uids, test_split=0.2, seed=0):
    # Check input data
    if np.any(images < 0) or np.any(images > 255):
        raise ValueError("Input data must be between 0 and 255")

    if uids is None:
        uids = np.arange(images.shape[0])

    # Normalize features
    images = images / 255.0

    # Normalize labels
    labels = np.clip(labels, 0, max_input_value)
    labels = np.round(labels / float(max_input_value), 2)

    # shuffle dataset
    images, labels, uids = shuffle(images, labels, uids, random_state=seed)

    # split dataset
    index = round(images.shape[0] * test_split)
    test_x, test_y, test_uids = images[0:index], labels[0:index], uids[0:index]
    train_x, train_y, train_uids = images[index:], labels[index:], uids[index:]

    return train_x, train_y, train_uids, test_x, test_y, test_uids
