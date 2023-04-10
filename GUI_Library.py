from Library import Library
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

WINDOW_SIZE = "500x500"
width = 600
height = 600
RESIZABLE_WINDOW = {
	"y": 0,
	"x": 0
}


class GuiImainPage:

	def __init__(self):
		self.root = Tk()
		self.lib = Library()
		self.MAIN_PAGE()

	def MAIN_PAGE(self):
		self.root.title('Library')
		Label(self.root, text="Choose Login Or Register", height="2").pack()
		Label(self.root, text="").pack()
		Button(self.root, text="Login", height="2", width="30", command=self.login_window).pack()
		Button(self.root, text="Register", height="2", width="30", command=self.register_windows).pack()
		self.CONFIGURE_GUI(self.root, None, None)
		self.root.mainloop()

	def CONFIGURE_GUI(self, page, to_return, interface):
		page.geometry(f"{width}x{height}")
		page.resizable(RESIZABLE_WINDOW["y"], RESIZABLE_WINDOW["x"])
		if page == self.root:
			Button(page, text="CLOSE", height="1", width="15",
				   command=lambda: self.DESTROY_PAGE(destroy_page=page, return_page=to_return)) \
				.pack(side=BOTTOM, pady=20)
		elif interface:
			pass
		else:
			Button(page, text="Return", height="1", width="15",
				   command=lambda: self.DESTROY_PAGE(destroy_page=page, return_page=to_return)) \
				.pack(side=BOTTOM, pady=10)

	# def SET_IMAGE(self):
	# 	image = Image.open('bookImage.png')
	# 	my_image = image.resize((height, width))
	# 	self.bg = ImageTk.PhotoImage(my_image)
	# 	self.bg_label = Label(self.root, image=self.bg)
	# 	self.bg_label.place(x=0, y=0, relwidth=1,relheight=1)

	def DESTROY_PAGE(self, destroy_page, return_page):
		destroy_page.destroy()
		return_page.wm_deiconify()

	def register_windows(self):
		register_page = Toplevel(self.root)
		self.root.withdraw()
		self.CONFIGURE_GUI(register_page, self.root, None)
		register_page.title('Registry')

		def register():
			password_info = reg_password.get()
			login_info = reg_login.get()
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
				self.lib.register_user(login_info, password_info)
				# Tu raczej custom message box (Nie ma popup'u "PASS")
				messagebox.showwarning("Successful", "User successful register!")
				self.DESTROY_PAGE(register_page, self.root)

		Label(register_page, text="Please input your 'Login' and 'Password' below").pack()
		Label(register_page, text="").pack()

		reg_login = StringVar()
		Label(register_page, text="Username:").pack()
		Entry(register_page, textvariable=reg_login).pack()

		reg_password = StringVar()
		Label(register_page, text="Password:").pack()
		Entry(register_page, textvariable=reg_password, show="*").pack()

		Button(register_page, text="Register", height="1", width="15",
			   command=register).pack(pady=20)

	# Button(register_page, text="return", height="1", width="15",
	#        command=lambda:self.DESTROY_PAGE(destroy_page=register_page,return_page=self.root)).pack(pady=20)

	def login_window(self):
		login_page = Toplevel(self.root)
		self.root.withdraw()
		self.CONFIGURE_GUI(login_page, self.root, None)
		login_page.title('Login window')

		def log_in():
			password_info = log_password.get()
			login_info = log_login.get()
			print(login_info)
			print(password_info)
			if self.lib.user_log_in(login_info, password_info):
				# Tu raczej custom message box (Nie ma popup'u "PASS")
				messagebox.showwarning("Successful", "User successful login!")
				if self.lib.user_log_in(login_info, password_info) == "admin":
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

		log_login = StringVar()
		Label(login_page, text="Username:").pack()
		Entry(login_page, textvariable=log_login).pack()

		log_password = StringVar()
		Label(login_page, text="Password:").pack()
		Entry(login_page, textvariable=log_password, show="*").pack()

		Button(login_page, text="Login", height="1", width="15",
			   command=log_in).pack(pady=20)

	def user_window(self, login_info):
		user_interface = Toplevel(self.root)
		self.root.withdraw()
		self.CONFIGURE_GUI(user_interface, self.root, True)
		user_interface.title(f'Library {login_info}')

		def borrow():
			if self.lib.available_books_to_borrow():
				borrow_window = Toplevel(user_interface)
				user_interface.withdraw()
				self.CONFIGURE_GUI(borrow_window, user_interface, None)
				borrow_window.title(f'Library {login_info} - Borrow')
				books = self.lib.available_books_to_borrow()
				self.books_index = 0
				self.actual_page_focus = 0
				page_focus = {
					0: 15,
					1: 30,
					2: 45,
					3: 60
				}
				check_button_objects = []
				self.books_list = []

				def borrow_books():
					selected_books = []
					for i in range(1, 15):
						if globals()[f"var{i}"].get():
							selected_books.append(self.books_list[i - 1])
					if selected_books:
						self.lib.borrow(login_info, selected_books)
						if messagebox.askyesno("Borrow next",
											   f"Book successful Borrowed. Are you want Borrow another?"):
							borrow_window.destroy()
							borrow()
						else:
							borrow_window.destroy()
							user_interface.wm_deiconify()

				Label(borrow_window, height=2, width=30,
					  text="Select books to borrow",
					  font=("Arial", 15)).pack(anchor=N)

				def displayed_books(book_start_iteration, focused_page):
					self.books_list = [book for book in books[book_start_iteration:page_focus[focused_page]]]
					if not check_button_objects:
						for i in range(0, 15):
							globals()[f"var{i}"] = IntVar()
							globals()[f"c{i}"] = ttk.Checkbutton(borrow_window,
																 variable=globals()[f"var{i}"],
																 text=self.books_list[i - 1],
																 onvalue=1)
							globals()[f"c{i}"].pack(anchor=W, padx=15)
							check_button_objects.append(globals()[f"c{i}"])
					else:
						for i in range(0, 15):
							globals()[f"c{i}"].config(text=self.books_list[i - 1])

				displayed_books(0, 0)

				def change_page(next_prev_info):
					if next_prev_info == "next":
						if self.actual_page_focus + 1 in page_focus:
							self.actual_page_focus += 1
							self.books_index += 15
							displayed_books(self.books_index, self.actual_page_focus)
						else:
							messagebox.showwarning("Error", "There is no more pages at the moment!")
					elif next_prev_info == "prev":
						if self.actual_page_focus - 1 in page_focus:
							self.actual_page_focus -= 1
							self.books_index -= 15
							displayed_books(self.books_index, self.actual_page_focus)
						else:
							messagebox.showwarning("Error", "You're on first page")

				label = Label(borrow_window, height=2, width=30)
				label.pack()
				button = Button(borrow_window, text="Borrow", command=borrow_books, height="2", width="30")
				button.pack()
				Button(borrow_window, text="Next Page", height="1", width="15",
					   command=lambda: change_page("next")).pack(side=RIGHT)
				Button(borrow_window, text="Prev Page", height="1", width="15",
					   command=lambda: change_page("prev")).pack(side=LEFT)
			else:
				messagebox.showerror("Borrow Error", f"Oops! We don't have books at this moment. :(")

		def deposit():
			if self.lib.available_books_to_deposit(login_info):
				deposit_window = Toplevel(user_interface)
				user_interface.withdraw()
				self.CONFIGURE_GUI(deposit_window, user_interface, None)
				deposit_window.title(f'Library {login_info} - Deposit')
				books = self.lib.available_books_to_deposit(login_info)

				def on_select(event):
					def lib_deposit():
						self.lib.deposit(login_info, selected)
						if messagebox.askyesno("Deposit next",
											   f"Book successful deposit. Are you want deposit another?"):
							deposit_window.destroy()
							deposit()
						else:
							deposit_window.destroy()
							user_interface.wm_deiconify()

					selected = event.widget.get()
					label['text'] = f"You want deposit: {selected}?"
					button['command'] = lib_deposit

				combo = ttk.Combobox(deposit_window, values=books)
				combo.pack(pady=10)
				combo.bind('<<ComboboxSelected>>', on_select)
				label = Label(deposit_window)
				label.pack()
				button = Button(deposit_window, text="Borrow", height="2", width="30")
				button.pack()
			else:
				messagebox.showerror("Deposit", f"You don't have book to deposit. Borrow first some books :)")

		# Button(deposit_window, text="return", height="1", width="15",
		#        command=lambda:self.DESTROY_PAGE(destroy_page=deposit_window,return_page=user_interface)).pack(pady=20)

		def change_password():
			change_password_window = Toplevel(user_interface)
			user_interface.withdraw()
			self.CONFIGURE_GUI(change_password_window, user_interface, None)
			change_password_window.title(f'Library {login_info} - Change password')

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

		# Button(change_password_window, text="return", height="1", width="15",
		#        command=lambda:self.DESTROY_PAGE(destroy_page=change_password_window,return_page=user_interface)).pack(pady=20)

		Label(user_interface, text="Whats you want do?", width="300", height="2").pack()
		Label(user_interface, text="").pack()
		Button(user_interface, text="Borrow", height="2", width="30", command=borrow).pack()
		Button(user_interface, text="Deposit", height="2", width="30", command=deposit).pack()
		Button(user_interface, text="Change Password", height="2", width="30", command=change_password).pack()
		Button(user_interface, text="LOGOUT", height="1", width="15",
			   command=lambda: self.DESTROY_PAGE(destroy_page=user_interface, return_page=self.root)) \
			.pack(pady=20)

	def admin_window(self, login_info):
		admin_interface = Toplevel(self.root)
		self.root.withdraw()
		self.CONFIGURE_GUI(admin_interface, self.root, True)
		admin_interface.title(f'Library {login_info}')

		def add_new_books():
			new_books_window = Toplevel(admin_interface)
			admin_interface.withdraw()
			self.CONFIGURE_GUI(new_books_window, admin_interface, None)
			new_books_window.title(f'Library {login_info} - Add new Books')

			def add_book():
				book_title_info = book_title.get()
				book_author_info = book_author.get()
				book_pages_info = book_pages.get()
				if self.lib.can_be_add(book_title_info):
					self.lib.add_new_book(book_title_info, book_author_info, book_pages_info)
					if messagebox.askyesno("Successful",
										   f"Book '{book_title_info}' successful add. Are you want add next?"):
						new_books_window.destroy()
						add_new_books()
					else:
						new_books_window.destroy()
						admin_interface.wm_deiconify()
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
			Button(new_books_window, text="Add Book", height="2", width="30", command=add_book).pack()

		# Button(new_books_window, text="return", height="1", width="15",
		#        command=lambda: self.DESTROY_PAGE(destroy_page=new_books_window, return_page=admin_interface)).pack(pady=20)

		def change_users_password():
			psr_manager_window = Toplevel(admin_interface)
			admin_interface.withdraw()
			self.CONFIGURE_GUI(psr_manager_window, admin_interface, None)
			psr_manager_window.title(f'Library {login_info} - Passwords manager')

			def change_password():
				user_name_info = user_name.get()
				old_password_info = old_password.get()
				new_password_info = new_password.get()
				if self.lib.password_available(new_password_info):
					self.lib.change_password(user_name_info, old_password_info, new_password_info)
					if messagebox.showwarning("Successful",
											  f"Password for user:'{user_name_info}' successful changed!"):
						psr_manager_window.destroy()
						admin_interface.wm_deiconify()

			user_name = StringVar()
			Label(psr_manager_window, text="Username:").pack()
			Entry(psr_manager_window, textvariable=user_name).pack()
			old_password = StringVar()
			Label(psr_manager_window, text="Old Password:").pack()
			Entry(psr_manager_window, textvariable=old_password).pack()
			new_password = StringVar()
			Label(psr_manager_window, text="New Password:").pack()
			Entry(psr_manager_window, textvariable=new_password).pack()
			Button(psr_manager_window, text="Confirm", height="2", width="30", command=change_password).pack()

		# Button(psr_manager_window, text="return", height="1", width="15",
		#        command=lambda: self.DESTROY_PAGE(destroy_page=psr_manager_window, return_page=admin_interface)).pack(pady=20)

		Label(admin_interface, text="Whats you want do?", width="300", height="2").pack()
		Label(admin_interface, text="").pack()
		Button(admin_interface, text="Add Books", height="2", width="30",
			   command=add_new_books).pack()
		Button(admin_interface, text="Password Manager", height="2", width="30",
			   command=change_users_password).pack()


# Button(admin_interface, text="LOGOUT", height="1", width="15",
#        command=lambda: self.DESTROY_PAGE(destroy_page=admin_interface, return_page=self.root)).pack(pady=20)


GuiImainPage()
