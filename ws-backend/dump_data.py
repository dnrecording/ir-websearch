import json
import os
from dotenv import load_dotenv

load_dotenv()
path = os.getenv('PATH')

index_count = 1
with open(path) as json_file:
    tracks = json.load(json_file)
    for track in tracks["MoviesList"]:
        head = head = {"index": {"_id": index_count}}
        data = {
            "title_id": track["title_id"],
            "title": track["title"],
            "boxart":  track["boxart"],
            "category":  track["category"]
        }
        index_count += 1
        with open("movies_list.json", "a") as outfile:
            json.dump(head, outfile)
            outfile.write("\n")
            json.dump(data, outfile)
            outfile.write("\n")
