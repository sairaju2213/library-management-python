# main.py

from src.book import Book
from src.borrower import Borrower
from src.library import Library
from datetime import datetime

def print_menu():
    print("\n=== Library Menu ===")
    print("1. Add Book")
    print("2. Add Borrower")
    print("3. Borrow Book")
    print("4. Return Book")
    print("5. Search Books")
    print("6. List All Books")
    print("7. List Borrowed by Borrower")
    print("8. List Overdue")
    print("9. Exit")

def main():
    lib = Library()

    while True:
        print_menu()
        choice = input("Enter choice: ").strip()
        if choice == '1':
            title = input("Title: ").strip()
            author = input("Author: ").strip()
            isbn = input("ISBN: ").strip()
            genre = input("Genre: ").strip()
            qty = input("Quantity (default 1): ").strip() or "1"
            try:
                q = int(qty)
            except ValueError:
                print("Invalid quantity. Using 1.")
                q = 1
            book = Book(title, author, isbn, genre, q)
            ok, msg = lib.add_book(book)
            print(msg)

        elif choice == '2':
            name = input("Name: ").strip()
            contact = input("Contact: ").strip()
            mid = input("Membership ID: ").strip()
            borrower = Borrower(name, contact, mid)
            ok, msg = lib.add_borrower(borrower)
            print(msg)

        elif choice == '3':
            mid = input("Membership ID: ").strip()
            isbn = input("ISBN: ").strip()
            days = input("Days to borrow (default 14): ").strip() or "14"
            try:
                days_i = int(days)
            except ValueError:
                days_i = 14
            ok, msg = lib.borrow_book(mid, isbn, borrow_days=days_i)
            print(msg)

        elif choice == '4':
            mid = input("Membership ID: ").strip()
            isbn = input("ISBN: ").strip()
            ok, msg = lib.return_book(mid, isbn)
            print(msg)

        elif choice == '5':
            field = input("Search by (title/author/genre/isbn) [title]: ").strip() or "title"
            q = input("Query: ").strip()
            results = lib.search_books(q, field=field)
            if results:
                for b in results:
                    print(b)
            else:
                print("No results found.")

        elif choice == '6':
            for b in lib.list_all_books():
                print(b)

        elif choice == '7':
            mid = input("Membership ID: ").strip()
            ok, data = lib.borrower_status(mid)
            if not ok:
                print(data)
            else:
                if not data:
                    print("No borrowed books.")
                else:
                    for isbn, due in data:
                        print(f"ISBN: {isbn} | Due: {due.strftime('%Y-%m-%d %H:%M:%S')}")

        elif choice == '8':
            overdue = lib.list_overdue()
            if not overdue:
                print("No overdue items.")
            else:
                for borrower, isbn, due, days_over in overdue:
                    print(f"Borrower: {borrower.name} (ID: {borrower.membership_id}) | ISBN: {isbn} | Due: {due.strftime('%Y-%m-%d')} | Days overdue: {days_over}")

        elif choice == '9':
            print("Goodbye.")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
