
# Project Name - BOOKSLOGGER

Write a small description of your project

    This is small project where an user can read and add star rating and reviews on the book


## Feature list
    1. User signup - user can be Adder ( one who can add/edit the book inventory) and another is Reader 
    2. User login
    3. If User is type Adder - can add/edit books
    4. User - Can select a book to read, and add stars rating and review on the book
    5. User - Can see the list of books read
    6. Can see all the reviews rating on any book


## Architecture/Flow Diagram
 - Create user - User Type (Adder/ Reader)
 - After User logins 
    - If User Type is Adder, user can
        - Add book
        - edit book
        - delete book ( only if there are no stars and reviews on the book)
        - Pick a book
        - review book
    - If User Type is Reader. user can
        - Pick a book to read
        - review book
        - list all the book that is read/reviewed
- User logoff

## API Design

List all the APIs it's methods, request and response params

1. ErrorHandler

    URL:        http://127.0.0.1:5000/pagenotfound
    Method :    GET
    Request:    wrongpage
    Response:   404 - Page Not Found


2. Homepage

    URL:        http://127.0.0.1:5000/
    Method :    GET
    Request:    NONE
    Response:   200 - OK

3. UserSignIn

    URL:        http://127.0.0.1:5000/signup
    Method :    POST
    Request:    JSON input
                {
                    "firstname": "<firstname>",
                    "lastname":" <lastname>",
                    "username": "<username>",
                    "password": "<password>",
                    "email":   "<email>",
                    "is_reader":<0/1>
                }
    Response:   200 - New User created
    ERROR:      400 - User already exists 

4. login

    URL:        http://127.0.0.1:5000/login
    Method :    POST
    Request:    Basic Authentication (username,password)
    Response:   200 - User logged in
    ERROR:      400 - User not found

5. logoff

    URL:        http://127.0.0.1:5000/logoff 
    Method :    POST
    Request:    NONE
    Response:   200 - User logged off 

6.  List_All_Users
    URL:        http://127.0.0.1:5000/users 
    Method :    GET
    Request:    NONE
    Response:   200 - JSON response - List of all users

7.  List_All_Books
    URL:        http://127.0.0.1:5000/book 
    Method :    GET
    Request:    NONE
    Response:   200 - JSON response - List of all books

8.  Add_Book
    URL:        http://127.0.0.1:5000/book 
    Method :    POST
    Request:    JSON - {
                            "title" : "<titlename>",
                            "author": "<authorname>",
                            "isbn"  : "<isbn number>"               
                        }
    Response:   200 - JSON response - new book that is added
    ERROR:      401 Errors 
                - Please login
                - UserType is Reader, Cannot add books
                - Wrong input format

9.  Delete_Book
    URL:        http://127.0.0.1:5000/book 
    Method :    DELETE
    Request:    JSON -  {    	
		                    "bid" : "<bookid>"
                        }
    Response:   200 - JSON response - new book that is added
    ERROR:      401 Errors 
                - Please login
                - UserType is Reader, Cannot delete books
                - Cannot delete this book- stars, reviews info exists
10. Edit_Book
    URL:        http://127.0.0.1:5000/book 
    Method :    PATCH
    Request:    JSON -  {
                            "bid":<bookid>
                            "title":"<title>",
                            "author":"<author>",
                            "isbn":"<isbn>"
                            
                        }
    Response:   200 - JSON response -  book that is updated
    ERROR:      401 Errors 
                - Please login
                - UserType is Reader, Cannot edit books

11. List All Books All_users read
    URL:        http://127.0.0.1:5000/readbook/all
    Method :    GET
    Request:    NONE
    Response:   200 - JSON response - List of all book info from bookread table.

12. Pick a book to read by bookid  
    URL:        http://127.0.0.1:5000/readbook/<b_id>
    Method :    POST
    Request:    NONE
    Response:   200 - "Read your book".
    ERROR:      401 - Please login
                    - This book is already read, You can review the book

13. Stars rating and review book that is already read
    URL:        http://127.0.0.1:5000/readbook/<b_id>
    Method :    PATCH
    Request:    JSON -{
                        "stars":<number 1-5>,
                        "review":"<comment>"
                    }
    Response:   200 - "Thanks for reviewing."
    ERROR:      401 - Please login
                    - Please Read before You can review the book

14. All books read by an user
    URL:        http://127.0.0.1:5000/readbook/
    Method :    GET
    Request:    NONE
    Response:   200 - JSON response - List of all books read by signed in user from bookread table.
    ERROR:      401 - Please login

15. All reviews on a book by all users
    URL:        http://127.0.0.1:5000/readbook/<b_id>
    Method :    GET
    Request:    NONE
    Response:   200 - JSON response - List of all books read or reviewed from bookread table

## DB Design Diagram
                        user
                        -------
            ------->    uid       integer,primary_key
            |            firstname string
            |            lastname  string
            |            username  string
            |            password  string
            |           email     string
            |            is_reader boolean # 0 - Adder, 1 -Reader
            |
            |
            |
            |       book
            |       ------
    --------|------> bid     integer, primary_key
    |       |       title   string
    |       |       author  string
    |       |       isbn    string
    |       |-----  user_id integer ForeignKey('user.uid')
    |       |
    |       |
    |       |
    |       |               bookread
    |       |               ---------
    |       |
    |       |               id       Integer, rimary_key=True
    |       |-------------  user_id  Integer, ForeignKey('user.uid')
    |---------------------  book_id  Integer, ForeignKey('book.bid')
                            stars    Integer  (valid values 1-5)
                            review   string




## Coding Issues and Learning
1. ModuleNotFoundError and ImportError
2. and clause in sqlalchemy
3. Authentication 
4. Logging
5. HTTP error handling


## Deployment Instructions
TODO

## Repo Setup
TODO

> Add How to setup and run your app
> This is what you will use to deploy your app, so create a seperate requirements.txt file here









