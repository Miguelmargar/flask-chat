import os
from flask import Flask, redirect, render_template, request

app = Flask(__name__)

#stores the messages and it has to be in global scope to keep the messages


messages = [] # this list is made up of different diccionaries with sender and body as made up at the bottom of this


banned_words = ["feck", "crap", "duck"]


@app.route("/")
def index_page():
    return render_template("index.html")
    
    
#this creates the different rooms but needs a html with room create button and messages list would need to be made a dictionary    
# @app.route("rooms/add")
# def add_room():
#     room_name = request.form.get("roomname")
#     rooms[roomname] = []
#     return redirect(.....)
    
    
    
@app.route("/login", methods=["GET"])
def do_login():
    username = request.args.get("username")
    #return username   -- this line will check in the browser if it is correct as we'll be able to see the url 
    return redirect(username)   
    
    
@app.route("/<username>")
def get_userpage(username):
    filtered_message = []
  # this filters out the messages that are not for the usename in question  
    for i in messages:
        if i["body"][0] != "@":
            filtered_message.append(i)
        elif i["body"].split()[0][1:] == username:
            filtered_message.append(i)
    return render_template("chat.html", logged_as=username, all_the_messages=filtered_message)


@app.route("/<username>/new", methods=["POST"])
def add_message(username):
    text = request.form.get("message")
    
    words = text.split()
    words = [ "*" * len(word) if word.lower() in banned_words else word for word in words]
#the directly below is the same as the list conprenhension above     
    # for word in words:
    #     if word.lower() in banned_words:
    #             word = "*" * len(word)
    
    text = " ".join(map(str,words))
    
    message = {
        "sender": username,
        "body": text
    }
    messages.append(message)
    return redirect(username)
        

if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)))