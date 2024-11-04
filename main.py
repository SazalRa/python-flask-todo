from flask import Flask, jsonify, request, render_template, url_for, redirect
from flask_basicauth import BasicAuth
#from pymongo import MongoClient 
from flask_pymongo import PyMongo
from bson import SON, ObjectId
from flask_admin import Admin
from flask_admin.contrib.pymongo import ModelView
from wtforms import form, fields
# 

from flask import Flask, redirect, url_for
from flask_pymongo import PyMongo
from flask_admin import Admin
from flask_admin.contrib.pymongo import ModelView
from wtforms import form, fields
from bson.objectid import ObjectId  # To work with MongoDB object IDs
import os

# Initialize Flask app
# Initialize Flask app
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/flask_database"
mongo = PyMongo(app)

basic_auth = BasicAuth(app)

app.config["SECRET_KEY"] = os.urandom(24)
app.config["BASIC_AUTH_USERNAME"] = 'obscure'
app.config["BASIC_AUTH_PASSWORD"] = 'xxxxxx'

# Initialize Flask-Admin
admin = Admin(app, name="MicroBoss Dashboard", template_mode='bootstrap4')

# Define a WTForms form for adding new entries in MongoDB
class TodoForm(form.Form):
    content = fields.StringField('Content')
    degree = fields.StringField('Degree')

# Custom MongoDB ModelView
class MyModelView(ModelView):
    column_list = ('content', 'degree')  # Fields to display in the list view
    form = TodoForm  # Specify the form class for adding/editing entries

def __init__(self, collection, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.collection = collection

def get_pk_value(self, model):
    # Return the primary key for the model (MongoDB uses '_id')
    return str(model.get('_id'))

def get_list(self, page, sort_field, sort_desc, search, filters, page_size=None):
    # Fetch a list of documents from the MongoDB collection
    return list(self.collection.find()), self.collection.count_documents({})

def get_one(self, id):
    # Retrieve a single document by '_id'
    return self.collection.find_one({"_id": ObjectId(id)})

def create_model(self, form):
    # Insert a new document into the MongoDB collection
    self.collection.insert_one(form.data)
    return True

def delete_model(self, model):
    # Delete a document by '_id'
    self.collection.delete_one({"_id": ObjectId(model['_id'])})
    return True

# Register the MongoDB collection with Flask-Admin
admin.add_view(MyModelView(mongo.db.todos, 'Todos'))

# Define a route to ensure the app is running
@app.route('/')
@basic_auth.required
def index():
    return redirect(url_for('admin.index'))

if __name__ == '__main__':
    app.run(debug=True, threaded=True)