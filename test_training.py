import keras
from utils import create_demo_model

# grab mnist data set
mnist = keras.datasets.mnist
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()
train_images, test_images = train_images / 255.0, test_images / 255.0

model = create_demo_model()

# evaluate the model
print()
loss, acc = model.evaluate(test_images, test_labels)
print("Untrained model, accuracy: {:5.2f}%".format(100 * acc))

# load the saved weight into the model
checkpoint_path = "training/checkpoint.weights.h5"
model.load_weights(checkpoint_path)

# evaluate the model again
loss, acc = model.evaluate(test_images, test_labels)
print("Restored model, accuracy: {:5.2f}%".format(100 * acc))
