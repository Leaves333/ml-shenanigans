import numpy as np
import os
import sqlite3
from PIL import Image
from numpy._core.multiarray import dtype

TARGET_TAGS = ["izuna_(blue_archive)",
               "arona_(blue_archive)",
               "kisaki_(blue_archive)",
               "shiroko_(blue_archive)",
               "plana_(blue_archive)"]

# gets an image's id in the database from its filename
def get_id_from_filepath(image_path: str) -> int:
    filename = os.path.basename(image_path)
    filename = filename.removesuffix(".jpg")
    id = filename[filename.find("_")+1:]
    return int(id)

# resizes an image to 128x128
def resize_image(image_path: str):
    with Image.open(image_path) as img:
        resized_image = img.resize(size=(128, 128));
        return resized_image

# converts an image to an 128x128x3 array, containing the rgb values of each pixel
def convert_image_to_array(image_path: str):

    img = resize_image(image_path)
    arr = np.zeros((128, 128, 3), dtype=np.uint8)

    for i in range(128):
        for j in range(128):

            # NOTE: the code error doesn't actually cause problems

            pixel: tuple[int, int, int]  = img.getpixel((i, j))
            if (type(pixel) == tuple):
                arr[i][j][0] = pixel[0]
                arr[i][j][1] = pixel[1]
                arr[i][j][2] = pixel[2]
            else:
                arr[i][j][0] = pixel
                arr[i][j][1] = pixel
                arr[i][j][2] = pixel
    return arr

# queries the sql database to get the tags for an image
# and then finds the idx of that tag in the target tags array
def get_image_tag_index(image_path: str):
    image_id = get_id_from_filepath(image_path)
    sql_command = f"""
        SELECT tag_string_character FROM images
            WHERE id=?
    """

    con = sqlite3.connect("images.db")
    cur = con.cursor()
    res = cur.execute(sql_command, [image_id])
    res_tuple: str = res.fetchone()
    tags = res_tuple[0].split()

    for tag in tags:
        if tag in TARGET_TAGS:
            return TARGET_TAGS.index(tag)

def process_data():

    image_paths = os.listdir("images")
    image_arr = np.zeros((len(image_paths), 128, 128, 3), dtype=np.uint8)
    tag_arr = np.zeros((len(image_paths)), dtype=np.uint8)

    for i in range(len(image_paths)):
        path = image_paths[i]
        image_arr[i] = convert_image_to_array(f"images/{path}")


    np.save("image_data.npy", image_arr)
    print("image data successfully saved!")

print("process images running!")
process_data()

# resized_image = resize_image(IMAGE_PATH)
# arr = convert_image_to_array(resized_image)
# print(arr)
#
# print(get_id_from_filepath(IMAGE_PATH))
