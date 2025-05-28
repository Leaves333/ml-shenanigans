import numpy as np
import os
from PIL import Image

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

# converts an image to an 3d array, containing the rgb values of each pixel
def convert_image_to_array(img: Image.Image):
    arr = np.zeros((img.size[0], img.size[1], 3), dtype=np.uint8)
    for i in range(img.size[0]):
        for j in range(img.size[1]):

            # NOTE: the code error doesn't actually cause problems

            pixel: tuple[int, int, int]  = img.getpixel((i, j))
            arr[i][j][0] = pixel[0]
            arr[i][j][1] = pixel[1]
            arr[i][j][2] = pixel[2]
    return arr

IMAGE_PATH = "images/679cd0fa56e8296a174cc33dd99b1a36_51.jpg"

print("process images running!")
resized_image = resize_image(IMAGE_PATH)
arr = convert_image_to_array(resized_image)
print(arr)

# print(get_id_from_filepath(IMAGE_PATH))
