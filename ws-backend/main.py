from flask import Flask, render_template, request
from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os

load_dotenv()
api_key_id = os.getenv('API_KEY_ID')
api_key = os.getenv('API_KEY')
host = os.getenv('HOST')

# es = Elasticsearch(host, api_key=(api_key_id, api_key), verify_certs=False)
es = Elasticsearch(host, basic_auth=(
    "elastic", "*wTCURruehG0l*SCdjW8"), verify_certs=False)
print(es)
app = Flask(__name__)
picFolder = os.path.join('static', 'img')
app.config['UPLOAD_FOLDER'] = picFolder
# print(es.get(index="movies", id="1"))


@app.route('/')
def home():
    logo = os.path.join(app.config['UPLOAD_FOLDER'], 'GooseGoose.png')
    return render_template('search.html', user_image=logo)


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query']
        # print(query)
        res = es.search(index="movies", body={
            "query": {
                "bool": {
                    "should": [
                        {"match": {"title": query}}
                    ]
                }
            }
        })
        # print(res)
        return render_template('search_results.html', results=res['hits']['hits'])
    return render_template('search.html')


if __name__ == '__main__':
    app.run(port=5000, debug=True)
