# src/book.py

class Book:
    def __init__(self, title, author, isbn, genre, quantity=1):
        """
        quantity: integer (>= 0)
        isbn: string (unique identifier for the book)
        """
        self.title = title
        self.author = author
        self.isbn = str(isbn)
        self.genre = genre
        self.quantity = int(quantity)

    def update_quantity(self, new_quantity):
        """Set quantity (must be >= 0)."""
        try:
            new_q = int(new_quantity)
            if new_q >= 0:
                old = self.quantity
                self.quantity = new_q
                return True, f"Quantity updated from {old} to {self.quantity}."
            else:
                return False, "Quantity cannot be negative."
        except (TypeError, ValueError):
            return False, "Invalid quantity value."

    def check_availability(self):
        """Returns True if at least one copy is available."""
        return self.quantity > 0

    def borrow_copy(self):
        """Decrease quantity by 1 if available. Return True/False and message."""
        if self.check_availability():
            self.quantity -= 1
            return True, f"Borrowed '{self.title}'. Remaining: {self.quantity}."
        return False, f"'{self.title}' is out of stock."

    def return_copy(self):
        """Increase quantity by 1 when a copy is returned."""
        self.quantity += 1
        return True, f"Returned '{self.title}'. Now available: {self.quantity}."

    def update_details(self, title=None, author=None, genre=None):
        """Update details selectively."""
        if title:
            self.title = title
        if author:
            self.author = author
        if genre:
            self.genre = genre
        return True, "Details updated."

    def to_dict(self):
        """Optional: helpful for future persistence."""
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "genre": self.genre,
            "quantity": self.quantity,
        }

    def __str__(self):
        status = "Available" if self.check_availability() else "Out of Stock"
        return f"{self.title} by {self.author} | ISBN: {self.isbn} | {self.genre} | Qty: {self.quantity} ({status})"
