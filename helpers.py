from flask import render_template
import requests

def error(message):
    for char in message:
        if char == " ":
            char = "_"
    # memegen.link
    return render_template("error.html", link=(f"https://api.memegen.link/images/sadfrog/Error/{message}.png?width=600&height=600"))

def lookup(search_term, query_type):
    # validate input
    if query_type not in ["intitle", "inauthor", "isbn", "inpublisher"]:
        return None

    # make request and ensure it returned properly
    data = requests.get(f"https://www.googleapis.com/books/v1/volumes?q={search_term}+{query_type}")
    if data.status_code != 200:
        return None
    
    # parse data
    data = data.json()

    response = []
    for book in data["items"]:
        item = book["volumeInfo"]
        #TODO: figure out why description, avgRating, and pageCount weren't working
        dict = {
            "title": item["title"],
            "authors": item["authors"],
            "publisher": item["publisher"],
            "date": item["publishedDate"],
            "img_link_small": (item["imageLinks"])["smallThumbnail"],
            "img_link_large": (item["imageLinks"])["thumbnail"],
            "isbn_13": ((item["industryIdentifiers"])[0])["identifier"],
            "isbn_10": ((item["industryIdentifiers"])[1])["identifier"]
        }
        response.append(dict)

    return response

