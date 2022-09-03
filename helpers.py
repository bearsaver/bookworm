from flask import render_template
import requests

def error(message):
    for char in message:
        if char == " ":
            char = "_"
    # memegen.link
    return render_template("error.html", link=(f"https://api.memegen.link/images/sadfrog/Error/{message}.png?width=600&height=600"))

def lookup(search_term):
    # validate input
    if search_term == None:
        return error("invalid search")

    # make request and ensure it returned properly
    data = requests.get(f"https://www.googleapis.com/books/v1/volumes?q={search_term}+isbn")
    if data.status_code != 200:
        return None

    data = data.json()

    # make sure there are actual results
    if data["totalItems"] == 0:
        return None

    book_data = [("title", "title"), ("authors", "authors"), ("publisher", "publisher"), ("date", "publishedDate"),
                 ("description", "description"), ("page_count", "pageCount")]
    
    # parse data
    response = []
    for book in data["items"]:
        item = book["volumeInfo"]
        id = book["id"]
        isbns = item["industryIdentifiers"]
        
        dict = {}

        # add isbn to dictionary
        try:
            dict["isbn"] = isbns[0]["identifier"]
        except (KeyError, ValueError):
            None
        
        # add images to dictionary
        dict["img_small"] = f"http://books.google.com/books/content?id={id}&printsec=frontcover&img=1&zoom=5&edge=curl&source=gbs_api"
        dict["img"] = f"http://books.google.com/books/content?id={id}&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api"
        
        # try to add other data
        for label, ref in book_data:
            try:
                dict[label] = item[ref]
            except (KeyError, ValueError):
                None
            
        # parse author data
        if dict["authors"] != None:
            str = ""
            counter = 0
            for author in dict["authors"]:
                str += author
                if counter != (len(dict["authors"]) - 1):
                    str += ", "
            dict["authors"] = str

        response.append(dict)
        
    return response

