from flask import render_template

def error(message):
    for char in message:
        if char == " ":
            char = "_"
    # memegen.link
    return render_template("error.html", link=(f"https://api.memegen.link/images/sadfrog/Error/{message}.png?width=600&height=600"))