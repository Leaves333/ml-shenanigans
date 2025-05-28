import tensorflow as tf
import keras
import os
import utils

print("train.py running !!")
print("tensorflow version: ", tf.version.VERSION)

(train_images, train_tags), (test_images, test_tags) = utils.load_training_data()
