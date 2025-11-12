# src/borrower.py

class Borrower:
    def __init__(self, name, contact, membership_id):
        """
        membership_id: unique identifier (string or int)
        borrowed_books: list of tuples (isbn, due_date) or (Book, due_date)
        """
        self.name = name
        self.contact = contact
        self.membership_id = str(membership_id)
        self.borrowed_books = []  # hold tuples (isbn, due_date)

    def update_contact(self, new_contact):
        self.contact = new_contact
        return True, "Contact updated."

    def add_borrowed(self, isbn, due_date):
        self.borrowed_books.append((str(isbn), due_date))
        return True, f"Recorded borrow of ISBN {isbn}, due {due_date}."

    def remove_borrowed(self, isbn):
        isbn = str(isbn)
        for i, (b_isbn, due) in enumerate(self.borrowed_books):
            if b_isbn == isbn:
                self.borrowed_books.pop(i)
                return True, f"Removed borrowed ISBN {isbn}."
        return False, "Book not found in borrower's records."

    def list_borrowed(self):
        """Return shallow copy for printing or inspection."""
        return list(self.borrowed_books)

    def __str__(self):
        return f"{self.name} (ID: {self.membership_id}, Contact: {self.contact})"
