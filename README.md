##  Library Management System (Python)

A simple **Object-Oriented Programming (OOP)** based **Library Management System** built using Python.  
This project demonstrates core OOP concepts such as **classes**, **objects**, **encapsulation**, and **inheritance**, while offering basic library operations like adding books, registering borrowers, borrowing and returning books.

---

## **Features**
✅ Add, update, and remove books  
✅ Register borrowers (students/users)  
✅ Borrow and return books  
✅ Check book availability  
✅ Calculate due dates using `datetime` module  
✅ Simple console-based menu system  



 **Project Structure**

library-management-python/
├── src/
│ ├── book.py # Book class (attributes: title, author, ISBN, genre, quantity)
│ ├── borrower.py # Borrower class (tracks borrowed books)
│ └── library.py # Library class (core logic for management)
├── main.py # Entry point for user interaction
├── README.md # Project description and setup
└── .gitignore # Ignore pycache, env files, etc.