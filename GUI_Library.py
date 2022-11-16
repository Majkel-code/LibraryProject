
from Library import Library
from tkinter import *
from tkinter import ttk
from tkinter import messagebox



class GUI_main_page():

    def __init__(self):
        self.lib = Library()
        self.root = Tk()
        self.root.title('Library')
        self.root.geometry("300x300")
        self.root.resizable(0, 0)

        Label(text="Choose Login Or Register", width="300", height="2").pack()
        Label(text="").pack()
        Button(text="Login", height="2", width="30",command=self.login_window).pack()
        Button(text="Register", height="2", width="30", command=self.register_windows).pack()
        mainloop()



    def register_windows(self):
        register_page = Toplevel(self.root)
        register_page.title('Registry')
        register_page.geometry("300x300")
        register_page.resizable(0, 0)

        def register():

            password_info = password.get()
            login_info = login.get()
            if not self.lib.password_available(password_info):
                messagebox.askretrycancel("Error", "Unavailable password!")
            if not self.lib.login_available(login_info):
                if messagebox.askyesno("Error", "User with this Nickname exist, you want to login?"):
                    self.login_window()
                    register_page.destroy()
                else:
                    register_page.destroy()
                    self.register_windows()
            if self.lib.password_available(password_info) and self.lib.login_available(login_info):
                self.lib.register_user(login_info,password_info)
                # Tu raczej custom message box (Nie ma popup'u "PASS")
                messagebox.showwarning("Successful", "User successful register!")
                register_page.destroy()

        Label(register_page, text="Please input your 'Login' and 'Password' below").pack()
        Label(register_page, text="").pack()

        login = StringVar()
        Label(register_page, text="Username:").pack()
        Entry(register_page, textvariable=login).pack()

        password = StringVar()
        Label(register_page, text="Password:").pack()
        Entry(register_page, textvariable=password,show="*").pack()

        Button(register_page, text="Register", height="1", width="15",
               command=register).pack(pady=20)

    def login_window(self):

        login_page = Toplevel(self.root)
        login_page.title('Login window')
        login_page.geometry("300x300")
        login_page.resizable(0, 0)

        def log_in():

            password_info = password.get()
            login_info = login.get()
            if self.lib.user_log_in(login_info,password_info):
                # Tu raczej custom message box (Nie ma popup'u "PASS")
                messagebox.showwarning("Successful", "User successful login!")
                if self.lib.user_log_in(login_info,password_info) == "admin":
                    self.admin_window(login_info)
                    login_page.destroy()
                else:
                    self.user_window(login_info)
                    login_page.destroy()
            else:
                if messagebox.askretrycancel("Error", "Username or password is incorrect, try again!"):
                    login_page.destroy()
                    self.login_window()
                else:
                    login_page.destroy()



        Label(login_page, text="Please input your 'Login' and 'Password' below").pack()
        Label(login_page, text="").pack()

        login = StringVar()
        Label(login_page, text="Username:").pack()
        Entry(login_page, textvariable=login).pack()

        password = StringVar()
        Label(login_page, text="Password:").pack()
        Entry(login_page, textvariable=password, show="*").pack()

        Button(login_page, text="Login", height="1", width="15",
               command=log_in).pack(pady=20)

    def user_window(self,login_info):
        user_interface = Toplevel(self.root)
        user_interface.title(f'Library {login_info}')
        user_interface.geometry("300x300")
        user_interface.resizable(0, 0)

        def borrow():
            if self.lib.available_books_to_borrow():
                borrow_window = Toplevel(self.root)
                borrow_window.title(f'Library {login_info} - Borrow')
                borrow_window.geometry("300x300")
                borrow_window.resizable(0, 0)

                books = self.lib.available_books_to_borrow()

                def on_select(event):
                    def lib_borrow():
                        self.lib.borrow(login_info, selected)
                        if messagebox.askyesno("Borrow next", f"Book successful borrowed. Are you want borrow another?"):
                            borrow_window.destroy()
                            borrow()
                        else:
                            borrow_window.destroy()
                    selected = event.widget.get()
                    label['text'] = f"You want borrow: {selected}?"
                    button = Button(borrow_window, text="Borrow", height="2", width="30", command=lib_borrow).pack()

                combo = ttk.Combobox(borrow_window, values=books)
                combo.pack(pady=10)
                combo.bind('<<ComboboxSelected>>', on_select)
                label = Label(borrow_window)
                label.pack()

            else:
                messagebox.showerror("Borrow Error", f"Oops! We don't have books at this moment. :(")

        def deposit():
            if self.lib.available_books_to_deposit(login_info):
                deposit_window = Toplevel(self.root)
                deposit_window.title(f'Library {login_info} - Deposit')
                deposit_window.geometry("300x300")
                deposit_window.resizable(0, 0)

                books = self.lib.available_books_to_deposit(login_info)

                def on_select(event):
                    def lib_deposit():
                        self.lib.deposit(login_info, selected)
                        if messagebox.askyesno("Deposit next", f"Book successful deposit. Are you want deposit another?"):
                            deposit_window.destroy()
                            deposit()
                        else:
                            deposit_window.destroy()

                    selected = event.widget.get()
                    label['text'] = f"You want deposit: {selected}?"
                    button = Button(deposit_window, text="Deposit", height="2", width="30", command=lib_deposit).pack()


                combo = ttk.Combobox(deposit_window, values=books)
                combo.pack(pady=10)
                combo.bind('<<ComboboxSelected>>', on_select)
                label = Label(deposit_window)
                label.pack()
            else:
                messagebox.showerror("Deposit", f"You don't have book to deposit. Borrow first some books :)")

        def change_password():
            change_password_window = Toplevel(self.root)
            change_password_window.title(f'Library {login_info} - Change password')
            change_password_window.geometry("300x300")
            change_password_window.resizable(0, 0)

            def changing_password():
                old_password_info = old_password.get()
                new_password_info = new_password.get()
                if self.lib.password_available(new_password_info):
                    self.lib.change_password(login_info, old_password_info, new_password_info)
                    if messagebox.showwarning("Successful", "Password successful changed! You need login again."):
                        change_password_window.destroy()
                        user_interface.destroy()
                        self.login_window()

            old_password = StringVar()
            Label(change_password_window, text="Old Password:").pack()
            Entry(change_password_window, textvariable=old_password, show="*").pack()
            new_password = StringVar()
            Label(change_password_window, text="New_Password:").pack()
            Entry(change_password_window, textvariable=new_password, show="*").pack()
            Button(change_password_window, text="Change", height="2", width="30", command=changing_password).pack()

        Label(user_interface, text="Whats you want do?", width="300", height="2").pack()
        Label(user_interface, text="").pack()
        Button(user_interface, text="Borrow", height="2", width="30",command=borrow).pack()
        Button(user_interface, text="Deposit", height="2", width="30",command=deposit).pack()
        Button(user_interface, text="Change Password", height="2", width="30",command=change_password).pack()

    def admin_window(self, login_info):
        admin_interface = Toplevel(self.root)
        admin_interface.title(f'Library {login_info}')
        admin_interface.geometry("300x300")
        admin_interface.resizable(0, 0)

        def add_new_books():
            new_books_window = Toplevel(self.root)
            new_books_window.title(f'Library {login_info} - Add new Books')
            new_books_window.geometry("300x300")
            new_books_window.resizable(0, 0)

            def add_book():
                book_title_info = book_title.get()
                book_author_info = book_author.get()
                book_pages_info = book_pages.get()
                if self.lib.can_be_add(book_title_info):
                    self.lib.add_new_book(book_title_info, book_author_info, book_pages_info)
                    if messagebox.askyesno("Successful", f"Book '{book_title_info}' successful add. Are you want add next?"):
                        new_books_window.destroy()
                        add_new_books()
                    else:
                        new_books_window.destroy()
                else:
                    messagebox.showerror("Error", f"Book '{book_title_info}' is already in Library.")


            book_title = StringVar()
            Label(new_books_window, text="Book Title:").pack()
            Entry(new_books_window, textvariable=book_title).pack()
            book_author = StringVar()
            Label(new_books_window, text="Book Author:").pack()
            Entry(new_books_window, textvariable=book_author).pack()
            book_pages = StringVar()
            Label(new_books_window, text="Pages:").pack()
            Entry(new_books_window, textvariable=book_pages).pack()
            Button(new_books_window, text="Add Book", height="2", width="30",command=add_book).pack()

        def change_users_password():
            psr_manager_window = Toplevel(self.root)
            psr_manager_window.title(f'Library {login_info} - Passwords manager')
            psr_manager_window.geometry("300x300")
            psr_manager_window.resizable(0, 0)

            def change_password():
                user_name_info = user_name.get()
                old_password_info = old_password.get()
                new_password_info = new_password.get()
                if self.lib.password_available(new_password_info):
                    self.lib.change_password(user_name_info, old_password_info, new_password_info)
                    if messagebox.showwarning("Successful", f"Password for user:'{user_name_info}' successful changed!"):
                        psr_manager_window.destroy()

            user_name = StringVar()
            Label(psr_manager_window, text="Username:").pack()
            Entry(psr_manager_window, textvariable=user_name).pack()
            old_password = StringVar()
            Label(psr_manager_window, text="Old Password:").pack()
            Entry(psr_manager_window, textvariable=old_password).pack()
            new_password = StringVar()
            Label(psr_manager_window, text="New Password:").pack()
            Entry(psr_manager_window, textvariable=new_password).pack()
            Button(psr_manager_window, text="Confirm", height="2", width="30",command=change_password).pack()

        Label(admin_interface, text="Whats you want do?", width="300", height="2").pack()
        Label(admin_interface, text="").pack()
        Button(admin_interface, text="Add Books", height="2", width="30",command=add_new_books).pack()
        Button(admin_interface, text="Password Manager", height="2", width="30",command=change_users_password).pack()



GUI_main_page()
