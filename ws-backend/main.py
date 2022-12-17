from flask import Flask, render_template, request
from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os

load_dotenv()
host = os.getenv('HOST')
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')

es = Elasticsearch(host, basic_auth=(
    username, password), verify_certs=False)
print(es)
app = Flask(__name__)
picFolder = os.path.join('static', 'img')
app.config['UPLOAD_FOLDER'] = picFolder


@app.route('/')
def home():
    logo = os.path.join(app.config['UPLOAD_FOLDER'], 'GooseGoose.png')
    return render_template('search.html', user_image=logo)


@app.route('/browse', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query']
        res = es.search(index="movies", size=50, body={
            "min_score": 1,
            "query": {
                "bool": {
                    "should": [
                        {
                            "multi_match": {
                                "query": query,
                                "fields": [
                                    "title",
                                    "category"
                                ],
                                "type": "most_fields",
                                "operator": "and",
                                "boost": 10
                            }
                        },
                        {
                            "multi_match": {
                                "query": query,
                                "fields": [
                                    "title",
                                    "category"
                                ],
                                "type": "most_fields",
                                "operator": "and",
                                "fuzziness": "AUTO",
                                "boost": 5
                            }
                        },
                        {
                            "multi_match": {
                                "query": query,
                                "fields": [
                                    "title",
                                    "category"
                                ],
                                "type": "most_fields",
                                "boost": 1
                            }
                        },
                        {
                            "multi_match": {
                                "query": query,
                                "fields": [
                                    "title",
                                    "category"
                                ],
                                "type": "most_fields",
                                "boost": 0.5,
                                "fuzziness": "AUTO"
                            }
                        }
                    ]
                }
            }
        })
        track_list = res["hits"]["hits"]
        title_list = []
        result = []
        for track in track_list:
            if track["_source"]["title_id"] not in title_list:
                title_list.append(track["_source"]["title_id"])
                result.append(track)
        print(result)
        return render_template('search_results.html', results=result)
    return render_template('search.html')


if __name__ == '__main__':
    app.run(port=5000, debug=True)
