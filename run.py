import os
from flask import Flask, redirect, render_template, request

app = Flask(__name__)

#stores the messages and it has to be in global scope to keep the messages
messages = []

@app.route("/")
def index_page():
    return render_template("index.html")
    
# @app.route("/")
# def get_index():
#     return "Welcome to your chat app!"    
    
@app.route("/login", methods=["GET"])
def do_login():
    username = request.args.get("username")
    #return username   -- this line will check in the browser if it is correct as we'll be able to see the url 
    return redirect(username)   
    
    
@app.route("/<username>")
def get_userpage(username):
    return render_template("chat.html", logged_as=username, all_the_messages=messages)


@app.route("/<username>/new", methods=["POST"])
def add_message(username):
    text = request.form.get("message")
    message = {
        "sender": username,
        "body": text
    }
    messages.append(message)
    return redirect(username)




app.run(host=os.getenv("IP"), port=int(os.getenv("PORT")), debug=True)