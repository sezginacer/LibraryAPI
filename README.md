## Library API
This is a project for MetGlobal Academy

### API Reference

|    Endpoint   |  HTTP Request |                     Description                               |  Authentication Required |
|:--------------|:-------------:|:-------------------------------------------------------------:|:------------------------:|
|  /            |     GET       |   Gives available endpoints and HTTP methods                  |   No                     |
|  token/       |     POST      |   Gives the access token for the user                         |   No                     |
|  login/       |     POST      |   Logins the user                                             |   No                     |
|  logout/      |     GET       |   Logouts the user                                            |   No                     |
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
