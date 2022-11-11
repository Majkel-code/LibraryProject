import os
import json


class Library:
    def __init__(self):
        self.database = {"books": [], "users": [{"login": "admin", "password": "admin"}], "registry": []}
        self.setup()

    def setup(self):
        cwd = os.getcwd()
        if os.path.exists(f"{cwd}\\database.json"):
            print("Library successful loaded! ")
            with open("database.json", "r") as f:
                self.database = json.load(f)
            print(self.database)
        else:
            with open("database.json", "a") as f:
                f.write(json.dumps(self.database))
                print(self.database)
                print(type(self.database))
        print(self.database["users"])

    def open_json_file(self):
        with open("database.json", "w") as f:
            f.write(json.dumps(self.database))

    def available_books_to_borrow(self, books):
        print("Books available to borrow:")
        for i in self.database["books"]:
            if i["borrow"] == "No":
                print(i["title"])
                books.append(i["title"])
            else:
                pass
        return books

    def borrow(self, user):
        books = []
        if self.available_books_to_borrow(books):
            book = input("Which book you want to borrow: ")
            for i in self.database["books"]:
                if i["title"] == book:
                    i["borrow"] = "Yes"
                    self.open_json_file()
                    self.database['registry'].append({'user': user, 'book': book})
                    self.open_json_file()
                    print(f"{user} just borrow book: {book}")
        else:
            print("Library is empty, 'admin' should deliver new books or wait maybe some user will return book :) ")

    def available_books_to_deposit(self, user, books):
        print("Books available to deposit:")
        for i in self.database["registry"]:
            if i["user"] == user:
                print(i["book"])
                books.append(i["book"])
            else:
                pass
        return books

    def deposit(self, user):
        books = []
        if self.available_books_to_deposit(user, books):
            book = input("Which book you want to return: ")
            if book in books:
                for i in self.database["registry"]:
                    if i["book"] == book:
                        self.database["registry"].remove(i)
                for b in self.database["books"]:
                    if b["title"] == book:
                        b["borrow"] = "No"
                self.open_json_file()
                print(f"{user} just deposit book: {book}")
            else:
                print(f"You don't have book: {book}")
                book = input("Which book you want to return: ")
                self.deposit(user)
        else:
            print("You don't have any book, please borrow some first :) ")

    def user_log_in(self, login, password):
        if login != "" and password != "":
            for user in self.database["users"]:
                if login == user["login"] and password == user["password"]:
                    return True
            return False

    def password_available(self, user_password):
        for user in self.database["users"]:
            if user["password"] == user_password:
                return False
        return True

    def login_available(self, user_name):
        for user in self.database["users"]:
            if user["login"] == user_name:
                return False
        return True

    def register_user(self, user_name, user_password):
        if self.login_available(user_name) and self.password_available(user_password):
            self.database["users"].append({"login": user_name, "password": user_password})
            self.open_json_file()
            print("User successful register! ")
            print(self.database)
        else:
            if not self.login_available(user_name):
                user_name = input(f"'{user_name}' is taken. Try again: ")
                self.register_user(user_name, user_password)
            elif not self.password_available(user_password):
                user_password = input(f"'{user_password}' is taken. Try again: ")

                self.register_user(user_name, user_password)

    def can_be_add(self, book):
        for i in self.database["books"]:
            if i["title"] == book:
                return False
        return True

    def add_new_book(self):
        book_name = input("Input book title: -to close input 'x' ")
        while book_name.lower() != "x":
            if self.can_be_add(book_name):
                book_author = input("Input book Author: ")
                book_pages = input("Input book pages: ")

                self.database['books'].append({"title": book_name, "author": book_author, "pages": book_pages, "borrow": "No"})
                print(self.database)
                self.open_json_file()

                print(f"Title:'{book_name}', Author:'{book_author}', pages:'{book_pages}' - successful added to Library")

                self.add_new_book()
            else:
                print(f"This book '{book_name}' is already in Library or have invalid title")
                self.add_new_book()
            break


lib = Library()
while True:
    log_in = input("Login = l / Register = r ").lower()
    if log_in == "l":
        login = input("Input username: ")
        password = input("Input user password: ")
        if lib.user_log_in(login, password):
            while True:
                choice = input(" a = add new book (only admin) / d = deposit / b = borrow / e = Logout ")
                if choice == "a" and login == "admin" and password == "admin":
                    lib.add_new_book()
                elif choice == "a" and login != "admin" and password != "admin":
                    print("This function is only for Administrator! ")
                elif choice == "b":
                    lib.borrow(login)
                elif choice == "d":
                    lib.deposit(login)
                elif choice == "e":
                    break
    elif log_in == "r":
        user_name = input("Input username: ")
        user_password = input("Input password: ")
        if user_name.isalnum() and user_password.isalnum():
            lib.register_user(user_name, user_password)
        else:
            print("Username or password is invalid!")
