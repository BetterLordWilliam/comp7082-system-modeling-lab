import types


class User:
    def __init__(self, name: str):
        self._name: str = name
        self._borrowed_books: list[Book] = []

    def get_name(self) -> str:
        return self._name
    
    def get_borrowed_books(self) -> list[Book]:
        return self._borrowed_books
    
    def add_borrowed_book(self, book: Book) -> None:
        try:
            self._borrowed_books.index(book)
        except ValueError:
            self._borrowed_books.append(book)
            
    def remove_borrowed_booK(self, book: Book) -> None:
        try:
            self._borrowed_books.remove(book)
        except ValueError:
            return
        
    def print_borrowed_books(self) -> None:
        _a = f"{self._name} has borrowed: "
        if len(self._borrowed_books) > 0:
            for book in self._borrowed_books:
                _a += f"\n\t{str(book)}"
        else:
            _a += "\n\tno books"
        print(_a)
    
    def __str__(self) -> str:
        return f"User: {{ _name: {self._name} }}"


class Library:
    def __init__(self):
        self._books: list[Book] = []
        self._users: list[User] = []
        self._librarian: Librarian = Librarian("Heather")

    def add_book(self, book: Book) -> None:
        self._books.append(book)

    def get_books(self) -> list[Book]:
        return self._books

    def reservation_request(self, book: Book, user: User) -> None:
        self._librarian.process_reservation(book, user)
    
    def return_request(self, book: Book, user: User) -> None:
        self._librarian.process_return(book, user)


class Book:
    def __init__(self, title: str, author: str, isbn: str):
        self._title: str = title
        self._author: str = author
        self._isbn: str = isbn
        self._is_available: bool = True
        self._reserved_by: User = None
        self._waitlist: list[User] = []
        
    def __str__(self) -> str:
        return f"Book: {{ _title: {self._title}, _author: {self._author}, _isbn: {self._isbn}, _is_available: {self._is_available} }}"

    def get_title(self) -> str:
        return self._title

    def get_author(self) -> str:
        return self._author

    def get_isbn(self) -> str:
        return self._isbn
    
    def get_availability(self) -> bool:
        return self._is_available

    def get_reserved_by(self) -> User:
        return self._reserved_by

    def get_waitlist(self) -> list[User]:
        return self._waitlist

    def set_reserved_by(self, user: User) -> bool:
        if self._is_available:
            self._reserved_by = user
            self._is_available = False
            user.add_borrowed_book(self)
            print(f"{user.get_name()} borrowed book {self._title}")
            return True
        else:
            self._waitlist.append(user)
            print(f"{user.get_name()} added to book {self._title} waitlist")
            return False
            
    def unreserve(self, user: User) -> None:
        if (user != self._reserved_by):
            print("cannot return a book you have not reserved")
            return
        
        self._is_available = True
        self._reserved_by.remove_borrowed_booK(self)
        if len(self._waitlist) is 0:
            print(f"waitlist is empty {self._title} is now available")
        else:
            self.set_reserved_by(self._waitlist.pop(0)) # like a dequeue
            print(f"waitlist is not empty {self._title} is now reserved by {self._reserved_by.get_name()}")

    def add_to_waitlist(self, user: User) -> None:
        try:
            # dont add the same user more than once
            self._waitlist.index(user)
        except ValueError:
            self._waitlist.append(user)
            
    def remove_from_waitlist(self, user: User) -> None:
        try:
            self._waitlist.remove(user)
        except ValueError:
            return


class Librarian:
    def __init__(self, name: str):
        self._name: str = name

    def get_name(self):
        return self._name

    def process_reservation(self, book: Book, user: User) -> None:
        if (book.get_availability()):
            book.set_reserved_by(user)
            print(f"enjoy the book {user.get_name()}!")
        else:
            book.add_to_waitlist(user)
            print(f"sorry {user.get_name()} you were waitlisted")
    
    def process_return(self, book: Book, user: User) -> None:
        if (book.get_reserved_by() is user):
            book.unreserve(user)
            print(f"thanks for returning {book.get_title()} {user.get_name()}")
        else:
            print(f"{user.get_name()} you cannot return a book you don't own")


def main():
    print("Hello from system-modeling!")
    
    user1 = User("Joe Schmoe") 
    user2 = User("Anthony Park")
    
    books = [
        Book("Once Upon a Time", "TE. Simons", "1234"),
        Book("Mary had a little lamb", "Unknown", "4321"),
        Book("Moby Dick", "Herman Melville", "4312"),
        Book("1984", "George Orwell", "4312"),
        Book("1984", "George Orwell", "4312"),
    ]
    
    library = Library()
    for book in books:
        library.add_book(book)
    
    # users sending requests to library
    # if this were a proper system, there would be a session or something which would have the 
    # current users object ready to go for these messages (or their id so that a backend
    # could query their user object or something of that nature)
    
    
    # some manual tests (message simulations)
    
    print(library.get_books())
  
    print(f"request: {user1.get_name()} is going to reserve {books[0].get_title()}")
    library.reservation_request(books[0], user1)
    user1.print_borrowed_books()
    
    print(f"request: {user2.get_name()} is going to reserve {books[0].get_title()}")
    library.reservation_request(books[0], user2)
    user2.print_borrowed_books()
    
    print(f"request: {user2.get_name()} is going to reserve {books[1].get_title()}")
    library.reservation_request(books[1], user2)
    user2.print_borrowed_books()
    
    print(f"request: {user1.get_name()} is going to return {books[0].get_title()}")
    library.return_request(books[0], user1)
    user2.print_borrowed_books()


if __name__ == "__main__":
    main()

