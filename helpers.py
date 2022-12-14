from flask import render_template
import requests

def error(message):
    for char in message:
        if char == " ":
            char = "_"
    # memegen.link
    return render_template("error.html", link=(f"https://api.memegen.link/images/sadfrog/Error/{message}.png?width=600&height=600"))

def lookup(search_term, type, types):

    # validate input
    if search_term == None:
        return error("invalid search")
    if type not in types:
        return error("invalid type")

    for type in types:
        if type != "isbn":
            type = f"in{type}"

    # make request and ensure it returned properly
    data = requests.get(f"https://www.googleapis.com/books/v1/volumes?q={search_term}+{type}")
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
        
        dict = {}

        # add isbn to dictionary
        try:
            isbns = item["industryIdentifiers"]
            for isbn in isbns:
                if isbn["type"] == "ISBN_13":
                    dict["isbn"] = isbn["identifier"]
        except (KeyError, ValueError):
            None

        try:
            isbns = item["industryIdentifiers"]
            for isbn in isbns:
                if isbn["type"] == "ISBN_10":
                    dict["isbn_10"] = isbn["identifier"]
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
        try:
            if dict["authors"] != None:
                str = ""
                counter = 0
                for author in dict["authors"]:
                    str += author
                    if counter != (len(dict["authors"]) - 1):
                        str += ", "
                dict["authors"] = str
        except (KeyError, ValueError):
            None

        response.append(dict)
        
    return response

def lookup_specific(isbn, types):
    
    # look up isbn
    response = lookup(isbn, "isbn", types)
    
    book = None

    # parse response 
    for item in response:
        try:
            # casting to int so it actually registers it!!!
            if int(item["isbn"]) == int(isbn):
                return item
        except (KeyError, ValueError):
            None
    
    # if nothing is found, return none
    return None