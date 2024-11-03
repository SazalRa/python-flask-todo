from flask import Flask, jsonify, request, render_template, url_for, redirect
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('localhost',27017)

db = client.flask_database
# this is mongodb database
todos = db.todos




@app.route('/hello', methods=['GET'])
def helloworld():
    if(request.method == ['GET']):
        data = { "data": "Hello, World!" }
        return jsonify(data)
@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)