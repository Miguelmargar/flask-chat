import os
from flask import Flask, redirect, render_template, request
from random import choice
from pymongo import MongoClient
from bson.objectid import ObjectId

MONGODB_URI = os.environ.get("MONGODB_URI")
MONGODB_NAME = os.environ.get("MONGODB_NAME")

app = Flask(__name__)


welcome_messages = ["Hi", "Hello", "Bonjour", "Ciao", "Hola", "Annyeonghaseyo"]




@app.route("/")
def get_index():
    welcome = choice(welcome_messages)
    with MongoClient(MONGODB_URI) as conn:
        db = conn[MONGODB_NAME]
        items = db.tasklist.find()
    return render_template('index.html', msg=welcome, tasks=items)








@app.route("/new_task", methods=['POST'])
def create_a_task():
    task = {
        'name': request.form['task_to_do'],
        'done': False
    }
    
    with MongoClient(MONGODB_URI) as conn:
        db = conn[MONGODB_NAME]
        db.tasklist.insert(task)    
    return redirect("/")









@app.route("/toggle", methods=['POST'])
def toggle_status():
    id = request.form.get('taskid')
    with MongoClient(MONGODB_URI) as conn:
        db = conn[MONGODB_NAME]
        item = db.tasklist.find_one({"_id": ObjectId(id)})
        item['done'] = not item['done']
        db.tasklist.save(item)
    return redirect("/")






@app.route("/edit/<taskid>", methods=["GET", "POST"])
def edit_task(taskid):
    with MongoClient(MONGODB_URI) as conn:
        db = conn[MONGODB_NAME]
        item = db.tasklist.find_one({"_id": ObjectId(taskid)})

    if request.method=="POST":
        item['name'] = request.form.get('task_name')
        item['done'] = request.form.get('task_done')
        with MongoClient(MONGODB_URI) as conn:
            db = conn[MONGODB_NAME]
            db.tasklist.save(item)
            return redirect("/")
    else:
        return render_template('edit_task.html', task=item)






if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug=True)