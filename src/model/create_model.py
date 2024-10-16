import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Dropout, Conv2D, Flatten
from tensorflow.keras.layers import Input, MaxPooling2D, AveragePooling2D
from tensorflow.keras.initializers import TruncatedNormal
from tensorflow.keras import backend as K


def create_model(img_size, dropout=0.2):
    K.backend()
    K.clear_session()
    seed = TruncatedNormal(stddev=0.1)
    img_width, img_height = img_size[2], img_size[1]

    # Input layer
    input = Input(shape=(img_height, img_width, 3))

    # Convolutional layers
    x = Conv2D(8, name="conv_1_1", kernel_size=3,
               activation='relu', strides=2, padding='same')(input)
    x = Conv2D(16, name="conv_1_2", kernel_size=3,
               activation='relu', strides=2, padding='same')(x)
    x = Conv2D(32, name="conv_1_3", kernel_size=3,
               activation='relu', strides=1, padding='same')(x)
    x = MaxPooling2D((3, 3), strides=1, padding='same')(x)
    x = inceptionModule(x, 8, 16, 8, 16, 8, 8, "1")
    x = Conv2D(32, name="conv_2_1", kernel_size=3,
               activation='relu', strides=2, padding='same')(x)
    x = Conv2D(64, name="conv_2_2", kernel_size=3,
               activation='relu', strides=2, padding='same')(x)
    x = Conv2D(128, name="conv_2_3", kernel_size=3,
               activation='relu', strides=1, padding='same')(x)
    x = MaxPooling2D((3, 3), strides=1, padding='same')(x)
    x = inceptionModule(x, 32, 64, 32, 64, 32, 32, "2")
    x = Conv2D(128, name="conv_3_1", kernel_size=3,
               activation='relu', strides=2, padding='same')(x)
    x = Conv2D(256, name="conv_3_2", kernel_size=3,
               activation='relu', strides=2, padding='same')(x)
    x = Conv2D(512, name="conv_3_3", kernel_size=3,
               activation='relu', strides=1, padding='same')(x)
    x = AveragePooling2D((3, 3), strides=2, padding='same')(x)
    x = Flatten()(x)

    # Fully connected dense layers
    x = Dense(256, name="dense_position_1", activation='relu',
              kernel_initializer=seed, bias_initializer=seed)(x)
    x = Dropout(dropout)(x)
    x = Dense(128, name="dense_position_2", activation='relu',
              kernel_initializer=seed, bias_initializer=seed)(x)
    x = Dropout(dropout)(x)
    x = Dense(64, name="dense_position_3", activation='relu',
              kernel_initializer=seed, bias_initializer=seed)(x)
    x = Dropout(dropout)(x)
    x = Dense(32, name="dense_position_4", activation='relu',
              kernel_initializer=seed, bias_initializer=seed)(x)
    x = Dropout(dropout)(x)
    output = Dense(1,  name="position_output", activation='sigmoid',
                   kernel_initializer=seed, bias_initializer=seed)(x)

    # Model definition and compile
    model = Model(inputs=input, outputs=output, name="DistanceEstimationModel")

    return model


def inceptionModule(input_layer, c1, c3_in, c3_out, c5_in, c5_out, p_out, id):
    # 1x1 Convolution
    conv1 = Conv2D(c1, name=f'incept_{id}_conv_1', kernel_size=1,
                   activation='relu', padding='same')(input_layer)
    # 3x3 Convolution
    conv3 = Conv2D(c3_in, name=f'incept_{id}_conv_3_in', kernel_size=1,
                   activation='relu', padding='same')(input_layer)
    conv3 = Conv2D(c3_out, name=f'incept_{id}_conv_1_out', kernel_size=3,
                   activation='relu', padding='same')(conv3)
    # 5x5 Convolution
    conv5 = Conv2D(c5_in, name=f'incept_{id}_conv_5_in', kernel_size=1,
                   activation='relu', padding='same')(input_layer)
    conv5 = Conv2D(c5_out, name=f'incept_{id}_conv5_out', kernel_size=5,
                   activation='relu', padding='same')(conv5)
    # 3x3 Max Pooling
    pool = MaxPooling2D((3, 3), strides=1, padding='same')(input_layer)
    pool = Conv2D(p_out, name=f'incept_{id}_conv_pool', kernel_size=1,
                  activation='relu', padding='same')(pool)
    # Concatenate
    layers = [conv1, conv3, conv5, pool]
    output_layer = tf.keras.layers.concatenate(layers, axis=-1)
    return output_layer
