from flask import Flask, render_template, request
from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os

load_dotenv()
api_key_id = os.getenv('API_KEY_ID')
api_key = os.getenv('API_KEY')
host = os.getenv('HOST')

es = Elasticsearch(host, api_key=(api_key_id, api_key))
app = Flask(__name__)
picFolder = os.path.join('static', 'img')
app.config['UPLOAD_FOLDER'] = picFolder


@app.route('/')
def home():
    logo = os.path.join(app.config['UPLOAD_FOLDER'], 'GooseGoose.png')
    return render_template('search.html', user_image=logo)


@app.route('/search/results', methods=['POST'])
def search():
    search_term = request.form["input"]
    print(search_term)
    return render_template('results.html', res=search_term)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
