import json
import os

path = "/Users/wsrisuntikan/ir-websearch/movie_list"
category_list = [pos_json for pos_json in os.listdir(
    path) if pos_json.endswith('.json')]

index_count = 1
for category in category_list:
    with open(path+"/"+category) as json_file:
        tracks = json.load(json_file)
        for track in tracks["catalogItems"]:
            head = head = {"index": {"_id": index_count}}
            data = {
                "title_id": track["titleId"],
                "title": track["title"],
                "boxart":  track["boxart"],
                "category":  category.replace(".json", "")
            }
            index_count += 1
            with open("movies_list.json", "a") as outfile:
                json.dump(head, outfile)
                outfile.write("\n")
                json.dump(data, outfile)
                outfile.write("\n")
