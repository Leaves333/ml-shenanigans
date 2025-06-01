import keras
import os
import utils
import tensorflow as tf
import numpy as np

print("train.py running !!")
print("tensorflow version: ", tf.version.VERSION)

training_dataset, validation_dataset = keras.utils.image_dataset_from_directory(
    directory="images",
    labels="inferred",      # labels are based on folder structure
    label_mode="int",       # for sparse categorical crossentropy
    image_size=(256, 256),
    shuffle=True,
    seed=123,
    validation_split=0.2,   # amount of data to reserve for validation
    subset="both",          # return both the testing and validation datasets
)

model = utils.create_model()
print()
print(model.summary())

checkpoint_path = "training/model.weights.h5"
if os.path.exists(checkpoint_path):
    model.load_weights(checkpoint_path)
    pass

# Create a callback that saves the model's weights
cp_callback = keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                             save_weights_only=True,
                                             verbose=1)

# Train the model with the new callback
model.fit(training_dataset,  
          epochs=10,
          validation_data=validation_dataset,
          callbacks=[cp_callback])  # Pass callback to training

# model.evaluate(test_images, test_tags)
