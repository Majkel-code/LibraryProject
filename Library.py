import os
class Library:

    def __init__(self):
        self.books = []
        self.users = []
        self.registry = []


    def setup(self):
        # warunek powinien być oddzielnie dla userów i książek
        cwd = os.getcwd()
        if os.path.exists(f"{cwd}\\books.txt") and os.path.exists(f"{cwd}\\users.txt"):
            print("Library successful loaded! ")
            # zawsze używaj 'with open' !
            # a jak już musisz open to pamiętaj o close
            self.books = open("books.txt").read().split()
            # PRINT TESTOWY!!!
            print(self.books)
            self.users = open("users.txt").read().split()
            # PRINT TESTOWY!!!
            print(self.users)
            # U mnie wysypało sie na registry :(
            self.registry = open("registry.txt").read().split()
            # PRINT TESTOWY!!!
            print(self.registry)

        else:
            print("Missing some database, Creating new one... ")
            open("books.txt", "a")
            open("users.txt", "a")
            open("registry.txt", "a")
            self.setup()

    # sprawdz czy pliki books.txt i users.txt istnieją w folderze x
    # jesli tak to zczytaj books i users do atrybutów
    # jesli nie to komunikat, biblioteka pusta

    def borrow(self, user, password, book):
        # jeśli pole users byłoby słownikiem łatiwej byłoby o dostęp po kluczach 'login' , 'password'
        # zamiast szukać jakiś indexów dziwnych
        if user in self.users and self.users[int(self.users.index(user) + 1)] == password:
            if self.available_books(book):
                # tak samo rejestr, lepiej żeby to byl dict
                self.registry.append(f"{user}={book}")
                with open("registry.txt","a") as f:
                    f.write(f"{user}={book}\n")
                self.books.remove(book)
                self.books.append(f"{book}Taken")# ??
                with open("books.txt", "r+") as f:#??
                    file_data = f.read()
                    file_data = file_data.replace(book, f"{book}Taken")
                    with open("books.txt", "w") as f: # :O ??
                        f.write(file_data)
                print(f"{user} just borrow book: {book}")
        else:
            print("Invalid inputs! ")

    def deposit(self, user, password, book):
        if user in self.users and self.users[int(self.users.index(user)+1)] == password and f"{user}={book}" in self.registry:
            self.books.remove(f"{book}Taken")
            self.books.append(book)
            with open("books.txt", "r") as f:
                file_data = f.read()
                file_data = file_data.replace(f"{book}Taken", book)
                with open("books.txt", "w") as f:
                    f.write(file_data)
            self.registry.remove(f"{user}={book}")
            with open("registry.txt", "r") as f:
                file_data = f.read()
                file_data = file_data.replace(f"{user}={book}", "")
                with open("registry.txt", "w") as f:
                    f.write(file_data)
            print(f"{user} just deposit book: {book}")
        else:
            # Albo hasło jest nieprawidłowe
            print(f"{user} do not have book: {book}")

    def available_books(self, book):
        if book in self.books:
            return True
        else:
            print("This book is already borrowed!")
            return False

    def register_user(self, user_name, user_password):
        if user_name not in self.users and user_password not in self.users:
            self.users.append(user_name)
            self.users.append(user_password)
            with open("users.txt", "a") as f:
                f.write(f"{user_name}\n")
                f.write(f"{user_password}\n")
            print(f"User '{user_name}' successful added to user database")
            return
        else:
            if user_name in self.users:
                user_name = input(f"'{user_name}' is taken. Try Again! ")
                self.register_user(user_name, user_password)
            elif user_password in self.users:
                user_password = input(f"'{user_password}' is taken. Try again: ")
                self.register_user(user_name, user_password)


    def add_new_book(self):
        # Info jak wyjść z tej petli w input message
        book_name = input("Input book title (CamelCase): ")
        while book_name.lower() != "x":
            if f"{book_name}Taken" not in self.books and book_name not in self.books and " " not in book_name:
                self.books.append(book_name)
                with open("books.txt", "a") as f:
                    f.write(f"{book_name}\n")
                print(f"Book '{book_name}' successful added to library! ")
                self.add_new_book()
            else:
                print(f"This book '{book_name}' is alredy in Library or have invalid title")
                self.add_new_book()
            break


lib = Library()
# można tu zmienić na current_working_directory żeby działało każdemu od razu
#path = "C:\\Users\\orokitax\\python-mentoring\\PytonMentoring"
path = os.getcwd()
lib.setup()
while True:
    choice = input("r = register / a = add new book / d = deposit / b = borrow / e = END ")
    if choice == "a":
        lib.add_new_book()
    elif choice == "r":
        user_name = input("Input username: ")
        user_password = input("Input password: ")
        lib.register_user(user_name, user_password)
    elif choice == "b":
        lib.borrow(user=input("Input username: "),password=input("Input user password: "), book=input("Input book title to borrow: "))
    elif choice == "d":
        lib.deposit(user=input("Input username: "), password=input("Input user password: "),
                   book=input("Input book title to deposit: "))
    elif choice == "e":
        break

print(f"Print bazy ksiazek na koniec {lib.books}")
print(f"Print bazy user'ow na koniec {lib.users}")
print(f"Print rejestru na koniec {lib.registry}")
