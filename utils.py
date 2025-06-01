import keras
import sqlite3
import numpy as np

def create_demo_model() -> keras.Sequential:
    model = keras.models.Sequential([
        keras.layers.Input(shape=(28, 28)),
        keras.layers.Flatten(),
        keras.layers.Dense(128, activation='relu'),
        keras.layers.Dropout(0.2),
        keras.layers.Dense(10)
    ])

    model.compile(
        optimizer='adam',
        loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=['accuracy'],
    )

    return model

def create_table_if_it_doesnt_exist():
    con = sqlite3.connect("images.db")
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY,
            hash TEXT, tag_string_general TEXT,
            tag_string_character TEXT,
            tag_string_copyright TEXT,
            tag_string_artist TEXT,
            tag_string_meta TEXT
        )
    """)

def create_model() -> keras.Sequential:
    model = keras.models.Sequential([

        # rescale input
        keras.layers.Input(shape=(256, 256, 3)),
        keras.layers.Rescaling(1/255),

        # do some convolutions stuff
        keras.layers.Conv2D(32, 3, activation='relu'),
        keras.layers.MaxPooling2D(),
        keras.layers.Conv2D(64, 3, activation='relu'),
        keras.layers.MaxPooling2D(),

        # flatten it and do some dense stuff
        keras.layers.Flatten(),
        keras.layers.Dense(128, activation='relu'),

        # prevent overfitting
        keras.layers.Dropout(0.5),
        keras.layers.Dense(3)

    ])

    model.compile(
        optimizer='adam',
        loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=['accuracy'],
    )

    return model

def load_training_data():

    print("loading training data...")
    
    image_arr = np.load("image_data.npy")
    tag_arr = np.load("tag_data.npy")

    # sanity check that image and tag data matches up
    assert len(image_arr) == len(tag_arr)
    print(f"total items: {len(image_arr)}")

    split_thresh = (len(image_arr) // 6) * 5
    image_arr = np.split(image_arr, [split_thresh])
    tag_arr = np.split(tag_arr, [split_thresh])

    train_images = image_arr[0]
    train_tags = tag_arr[0]
    test_images = image_arr[1]
    test_tags = tag_arr[1]

    print(f"{len(train_images)} training items, {len(test_images)} testing items")
    return ((train_images, train_tags), (test_images, test_tags))
