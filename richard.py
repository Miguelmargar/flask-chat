import os
from flask import Flask, redirect, render_template, request

app = Flask(__name__)

# Stores messages between requests
messages = []

banned_words = {
    'cat',
    'cats',
    'trump',
    'duck'
    }

@app.route("/")
def get_index():
    return render_template("index.html")
    
    
@app.route("/login")
def do_login():
    username = request.args['username']
    return redirect(username)

def can_see_message(message, username):
    for_everyone = not message['body'].startswith('@')
    for_this_user = message['body'].startswith('@' + username)
    user_is_sender = message['sender'] == username
    
    return for_everyone or for_this_user or user_is_sender

@app.route("/<username>")
def get_userpage(username):
    
    filtered_messages = []
    for message in messages:
        if can_see_message(message, username):
            filtered_messages.append(message)
    
    return render_template("chat.html", logged_in_as=username, messages=filtered_messages)


@app.route("/new", methods=["POST"])
def add_message():
    username = request.form['username']
    text = request.form['message']
    
    words = text.split()
    words = [ "*" * len(word) if word.lower() in banned_words else word for word in words]
    
    text = " ".join(map(str,words))

    message = {
        'sender': username,
        'body': text,
    }
    
    messages.append(message)
    return redirect(username)


if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)))