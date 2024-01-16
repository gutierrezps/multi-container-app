import datetime
import os

from bson.objectid import ObjectId
from flask import Flask, redirect, render_template, request
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = f"mongodb://{os.environ['MONGO_HOST']}:27017/tasks"
mongo = PyMongo(app)

@app.route("/", methods=['GET'])
def home():
    tasks = mongo.db.tasks.find()
    return render_template(
        "index.html",
        tasks=tasks,
        n_tasks=len(list(tasks.clone())))

@app.route("/", methods=['POST'])
def new_task():
    task = {
        "task": request.form['task'],
        "created_at": datetime.datetime.now(tz=datetime.timezone.utc),
    }
    mongo.db.tasks.insert_one(task)
    return redirect('/')

@app.route("/delete", methods=['POST'])
def delete_task():
    task = { "_id": ObjectId(request.form['id']) }
    mongo.db.tasks.delete_one(task)
    return redirect('/')
