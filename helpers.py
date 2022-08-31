def error(message):
    for char in message:
        if char == " ":
            char = "_"
    # memegen.link
    return (f"https://api.memegen.link/images/sadfrog/Error/{message}.png?width=600&height=600")