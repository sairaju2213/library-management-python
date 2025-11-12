# src/library.py

from datetime import datetime, timedelta
from src.book import Book
from src.borrower import Borrower

class Library:
    def __init__(self):
        self.books = {}      # map isbn -> Book
        self.borrowers = {}  # map membership_id -> Borrower

    # ---------------- Books ----------------
    def add_book(self, book: Book):
        """Add a Book object. If ISBN exists, increase quantity."""
        isbn = str(book.isbn)
        if isbn in self.books:
            self.books[isbn].quantity += book.quantity
            return True, f"Existing book found. Increased quantity to {self.books[isbn].quantity}."
        self.books[isbn] = book
        return True, "Book added."

    def update_book_details(self, isbn, **kwargs):
        isbn = str(isbn)
        if isbn not in self.books:
            return False, "Book not found."
        self.books[isbn].update_details(kwargs.get('title'), kwargs.get('author'), kwargs.get('genre'))
        if 'quantity' in kwargs:
            ok, msg = self.books[isbn].update_quantity(kwargs['quantity'])
            if not ok:
                return False, msg
        return True, "Book updated."

    def remove_book(self, isbn):
        isbn = str(isbn)
        if isbn in self.books:
            del self.books[isbn]
            return True, "Book removed."
        return False, "Book not found."

    def search_books(self, query=None, field='title'):
        """Search by title/author/genre/isbn (case-insensitive). Return list of Book objects."""
        results = []
        if not query:
            return list(self.books.values())
        q = str(query).lower()
        for book in self.books.values():
            if field == 'title' and q in book.title.lower():
                results.append(book)
            elif field == 'author' and q in book.author.lower():
                results.append(book)
            elif field == 'genre' and q in book.genre.lower():
                results.append(book)
            elif field == 'isbn' and q == book.isbn.lower():
                results.append(book)
        return results

    # ---------------- Borrowers ----------------
    def add_borrower(self, borrower: Borrower):
        mid = str(borrower.membership_id)
        if mid in self.borrowers:
            return False, "Borrower with this membership ID already exists."
        self.borrowers[mid] = borrower
        return True, "Borrower added."

    def update_borrower_contact(self, membership_id, new_contact):
        mid = str(membership_id)
        if mid not in self.borrowers:
            return False, "Borrower not found."
        return self.borrowers[mid].update_contact(new_contact)

    def remove_borrower(self, membership_id):
        mid = str(membership_id)
        if mid in self.borrowers:
            if self.borrowers[mid].borrowed_books:
                return False, "Borrower has borrowed books; cannot remove."
            del self.borrowers[mid]
            return True, "Borrower removed."
        return False, "Borrower not found."

    # ---------------- Borrow / Return ----------------
    def borrow_book(self, membership_id, isbn, borrow_days=14):
        mid = str(membership_id)
        isbn = str(isbn)

        if mid not in self.borrowers:
            return False, "Borrower not found."

        if isbn not in self.books:
            return False, "Book not found."

        book = self.books[isbn]
        borrower = self.borrowers[mid]

        if not book.check_availability():
            return False, "Book is out of stock."

        # Borrow operation
        ok, msg = book.borrow_copy()
        if not ok:
            return False, msg

        due_date = datetime.now() + timedelta(days=int(borrow_days))
        borrower.add_borrowed(isbn, due_date)
        return True, f"Book borrowed. Due date: {due_date.strftime('%Y-%m-%d %H:%M:%S')}."

    def return_book(self, membership_id, isbn):
        mid = str(membership_id)
        isbn = str(isbn)

        if mid not in self.borrowers:
            return False, "Borrower not found."
        if isbn not in self.books:
            return False, "Book not found in library records."

        borrower = self.borrowers[mid]
        # Remove from borrower record first
        removed, msg = borrower.remove_borrowed(isbn)
        if not removed:
            return False, "This borrower did not borrow that book."
        # Return copy to stock
        book = self.books[isbn]
        book.return_copy()
        return True, "Book returned successfully."

    # ---------------- Overdue and status ----------------
    def list_overdue(self):
        """Return list of tuples (Borrower, isbn, due_date, days_overdue)"""
        now = datetime.now()
        overdue = []
        for borrower in self.borrowers.values():
            for isbn, due in borrower.borrowed_books:
                if due < now:
                    days_over = (now - due).days
                    overdue.append((borrower, isbn, due, days_over))
        return overdue

    def borrower_status(self, membership_id):
        mid = str(membership_id)
        if mid not in self.borrowers:
            return False, "Borrower not found."
        borrowed = self.borrowers[mid].list_borrowed()
        return True, borrowed

    # ---------------- Utility ----------------
    def list_all_books(self):
        return list(self.books.values())

    def list_all_borrowers(self):
        return list(self.borrowers.values())
