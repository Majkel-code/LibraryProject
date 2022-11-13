from libraryGUI import Library
from tkinter import *


class GUI_main_page():

    def __init__(self):
        self.lib = Library()
        self.root = Tk()
        self.root.title('Library')
        self.root.geometry("300x300")
        self.root.resizable(0, 0)

        Label(text="Choose Login Or Register", width="300", height="2").pack()
        Label(text="").pack()
        Button(text="Login", height="2", width="30").pack()
        Button(text="Register", height="2", width="30", command=self.register_windows).pack()
        mainloop()

    def destroy_windows(self,window_name):
        window_name.destroy()


    def register_windows(self):
        register_page = Toplevel(self.root)
        register_page.title('Registry')
        register_page.geometry("300x300")
        register_page.resizable(0, 0)

        def register():


            def message(info_return):
                popup = Toplevel(register_page)
                popup.geometry("150x50")
                popup.resizable(0, 0)
                if info_return == "PE":
                    Label(popup, text="Unavailable password!", bg="red").pack()
                elif info_return == "LE":
                    Label(popup, text="Unavailable Username!", bg="red").pack()
                elif info_return == "Pass":
                    Label(popup, text="User successful register!", bg="green").pack()


            password_info = password.get()
            login_info = login.get()
            if not self.lib.password_available(password_info):
                message("PE")
            if not self.lib.login_available(login_info):
                message("LE")
            if self.lib.password_available(password_info) and self.lib.login_available(login_info):
                self.lib.register_user(login_info,password_info)
                message("Pass")

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



GUI_main_page()
