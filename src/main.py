import types


class Book:
    def __init__(self, title: str, author: str, isbn: str):
        self.title: str = title
        self.author: str = author
        self.isbn: str = isbn
        self._is_available: bool = True
        self._current_borrower: User = None
        self._waitlist: list[User] = []
        
    def __str__(self) -> str:
        return f"Book: {{ title: {self.title}, author: {self.author}, isbn: {self.isbn}, _is_available: {self._is_available} }}"
    
    def print_waitlist(self) -> None:
        _a = f"{self.title} is waitlisted by"
        for user in self._waitlist:
            _a += f"\n\t{str(user)}"
        print(_a)

    def get_availability(self) -> bool:
        return self._is_available

    def get_current_borrower(self) -> User:
        return self._current_borrower

    def get_waitlist(self) -> list[User]:
        return self._waitlist

    def borrow(self, user: User) -> None:
        if self._is_available:
            self._current_borrower = user
            self._is_available = False
            user.add_borrowed_book(self)
            print(f"{self.title} has been borrowed by {self._current_borrower.name}")
        else:
            self._waitlist.append(user)
            print(f"{self.title} is not available. Adding {user.name} to the waitlist")
            
    def return_book(self, user: User) -> None:
        if (user != self._current_borrower):
            print("cannot return a book you have not reserved")
            return
        
        self._is_available = True
        self._current_borrower.remove_borrowed_book(self)
        # if len(self._waitlist) is 0:
        #     print(f"waitlist is empty {self.title} is now available")
        # else:
        #     self.borrow(self._waitlist.pop(0)) # like a dequeue
        #     print(f"waitlist is not empty {self.title} is now reserved by {self._current_borrower.name}")

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
        
        
class User:
    def __init__(self, name: str):
        self.name: str = name
        self.borrowed_books: list[Book] = []
        
    def __str__(self) -> str:
        return f"User: {{ name: {self.name} }}"
    
    def borrow_book(self, library: Library, book_title: str):
        book = library.get_book(book_title)
        library.borrow_book(book, self)
    
    def return_book(self, library: Library, book_title: str):
        book = library.get_book(book_title)
        library.return_book(book, self)

    def add_borrowed_book(self, book: Book) -> None:
        try:
            self.borrowed_books.index(book)
        except ValueError:
            self.borrowed_books.append(book)
            
    def remove_borrowed_book(self, book: Book) -> None:
        try:
            self.borrowed_books.remove(book)
        except ValueError:
            return
        
    def print_borrowed_books(self) -> None:
        _a = f"{self.name} has borrowed: "
        if len(self.borrowed_books) > 0:
            for book in self.borrowed_books:
                _a += f"\n\t{str(book)}"
        else:
            _a += "\n\tno books"
        print(_a)


class Librarian:
    def manage_return(self, book: Book, user: User) -> None:
        if (book.get_current_borrower() is not user):
            print("you cannot return a book you dont have on load")
            return
        
        book.return_book(user)
        print(f"{book.title} has been returned")
        self.manage_waitlist(book)
            
    def manage_waitlist(self, book: Book) -> None:
        waitlist = book.get_waitlist()
        if len(waitlist) > 0:
            nextB = waitlist.pop(0) # like dequeuing
            print(f"notifying {nextB.name} from the waitlist")
            book.borrow(nextB)
            
        # if len(self._waitlist) is 0:
        #     print(f"waitlist is empty {self.title} is now available")
        # else:
            


class Library:
    def __init__(self, librarian: Librarian):
        self.books: list[Book] = []
        self.users: list[User] = []
        self.librarian: Librarian = librarian

    def add_book(self, book: Book) -> None:
        try:
            self.books.index(book)
        except ValueError:
            self.books.append(book)

    def add_user(self, user: User) -> None:
        try:
            self.users.index(user)
        except ValueError:
            self.users.append(user)
    
    def get_book(self, book_title: str) -> Book:
        return list(filter(lambda book: book.title == book_title, self.books))[0]

    def borrow_book(self, book: Book, user: User) -> None:
        book.borrow(user)
    
    def return_book(self, book: Book, user: User) -> None:
        self.librarian.manage_return(book, user)


def main():
    user1 = User("Alice") 
    user2 = User("Bob")
    user3 = User("Charlie")
    
    users = [
        user1, user2, user3 
    ] 
    books = [
        Book("1984", "George Orwell", "4312"),
        Book("Once Upon a Time", "TE. Simons", "1234"),
        Book("Mary had a little lamb", "Unknown", "4321"),
        Book("Moby Dick", "Herman Melville", "1324"),
    ]
    
    library = Library(Librarian())
    for user in users:
        library.add_user(user)
    for book in books:
        library.add_book(book)
        
    # some manual tests (message simulations)
    # print(library.books)
  
    # print(f"request: {user1.name} is going to reserve {books[0].title}")
    user1.borrow_book(library, books[0].title)
    # user1.print_borrowed_books()
    
    # print(f"request: {user2.name} is going to reserve {books[0].title}")
    user2.borrow_book(library, books[0].title)
    # user2.print_borrowed_books()
    
    user3.borrow_book(library, books[0].title)
    
    # print(f"request: {user2.name} is going to reserve {books[1].title}")
    # user2.borrow_book(library, books[1].title)
    # user2.print_borrowed_books()
    
    # should trigger the waitlist stuff    
    # print(f"request: {user1.name} is going to return {books[0].title}")
    user1.return_book(library, books[0].title)
    # user1.print_borrowed_books()
    
    print(str(books[0]))
    books[0].print_waitlist()
    

if __name__ == "__main__":
    main()

