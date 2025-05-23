import tensorflow as tf
import keras
import os

from utils import create_model

print("script running !!")
print("tensorflow version: ", tf.version.VERSION)

# grab mnist data set
mnist = keras.datasets.mnist
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()
train_images, test_images = train_images / 255.0, test_images / 255.0

# train the model for some time
model = create_model()
print()
print(model.summary())

# model.fit(train_images, train_labels, epochs=5)
# model.evaluate(test_images, test_labels)

checkpoint_path = "training/checkpoint.weights.h5"
checkpoint_dir = os.path.dirname(checkpoint_path)

# Create a callback that saves the model's weights
cp_callback = keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                             save_weights_only=True,
                                             verbose=1)

# Train the model with the new callback
model.fit(train_images, 
          train_labels,  
          epochs=10,
          validation_data=(test_images, test_labels),
          callbacks=[cp_callback])  # Pass callback to training

# This may generate warnings related to saving the state of the optimizer.
# These warnings (and similar warnings throughout this notebook)
# are in place to discourage outdated usage, and can be ignored.
