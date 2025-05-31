import keras
import utils

print("test training running!")

(a, b), (c, d) = keras.datasets.mnist.load_data()
print(f"mnist: {len(d)}")

(train_images, train_labels), (test_images, test_labels) = utils.load_training_data()
train_images, test_images = train_images / 255.0, test_images / 255.0
print(f"my test: {len(test_images)}")

model = utils.create_model()

# evaluate the model
print()
loss, acc = model.evaluate(test_images, test_labels)
print("Untrained model, accuracy: {:5.2f}%".format(100 * acc))

# load the saved weight into the model
checkpoint_path = "training/model.weights.h5"
model.load_weights(checkpoint_path)

# evaluate the model again
loss, acc = model.evaluate(test_images, test_labels)
print("Restored model, accuracy: {:5.2f}%".format(100 * acc))
