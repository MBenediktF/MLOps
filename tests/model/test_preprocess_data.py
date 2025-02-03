import pytest
import numpy as np
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))  # noqa: E501
from src.model.preprocess_data import preprocess_data  # noqa: E402


@pytest.mark.parametrize("test_split", [0.1, 0.2])
def test_preprocess_data(test_split):
    # Create random data (100 images, 75x100 pixels, 3 channels)
    images = np.random.randint(0, 256, (100, 100, 75, 3), dtype=np.uint8)
    labels = np.random.randint(0, 350, 100)
    uids = np.arange(100)

    # Run preprocess_data
    train_x, train_y, train_uids, test_x, test_y, test_uids = \
        preprocess_data(images, labels, uids, test_split=test_split)

    # Validate results
    assert train_x.shape[0] > test_x.shape[0], \
        "Test data smaller than training data"
    assert train_y.shape[0] == train_x.shape[0], \
        "Train data and labels must have the same length"
    assert test_y.shape[0] == test_x.shape[0], \
        "Test data and labels must have the same length"
    assert train_x.shape[1:] == (100, 75, 3), \
        "Images must have the correct shape"
    assert test_x.shape[1:] == (100, 75, 3), \
        "Images must have the correct shape"
    assert np.all(train_y <= 1) and np.all(train_y >= 0), \
        "Labels must be normalized"
    assert np.all(test_y <= 1) and np.all(test_y >= 0), \
        "Labels must be normalized"
    assert np.all(train_x <= 1) and np.all(train_x >= 0), \
        "Images must be normalized"
    assert np.all(test_x <= 1) and np.all(test_x >= 0), \
        "Images must be normalized"
    assert set(train_uids).isdisjoint(set(test_uids)), \
        "Train and test uids must be unique"


def test_preprocess_data_invalid_input():
    # Create invalid images and labels
    images_invalid = np.array([[[[300, -10, 500]]]], dtype=np.int32)
    labels_invalid = np.array([10])

    with pytest.raises(
            ValueError, match="Input data must be between 0 and 255"):
        preprocess_data(images_invalid, labels_invalid, None)
