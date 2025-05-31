from pybooru import Danbooru
from urllib.request import urlretrieve
import sqlite3
import utils
import os

TARGET_TAGS = ["izuna_(blue_archive)",
               "arona_(blue_archive)",
               "kisaki_(blue_archive)",
               "shiroko_(blue_archive)",
               "plana_(blue_archive)"]

def download_images_by_tag(tags: str, page: int):

    print(f"searching for {tags}")

    client = Danbooru('danbooru')
    posts = client.post_list(tags=tags, page=page, limit=100)

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
        if (post["score"] < 30):
            continue

        # get next id to use
        with open(ID_FILEPATH, "r") as file:
            id = int(file.read())
            id += 1
        with open(ID_FILEPATH, "w") as file:
            file.write(f"{id}")

        # get image tags
        tags_general: str = post["tag_string_general"]
        tags_character: str = post["tag_string_character"]
        tags_copyright: str = post["tag_string_copyright"]
        tags_artist: str = post["tag_string_artist"]
        tags_meta: str = post["tag_string_meta"]

        # filter out images with multiple matching characters in them
        character_list = tags_character.split()
        count = 0
        for character in character_list:
            if character in TARGET_TAGS:
                count += 1
        if count > 1:
            continue

        # download the image from the internet
        image_url = post["file_url"]
        image_hash = post["md5"]
        print(f"image found, downloading {image_hash}")
        filename = f"images/{image_hash}_{id}.jpg"
        urlretrieve(image_url, filename)

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

for tag in TARGET_TAGS:
    for page in range(1, 11):
        download_images_by_tag(tag, page)
