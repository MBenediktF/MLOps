import numpy as np
import tensorflow as tf
import tensorflow.keras.datasets.mnist as mnist
import matplotlib.pyplot as plt

# Load data
(trainX, trainY), (testX, testY) = mnist.load_data()
trainX, testX = np.reshape(trainX / 255.0, (trainX.shape[0], -1)), np.reshape(testX / 255.0, (testX.shape[0], -1))
trainY = tf.keras.utils.to_categorical(trainY)
testY = tf.keras.utils.to_categorical(testY)
print('Number of training images, number of pixels: \n', trainX.shape)
print('Number of test images, number of pixels: \n', testX.shape)


# Network architecture
inputs = tf.keras.layers.Input(shape=trainX.shape[1])
x = tf.keras.layers.Dense(128,
                          activation='relu', name='h1',
                          kernel_initializer=tf.keras.initializers.TruncatedNormal(stddev=0.1),
                          bias_initializer=tf.keras.initializers.TruncatedNormal(stddev=0.1))(inputs)
x = tf.keras.layers.Dropout(rate=0.1)(x)
x = tf.keras.layers.Dense(32,
                           activation='relu', name='h2',
                           kernel_initializer=tf.keras.initializers.TruncatedNormal(stddev=0.1),
                           bias_initializer=tf.keras.initializers.TruncatedNormal(stddev=0.1))(x)
x = tf.keras.layers.Dropout(rate=0.1)(x)
logits = tf.keras.layers.Dense(10, name='logits',
                               activation=None,
                               kernel_initializer=tf.keras.initializers.TruncatedNormal(stddev=0.1),
                               bias_initializer=tf.keras.initializers.TruncatedNormal(stddev=0.1))(x)
model = tf.keras.Model(inputs=inputs, outputs=logits)

model.summary()


optimizer = tf.keras.optimizers.SGD(learning_rate=1e-3)
cost = tf.keras.losses.CategoricalCrossentropy(from_logits=True)
model.compile(optimizer = optimizer,
              loss = cost,
              metrics=['accuracy'])

def get_batches(x, y, batch_size=128):
    """ Return a generator that yields batches from arrays x and y. """
    n_batches = len(x)//batch_size  # number of full batches

    for ii in range(0, n_batches*batch_size, batch_size):
        X, Y = x[ii: ii+batch_size], y[ii: ii+batch_size]
        yield X, Y

gen = get_batches(trainX, trainY, 128)

epochs = 5
learning_rate = 0.1
batch_size = 64

# Training
optimizer.learning_rate = learning_rate
for e in range(epochs):
    for x, y in get_batches(trainX, trainY, batch_size):
        loss, _ = model.train_on_batch(x,y)

    test_loss, test_acc = model.evaluate(testX, testY)
    print("Epoch: {:2}/{}".format(e+1, epochs),
          "Training loss: {:.5f}".format(loss),
          'Test Accuracy: {:.4f}'.format(test_acc))

print(model.evaluate(testX, testY))
model.save_weights("./Mnist-Digits.h5")
