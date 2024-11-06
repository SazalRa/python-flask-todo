from flask import Flask, jsonify, request, render_template, url_for, redirect

from flask_pymongo import PyMongo
from flask_admin import Admin
from flask_admin.contrib.pymongo import ModelView
#from pymongo import MongoClient 
#from flask_pymongo import PyMongo
#from bson import SON, ObjectId
#from flask_admin import Admin
#from flask_admin.contrib.pymongo import ModelView
#from wtforms import form, fields
# 

#from flask import Flask, redirect, url_for

from wtforms import form, fields
from bson.objectid import ObjectId  # To work with MongoDB object IDs
import os
from flask_basicauth import BasicAuth

from flask_cors import CORS
from googleapiclient.discovery import build
from google.oauth2 import service_account
from google.cloud import bigquery
from dotenv import load_dotenv
load_dotenv()


# Initialize Flask app
# Initialize Flask app
app = Flask(__name__)
CORS(app)
app.config["MONGO_URI"] = "mongodb://localhost:27017/flask_database"
mongo = PyMongo(app)

basic_auth = BasicAuth(app)

app.config["SECRET_KEY"] = os.urandom(24)
app.config["BASIC_AUTH_USERNAME"] = 'obscure'
app.config["BASIC_AUTH_PASSWORD"] = 'xxxxxx'
app.config['BASIC_AUTH_FORCE'] = True

SERVICE_ACCOUNT_FILE = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
print("ok",SERVICE_ACCOUNT_FILE)
SCOPES = ['https://www.googleapis.com/auth/bigquery']

# Authenticate using the service account file
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

bigquery_client = bigquery.Client(credentials=credentials, project=credentials.project_id)

if not SERVICE_ACCOUNT_FILE:
    raise ValueError("Please set the GOOGLE_APPLICATION_CREDENTIALS environment variable")

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

@app.route('/api/sales-data', methods=["GET"])
def sales_data():
    
    data = {
        "monthly_sales": "4561.83",
        "daily_sales": "219.20",
        "yearly_sales": "31065.20",
        "currency": "USD"
    }
    return jsonify(data)

@app.route('/api/send', methods=['POST'])
def receive_data():
    received = request.json
    print("Received data:", received)
    return jsonify({"status": "success", "data_received": received})

@app.route('/biqquery-api-call')
def get_bigquery_data():
    # Example query
    query = """
        SELECT event_name FROM `somoy-analytics-v4.analytics_312613195.events_20241029` LIMIT 10
    """
    # Run the query
    query_job = bigquery_client.query(query)
    print(query_job)
    # Fetch results
    results = []
    for row in query_job:
        print(row)
        #results.append({"name": row.name, "total_number": row.total_number})
    
    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True, threaded=True, port= 5001)