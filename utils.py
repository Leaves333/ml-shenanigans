import keras
import sqlite3

def create_model() -> keras.Sequential:
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
            hash TEXT,
            tag_string_general TEXT,
            tag_string_character TEXT,
            tag_string_copyright TEXT,
            tag_string_artist TEXT,
            tag_string_meta TEXT
        )
    """)
