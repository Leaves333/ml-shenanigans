from pybooru import Danbooru
from urllib.request import urlretrieve
import sqlite3

search_tags = "shirakami_fubuki"
client = Danbooru('danbooru')
posts = client.post_list(tags=search_tags, random=True, limit=100)

with open("image_links.txt", "w") as file:
    for post in posts:

        # filter out explicit images
        explicit_ratings = ["e", "q"]
        if (post["rating"] in explicit_ratings):
            continue
        
        # filter for only jpgs
        if (post["file_ext"] != "jpg"):
            continue

        # filter out posts with low score
        if (post["score"] < 20):
            continue

        file.write(post["file_url"] + "\n")

        image_url = post["file_url"]
        image_hash = post["md5"]
        
        filename = f"images/{image_hash}.jpg"
        urlretrieve(image_url, filename)
