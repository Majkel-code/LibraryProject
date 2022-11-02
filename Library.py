import os
import json
class Library:

    def __init__(self):
        self.books = {"books": {}}
        self.users = {"users": {}}
        self.registry = {"registry": {}}


    def setup(self):
        cwd = os.getcwd()
        if os.path.exists(f"{cwd}\\books.json"):
            with open("books.json", "r") as f:
                self.books = json.load(f)
        else:
            with open("books.json", "a") as f:
                f.write(json.dumps(self.books))

        if os.path.exists(f"{cwd}\\users.json"):
            with open("users.json", "r") as f:
                self.users = json.load(f)
        else:
            with open("users.json", "a") as f:
                f.write(json.dumps(self.users))

        if os.path.exists(f"{cwd}\\registry.json"):
            with open("registry.json", "r") as f:
                self.registry = json.load(f)
        else:
            with open("registry.json", "a") as f:
                f.write(json.dumps(self.registry))
        print("Library successful loaded! ")
        print(self.books)
        print(self.users)
        print(self.registry)

    def borrow(self, user, password, book):
        if user in self.users["users"] and password in self.users["users"][user]:
            if self.available_books(book):
                self.books["books"][book].append("BORROWED")
                with open("books.json", "w") as f:
                    f.write(json.dumps(self.books))
                self.registry['registry'].update({user: book})
                with open("registry.json", "w") as f:
                    f.write(json.dumps(self.registry))
                    print(f"{user} just borrow book: {book}")
            else:
                print(f"{user} do not have book: {book}")
        else:
            print(f"Username or password is incorrect, Try again ")

    def deposit(self, user, password, book):
        if user in self.users["users"] and password in self.users["users"][user]:
            if user in self.registry["registry"] and book in self.registry["registry"][user]:
                self.books["books"][book].remove("BORROWED")
                with open("books.json", "w") as f:
                    f.write(json.dumps(self.books))
                self.registry['registry'].update({user: ""})
                with open("registry.json", "w") as f:
                    f.write(json.dumps(self.registry))
                print(f"{user} just deposit book: {book}")
            else:
                print(f"{user} do not have book: {book}")
        else:
            print(f"Username or password is incorrect, Try again ")

    def available_books(self, book):
        if book in self.books["books"] and "BORROWED" not in self.books["books"][book]:
            return True
        else:
            print("This book is already borrowed!")
            return False

    def password_available(self,user_password):
        for i in self.users["users"]:
            if self.users["users"][i] == user_password:
                return False
        return True

    def register_user(self, user_name, user_password):
        if user_name not in self.users["users"] and self.password_available(user_password):
            self.users["users"].update({user_name: user_password})
            with open("users.json", "w") as f:
                f.write(json.dumps(self.users))
            print("User successful register! ")
            print(self.users)
        else:
            if user_name in self.users["users"]:
                user_name = input(f"'{user_name}' is taken. Try Again! ")
                self.register_user(user_name, user_password)
            elif not self.password_available(user_password):
                user_password = input(f"'{user_password}' is taken. Try again: ")
                self.register_user(user_name, user_password)


    def add_new_book(self):
        book_name = input("Input book title (CamelCase): -to close input 'x'  ")
        while book_name.lower() != "x":
            if book_name not in self.books["books"]:
                book_author = input("Input book Author: ")
                book_pages = input("Input book pages: ")
                self.books['books'].update({book_name: [book_author, book_pages]})
                with open("books.json", "w") as f:
                    f.write(json.dumps(self.books))
                print(f"Title:'{book_name}', Author:'{book_author}', pages:'{book_pages}' - successful added to Library")
                self.add_new_book()
            else:
                print(f"This book '{book_name}' is alredy in Library or have invalid title")
                self.add_new_book()
            break


lib = Library()
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
