from pybooru import Danbooru
from urllib.request import urlretrieve
import sqlite3
import utils
import os

search_tags = "nekomata_okayu"
client = Danbooru('danbooru')
posts = client.post_list(tags=search_tags, random=True, limit=100)

ID_FILEPATH = "last_used_id.txt"
if not os.path.exists(ID_FILEPATH):
    with open(ID_FILEPATH, "w") as file:
        file.write("0")
utils.create_table_if_it_doesnt_exist()

for post in posts:

    # filter out explicit images
    explicit_ratings = ["e", "q"]
    if (post["rating"] in explicit_ratings):
        continue
    
    # filter for only jpgs
    if (post["file_ext"] != "jpg"):
        continue

    # filter out posts that can't be downloaded?
    if ("file_url" not in post):
        continue

    # filter out posts with low score
    if (post["score"] < 20):
        continue

    # get next id to use
    with open(ID_FILEPATH, "r") as file:
        id = int(file.read())
        id += 1
    with open(ID_FILEPATH, "w") as file:
        file.write(f"{id}")

    # download the image from the internet
    image_url = post["file_url"]
    image_hash = post["md5"]
    print(f"image found, downloading {image_hash}")
    filename = f"images/{image_hash}_{id}.jpg"
    urlretrieve(image_url, filename)

    # get image tags
    tags_general = post["tag_string_general"]
    tags_character = post["tag_string_character"]
    tags_copyright = post["tag_string_copyright"]
    tags_artist = post["tag_string_artist"]
    tags_meta = post["tag_string_meta"]

    # write metadata about the image into sqlite database
    sql_command = f"""
        INSERT INTO images VALUES
            (?, ?, ?, ?, ?, ?, ?)
    """
    sql_data = (id, image_hash, tags_general, tags_character, tags_copyright, tags_artist, tags_meta);

    con = sqlite3.connect("images.db")
    cur = con.cursor()
    cur.execute(sql_command, sql_data)
    con.commit()
