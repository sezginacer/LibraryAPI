## Library API
This is a project for MetGlobal Academy

### API Reference

|    Endpoint   |  HTTP Request |                     Description                               |  Authentication Required |
|:--------------|:-------------:|:-------------------------------------------------------------:|:------------------------:|
|  /            |     GET       |   Gives available endpoints and HTTP methods                  |   No                     |
|  token/       |     POST      |   Gives the access token for the user                         |   No                     |
|  login/       |     POST      |   Logins the user                                             |   No                     |
|  logout/      |     GET       |   Logouts the user                                            |   No                     |
|  signup/      |     POST      |   Registers user                                              |   No                     |
|  library/     |     POST      |   Deletes all books and authors, create new library           |   Yes                    |
|  library/     |     PATCH     |   Keeps existing books and authors adds new books and authors |   Yes                    |
|  book/        |     GET       |   Gives all books                                             |   Yes                    |     
|  book/        |     POST      |   Creates new book                                            |   Yes                    |
|  author/      |     GET       |   Gives all authors                                           |   Yes                    |
|  author/      |     POST      |   Creates new author                                          |   Yes                    |
|  book/{id}/   |     GET       |   Gives the book with given ID                                |   Yes                    |
|  book/{id}/   |     PATCH     |   Updates the book with given ID                              |   Yes                    |
|  book/{id}/   |     PUT       |   Updates the book with given ID                              |   Yes                    |
|  author/{id}/ |     GET       |   Gives the author with given ID                              |   Yes                    |
|  author/{id}/ |     PATCH     |   Updates the author with given ID                            |   Yes                    |
|  author/{id}/ |     PUT       |   Updates the author with given ID                            |   Yes                    |

### Access to API
It's a must to signup to do library operations. An API access token will be given after signup. In
order to get token for registered user, `token/` endpoint can be used.

### Using API and Client
First clone repo, then goto project's home directory and run `firstrun.sh`. This script creates
virtual environment, activates it, installs project requirements, creates database schema, creates
user with username `admin` and password `admin`, populates database with books and authors, finally
runs the server. After running server, now `client.py` can be used to test Library API.
