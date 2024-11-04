from flask import Flask, jsonify, request, render_template, url_for, redirect
from pymongo import MongoClient 
from bson import SON, ObjectId
from flask_admin import Admin


app = Flask(__name__)

admin = Admin(app, name="microblog", template_mode='bootstrap4')

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
    if request.method == "POST":
       
        content = request.form["content"]
        degree = request.form["degree"]
        todos.insert_one({
            "content": content,
            "degree": degree
        })

    all_todos = todos.find()
    return render_template('index.html', todos = all_todos)


@app.route("/<id>/delete", methods=["POST"])
def delete(id):
    todos.delete_one({
        "_id": ObjectId(id)
    })
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(debug=True, threaded=True)