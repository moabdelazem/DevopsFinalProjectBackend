# Library Management System

## Tech Using
- Python
- Flask Microframework
- JSON as Database
- Reactjs

# API Structure Backend Endpoints

GET / Get endpoint to get all the requierd books 
`localhost:5000/api/books`

POST / Create New User to get all the required books
`localhost:5000/api/books`

PUT / To Update The Status Of The Borrowed Books
`localhost:5000/api/books/borrow`

DELETE / To Delete Specfic Book By The ${book_id}
`localhost:5000/api/books/${book_id}`

GET / Search For The Book By It's Id  ${book_id}
`localhost:5000/api/books/search=id?${book_id}`