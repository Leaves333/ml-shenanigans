import keras
import utils
import numpy as np
import tensorflow as tf
from tabulate import tabulate

print("test training running!")

model = utils.create_model()

# load the saved weight into the model
checkpoint_path = "training/model.weights.h5"
model.load_weights(checkpoint_path)

img = keras.utils.load_img("test.jpg", target_size=(256, 256))
img_array = keras.utils.img_to_array(img)

# expand batch direction
# resize from (256, 256, 3) to (1, 256, 256, 3)
img_array = np.expand_dims(img_array, axis=0) 

training_dataset = keras.utils.image_dataset_from_directory(
    directory="images",
    labels="inferred",      # labels are based on folder structure
    label_mode="int",       # for sparse categorical crossentropy
    image_size=(256, 256),
    shuffle=True,
    seed=123,
)

class_names = training_dataset.class_names
logits = model.predict(img_array)
predictions = tf.nn.softmax(logits).numpy()


print()
print("prediction results:")
print()
print(tabulate(predictions, headers=class_names, tablefmt="github"))

prediction_class = class_names[np.argmax(predictions[0])]
confidence = np.max(predictions[0])
print()
print(f"final prediction: {prediction_class} with confidence {confidence:.3f}")
