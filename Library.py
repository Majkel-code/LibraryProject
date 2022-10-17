class Library:

    def __init__(self, books=[], users=[]):
        self.books = books
        self.users = users
        self.registry = {}
        # 'name': status
        # setup()

    def setup(self):
        pass

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
        else:
            print("User with this nickname is already registered!")

        # with open user_file:
        # dopisz nowego goscia

    def add_new_book(self, book_name):
        if book_name not in self.books and self.registry.values() != book_name:
            self.books.append(book_name)
        else:
            print("This book is alredy in Library data base")

        # with open books_file:
        # add new line