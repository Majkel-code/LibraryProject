import os
class Library:

    def __init__(self):
        self.books = []
        self.users = []
        self.registry = {}


    def setup(self, path):
        if os.path.exists("C:/Users/micha/Documents/Python/PytonMentoring/books.txt") and os.path.exists("C:/Users/micha/Documents/Python/PytonMentoring/users.txt"):
            print("Library successful loaded! ")
            self.books = open("books.txt").read().split()
            print(self.books)
            self.users = open("users.txt").read().split()
            print(self.users)

        else:
            print("Library doesn't exist! ")

    # sprawdz czy pliki books.txt i users.txt istnieją w folderze x
    # jesli tak to zczytaj books i users do atrybutów
    # jesli nie to komunikat, biblioteka pusta

    def borrow(self, user, book):
        if self.available_books(book):
            self.registry[user] = book
            self.books.remove(book)
            print(f"{user} just borrow book: {book}")

    def deposit(self, user, book):
        if self.registry[user] == book:
            self.registry[user] = ""
            self.books.append(book)
            print(f"{user} just deposit book: {book}")
        else:
            print(f"{user} do not have book: {book}")

    def available_books(self, book):
        if book in self.books:
            return True
        else:
            print("This book is already borrowed!")
            return False

    def register_user(self, user_name):
        if user_name not in self.users:
            self.users.append(user_name)
            with open("users.txt", "a") as f:
                f.write(f"{user_name}\n")
            print(f"User '{user_name}' successful added to user database")
            return
        else:
            user_name = input(f"'{user_name}' is taken. Try Again! ")
            self.register_user(user_name)

        # with open user_file:
        # dopisz nowego goscia

    def add_new_book(self, book_name):
        if book_name not in self.books and self.registry.values() != book_name:
            self.books.append(book_name)
            with open("books.txt", "a") as f:
                f.write(f"{book_name}\n")
            print(f"Book '{book_name}' successful added to library! ")
        else:
            print(f"This book '{book_name}' is alredy in Library data base")

        # with open books_file:
        # add new line

lib = Library()
path = "C:/Users/micha/Documents/Python/PytonMentoring"
lib.setup(path)
lib.add_new_book("Book1")
lib.register_user("Michal")

print(lib.users)
print(lib.books)
