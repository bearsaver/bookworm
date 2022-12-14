# Bookworm
#### Video Demo: https://youtu.be/G0kUaABFpTA
#### Description:

Bookworm is a web app that mimics Goodreads' ability to search books and store them on shelves. Its goal is to be a minimalist alternative that can still effectively track the user's books.

Bookworm is based around the Google Books API, a free and flexible API that contains all of Google's book information. Because I am a beginner, using this API was difficult, as it often would fail to return the intended books or certain fields. After debating using the ISBNdb API, which seemed far more robust, I decided to continue using Google Books and try my best to make it work.

The webpage is essentially inacessible without a login. When a user  registers for the site, three bookshelves are created: "to read", "reading", and "read". By default, they are empty.

The user can fill their bookshelves using the "search" page. The user can make queries based on three categories: title, author, and ISBN. You can add books directly from the search, or view their details and descriptions before adding. I opted to use a simple table to display search results because I thought it was functional and visually appealing. 

The homepage displays the books that the user is currently reading. I debated adding more functionality, but realized that the user would likely spend minimal time on the page, and decided to keep it simple.

There are two ways to see your books: by viewing the individual shelf, which is displayed like search results, or clicking "my books" and viewing all the books at once. The user can also add custom shelves by going to the "shelves" page and clicking "add shelf".

I also initially planned on allowing the user to add notes and quotes to books; however, after pondering the vast possibilities for how to implement this, I decided it wouldn't be worth the time, and moved on. 


#### Files:

`app.py` contains all of the backend code. It verifies user input, interacts with the database, makes API requests using the helper functions, and passes informaiton to the pages. My SQL queries were relatively messy and could have been better, but they were functional, so I am leaving them as is. At first, I tried to use SQLAlchemy, but struggled to figure it out and opted to stick with CS50's SQL funcitons. Overall, this file is very straightforward.

`bookworm.db` stores all user, shelf, and book information. The `users` table contains three columns: `id`, `username`, and `password_hash` (a hash generated by the Werkzeug module). `shelves` also has three columns: `id`, `name`, and `user_id` (foreign key). `books` is more simple: it has two columns, `ISBN` and `shelf_id` (foreign key). I chose to use ISBNs as books' primary identifiers because it integrated well with the helper functions, and it works well.  

All of the `.html` files in `/templates` use Jinja2 templating. They also use Bootstrap. I wanted the pages' aesthetic to be simple and functional. For me, designing pages  was the hardest part, and I am very thankful for the tools that I used, because I would've been completely lost without them. Note: a lot of the HTML indentation is slightly messed up, as I was unsure how to indent when using Jinja syntax.

`helpers.py` contains a few supplemental functions that are integral to the program, and I'd like to talk about them, as I spent a lot of time working on them. `lookup()` queries the API and returns book information. `lookup_specific()`, which uses `lookup()`, is an incredibly important part of the app. Initially, when passing ISBNs between pages to identify a book, I would take the first result from regular `lookup()`, which very often failed to yield the intended book. For this reason, I created `lookup_specific()`, which uses `lookup()` and then parses through all of the results. When it finds the book with the exact intended API, it returns it. This function is incredibly important, as it enables ISBNs to be passed everywhere seamlessly.

Thanks to the CS50 staff for teaching me everything I needed to know. It's been an amazing ride, and I'm so glad I took the course.