import json
import os

class Book:
    def __init__(self, book_id, title, author, issued=False):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.issued = issued

    def to_dict(self):
        return {
            "id": self.book_id,
            "title": self.title,
            "author": self.author,
            "issued": self.issued
        }
		
class Library:
    FILE_NAME = "library.json"

    def __init__(self):
        self.books = {}  # dictionary for fast lookup (HashMap-like)
        self.load_data()

    # Load library data from file
    def load_data(self):
        if os.path.exists(self.FILE_NAME):
            try:
                with open(self.FILE_NAME, "r") as file:
                    data = json.load(file)
                    for b in data:
                        book = Book(
                            b["id"], b["title"], b["author"], b["issued"]
                        )
                        self.books[book.book_id] = book
            except json.JSONDecodeError:
                self.books = {}
        else:
            self.books = {}

    # Save data to JSON file
    def save_data(self):
        with open(self.FILE_NAME, "w") as file:
            json.dump([b.to_dict() for b in self.books.values()], file, indent=4)

    # Add book
    def add_book(self, book):
        if book.book_id in self.books:
            print("Error: Book ID already exists")
            return
        self.books[book.book_id] = book
        self.save_data()
        print("Book added successfully")

    # Search by title
    def search_by_title(self, title):
        results = [b for b in self.books.values() if title.lower() in b.title.lower()]
        return results

    # Search by author
    def search_by_author(self, author):
        results = [b for b in self.books.values() if author.lower() in b.author.lower()]
        return results

    # Issue a book
    def issue_book(self, book_id):
        book = self.books.get(book_id)
        if not book:
            print("Book not found")
            return

        if book.issued:
            print("Book already issued")
            return

        book.issued = True
        self.save_data()
        print("Book issued successfully")

    # Return a book
    def return_book(self, book_id):
        book = self.books.get(book_id)
        if not book:
            print("Book not found")
            return

        if not book.issued:
            print("Book is not issued")
            return

        book.issued = False
        self.save_data()
        print("Book returned successfully")

    # Reports
    def total_books(self):
        return len(self.books)

    def issued_count(self):
        return len([b for b in self.books.values() if b.issued])

    # Show all books
    def list_books(self):
        if not self.books:
            print("No books in inventory.")
            return

        print("\n------------- Library Inventory -------------")
        print("{:<10} {:<30} {:<20} {:<10}".format("ID", "Title", "Author", "Status"))
        print("---------------------------------------------------------------")

        for b in self.books.values():
            status = "Issued" if b.issued else "Available"
            print("{:<10} {:<30} {:<20} {:<10}".format(b.book_id, b.title, b.author, status))

        print("---------------------------------------------------------------")

def main():
    library = Library()

    while True:
        print("\n=========== Library Book Inventory Manager ===========")
        print("1. Add Book")
        print("2. Search by Title")
        print("3. Search by Author")
        print("4. Issue Book")
        print("5. Return Book")
        print("6. List All Books")
        print("7. Reports")
        print("8. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            book_id = input("Enter Book ID: ")
            title = input("Enter Title: ")
            author = input("Enter Author: ")
            library.add_book(Book(book_id, title, author))

        elif choice == "2":
            title = input("Enter title to search: ")
            results = library.search_by_title(title)
            if results:
                print("\nSearch Results:")
                for b in results:
                    print(f"{b.book_id} | {b.title} | {b.author} | {'Issued' if b.issued else 'Available'}")
            else:
                print("No books found.")

        elif choice == "3":
            author = input("Enter author to search: ")
            results = library.search_by_author(author)
            if results:
                print("\nSearch Results:")
                for b in results:
                    print(f"{b.book_id} | {b.title} | {b.author} | {'Issued' if b.issued else 'Available'}")
            else:
                print("No books found.")

        elif choice == "4":
            book_id = input("Enter Book ID to Issue: ")
            library.issue_book(book_id)

        elif choice == "5":
            book_id = input("Enter Book ID to Return: ")
            library.return_book(book_id)

        elif choice == "6":
            library.list_books()

        elif choice == "7":
            print("\n----- Reports -----")
            print(f"Total Books: {library.total_books()}")
            print(f"Issued Books: {library.issued_count()}")

        elif choice == "8":
            print("Exiting... Goodbye!")
            break

        else:
            print("Invalid choice! Try again.")

if __name__ == "__main__":
    main()
