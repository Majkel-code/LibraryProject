import os
import json
import requests

url = "https://wolnelektury.pl/api/books/?format=json"
response = requests.get(f"{url}")
data = response.json()

class Library:
    def __init__(self):
        self.database = {"books": [], "users": [{"login": "admin", "password": "admin"}], "registry": []}
        self.load_books()
        self.setup()

    def load_books(self):
        # API can return ~6000 books, for this project i take only 60 of them to test it.
        for book in data[:60]:
            self.database["books"].append({"title": book['title'], "author": book['author'], "genre": book['genre'], "borrow": "No"})


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

    def available_books_to_borrow(self):
        books = []
        print("Books available to borrow:")
        for i in self.database["books"]:
            if i["borrow"] == "No":
                print(i["title"])
                books.append(i["title"])
            else:
                pass
        return books

    def borrow(self, user,books_to_borrow):
        for book in books_to_borrow:
            for i in self.database["books"]:
                if i["title"] == book:
                    i["borrow"] = "Yes"
                    self.open_json_file()
                    self.database['registry'].append({'user': user, 'book': book})
                    self.open_json_file()
                    print(f"{user} just borrow book: {book}")

    def available_books_to_deposit(self, user):
        books = []
        print("Books available to deposit:")
        for i in self.database["registry"]:
            if i["user"] == user:
                print(i["book"])
                books.append(i["book"])
            else:
                pass
        return books

    def deposit(self, user, book):
        for i in self.database["registry"]:
            if i["book"] == book:
                self.database["registry"].remove(i)
        for b in self.database["books"]:
            if b["title"] == book:
                b["borrow"] = "No"
        self.open_json_file()
        print(f"{user} just deposit book: {book}")

    def user_log_in(self, login, password):
        if login != "" and password != "":
            for user in self.database["users"]:
                if login == user["login"] and password == user["password"]:
                    if login == "admin" and password == "admin":
                        return "admin"
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

    def change_password(self,user_name, old_user_password,new_password):
        for user in self.database["users"]:
            if user["login"] == user_name:
                if user["password"] == old_user_password:
                    user["password"] = new_password
                    self.open_json_file()
                    return True

    def register_user(self,user_name,user_password):
        if self.login_available(user_name) and self.password_available(user_password):
            self.database["users"].append({"login": user_name, "password": user_password})
            self.open_json_file()
            print(self.database)
            return True

    def can_be_add(self, book):
        for i in self.database["books"]:
            if i["title"] == book:
                return False
        return True

    def add_new_book(self,book_title,book_author,book_genre):
                self.database['books'].append({"title": book_title, "author": book_author, "genre": book_genre, "borrow": "No"})
                print(self.database)
                self.open_json_file()
                print(f"Title:'{book_title}', Author:'{book_author}', genre:'{book_genre}' - successful added to Library")


