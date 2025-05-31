import tensorflow as tf
import keras
import os
import utils

print("train.py running !!")
print("tensorflow version: ", tf.version.VERSION)

(train_images, train_tags), (test_images, test_tags) = utils.load_training_data()

model = utils.create_model()
print()
print(model.summary())

checkpoint_path = "training/model.weights.h5"
if os.path.exists(checkpoint_path):
    model.load_weights(checkpoint_path)

# Create a callback that saves the model's weights
cp_callback = keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                             save_weights_only=True,
                                             verbose=1)

# Train the model with the new callback
model.fit(train_images, 
          train_tags,  
          epochs=100,
          validation_data=(test_images, test_tags),
          callbacks=[cp_callback])  # Pass callback to training

model.evaluate(test_images, test_tags)
