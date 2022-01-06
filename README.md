# OpenLibrary

## About
This project contains api for OpenLibarary and this project used `Django Rest Framework` and based on `mircoservice` architecture.

## Available API
### Content Service
1. `http://127.0.0.1:8000/books` for **get request** returns all the available ordered by creation time and for **post request** create one new book.
2. `http://127.0.0.1:8000/books/topcontent` returns books based on interaction of book suports only **get rquest**.
3. `http://127.0.0.1:8000/books/<id>` supports **get**, **put** and **delete** request for reteriving, updating and deleting any particular book
4. `http://127.0.0.1:8000/books/uploadfile` it accpet only **post request** which help in ingesting the book via csv file. *Please put only (title, story, author) in the given order.*

### User Interaction Service
1. `http://127.0.0.1:8001/userbook/like` it accept only **post request** which helps user to like any book.
2. `http://127.0.0.1:8001/userbook/read` it accept only **post request** which helps user to read any book.

### User Service 
1. `http://127.0.0.1:8002/users` it accept **get and post** request which helps to get all the user and to create the user.
2. `http://127.0.0.1:8002/users/<pk>` it accept **get, put and delete** which helps in to get, update or delete the particular user


## How to run the webapp?
1. First pull the OpenLibrary `git pull https://github.com/gaddopur/OpenLibrary`.
2. Install docker if already not installed.
3. Open three terminals and go to the location of each service folder and type ```docker-compose up```.

