from Tkinter import *
import Tkinter
import tkMessageBox
import User
import Password
import os


root = Tkinter.Tk()
class GUI:

	def __init__(self,root):
		root.columnconfigure(0, weight=1)	
		root.rowconfigure(0, weight=1)
		root.title("UrPas v 0.1")
		self.frame = Frame(root)
		self.frame.grid()

		os.chdir("/opt/lampp")
		os.system("sudo ./xampp start")

		self.login_username_label = Label(self.frame, text="Username: ")
		self.login_username_label.grid(row=0)
		self.login_password_label = Label(self.frame, text="Password: ")
		self.login_password_label.grid(row=1)

		self.login_username_entry = Entry(self.frame)
		self.login_password_entry = Entry(self.frame, show='*')
		self.login_username_entry.grid(row=0, column=1)		
		self.login_password_entry.grid(row=1, column=1)

		self.login_button = Button(self.frame, text="Login", command=self.login_btn)
		self.login_button.grid(row=2, column=1)

		self.register_username = Label(self.frame, text="Select username: ")
		self.register_username.grid(row=3, pady=(40,0))

		self.register_username_entry = Entry(self.frame)
		self.register_username_entry.grid(row=3, column=1, pady=(40,0))

		self.register_button = Button(self.frame, text="Register", command=self.register)
		self.register_button.grid(row=4, column=1)

	def __del__(self):
		os.chdir("/opt/lampp")
		os.system("sudo ./xampp stop")

	def register(self):
		self.register_username_entry.grid(row=3, column=1, pady=(40,0))
		user = User.User()
		password_generator = Password.Password()
		random_password = password_generator.generate_key()
		if user.create(self.register_username_entry.get(), random_password):
			print user.password
			tkMessageBox.showinfo("Registration status", "Registration successful!\n" + user.password)
		else:
			tkMessageBox.showinfo("Registration status", "Registraton FAILED. This username already exists")

	def update_lists(self):
		if self.username_listbox:
			self.username_listbox.delete(0, END)
		if self.password_listbox:
			self.password_listbox.delete(0, END)

		self.destinations_list = self.user.get_destinations()
		self.passwords_list = self.user.get_passwords(self.destinations_list)
		for destination in self.destinations_list:
			self.username_listbox.insert(END, destination)

		for password in self.passwords_list:
			self.password_listbox.insert(END, password)		

	def list_data(self):
		self.username_listbox = Listbox(root, width=40)
		self.username_listbox.grid(row=0,column=0,sticky=W)
		self.password_listbox = Listbox(root,width=40)
		self.password_listbox.grid(row=0,column=1,sticky=W)

		self.update_lists()

		self.username_listbox.grid()
		self.password_listbox.grid()

	def open(self):
		root.geometry("175x200")
		top.mainloop()   	

	def add_new_record(self):
		self.root=Tkinter.Tk()
		self.root.title("Add record")
		self.root.geometry("175x200")
		self.save_frame = Frame(self.root)
		self.save_frame.grid()
		add_username_label=Label(self.save_frame,text="New destination:")
		add_username_label.grid()
		self.add_username_entry=Entry(self.save_frame)
		self.add_username_entry.grid()
		add_password_label=Label(self.save_frame, text="New password:")
		add_password_label.grid()
		self.add_password_entry=Entry(self.save_frame, show="*")
		self.add_password_entry.grid()
		confirm_password_label=Label(self.save_frame, text="Confirm password:")
		confirm_password_label.grid()
		self.confirm_password_entry=Entry(self.save_frame, show="*")
		self.confirm_password_entry.grid()
		self.save_button=Button(self.save_frame,text="Save",command=self.add_new_record_button)
		self.save_button.grid(row=6, column=0)

	def add_new_record_button(self):
		if self.add_password_entry.get()==self.confirm_password_entry.get():
			self.user.add_data(self.add_username_entry.get(), self.add_password_entry.get())	
			self.update_lists()	
			tkMessageBox.showinfo("Status","Save successfully!")
			self.save_frame.destroy()
			self.root.destroy()
		else:
			tkMessageBox.showinfo("Status","Failed to save! Passwords mismatch! Try again")

	def help(self):
		tkMessageBox.showinfo("About", ("It is simple password application "
			"that will allow the user to save his password via a "
			"personal account. Other options include, but are not "
			"limited to, password generation and encryption. A demo "
			"version is availabe for the first 5 saved and 2 random "
			"generated passwords. Full licensed version is available "
			"for $5. The licensed version includes: unlimited number "
			"of saved passwords; unlimited number of password generations."))

	
	def login_btn(self):
		username=self.login_username_entry.get()
		password=self.login_password_entry.get()
		self.user = User.User()
		if self.user.auth(username, password):
			tkMessageBox.showinfo("Login info", "Welcome " + self.user.username)
			self.create_menu()
		else:
			tkMessageBox.showinfo("Login info", "Incorrect username or password")

	def remove_record(self):
		self.remove_one_record_root=Tkinter.Tk()
		self.remove_one_record_root.geometry("175x200")
		self.remove_one_record_root.title("Remove record")
		self.remove_frame = Frame(self.remove_one_record_root)
		self.remove_frame.grid()
		remove_destination_label=Label(self.remove_frame,text="Remove destination:")
		remove_destination_label.grid()
		self.remove_destination_entry=Entry(self.remove_frame)
		self.remove_destination_entry.grid()
		remove_button=Button(self.remove_frame,text="Remove", command=self.remove_one_record)
		remove_button.grid(row=3)

	def remove_one_record(self):
		destination = self.remove_destination_entry.get()
		if self.user.delete_record(destination):
			self.update_lists()
			tkMessageBox.showinfo("Remove status","Removed successfuly!")
			self.remove_one_record_root.destroy()
		else:
			tkMessageBox.showinfo("Status","Failed to remove! Destination does not exist! Try again")

	def remove_all(self):
		self.remove_root=Tkinter.Tk()
		#self.remove_root.geometry("175x200")
		self.remove_root.title("Remove all records")
		self.remove_all_frame = Frame(self.remove_root)
		self.remove_all_frame.grid()
		self.remove_all_button=Button(self.remove_all_frame,text="Remove all records", command=self.remove_all_records)
		self.remove_all_button.grid(row=3)

	def remove_all_records(self):
		if self.user.delete_all_records():
			self.update_lists()
			tkMessageBox.showinfo("Remove","Removed successfully!")
			self.remove_all_frame.destroy()
			self.remove_root.destroy()
		else:
			tkMessageBox.showinfo("Status","Failed to remove! Try again!")

	def edit_password(self):
		self.edit_root=Tkinter.Tk()
		self.edit_root.geometry("175x200")
		self.edit_root.title("Edit password")
		self.edit_frame = Frame(self.edit_root)
		self.edit_frame.grid()
		self.edit_destination_label = Label(self.edit_frame, text="Destination: ")
		self.edit_destination_label.grid()
		self.edit_destination_entry = Entry(self.edit_frame)
		self.edit_destination_entry.grid()

		self.edit_new_password_label=Label(self.edit_frame,text="New password: ")
		self.edit_new_password_label.grid()
		self.edit_new_password_entry=Entry(self.edit_frame, show="*")
		self.edit_new_password_entry.grid()
		
		self.edit_button=Button(self.edit_frame,text="Edit", command=self.edit_password_button)
		self.edit_button.grid(row=4)

	def edit_password_button(self):
		if self.user.edit_password(self.edit_destination_entry.get(), self.edit_new_password_entry.get()):
			self.update_lists()
			tkMessageBox.showinfo("Edit status","Password edited successfuly!")
			self.edit_root.destroy()
		else:
			tkMessageBox.showinfo("Edit status","Failed to edit password!")

	def generate_password(self):
		self.generate_root=Tkinter.Tk()
		self.generate_root.title("Generate password")
		self.generate_frame=Frame(self.generate_root)
		self.generate_frame.grid()
		self.generate_password_label=Label(self.generate_frame,text="Generate: ")
		self.generate_password_label.grid()
		'''
		self.CheckVar1 = IntVar()
		self.special=Checkbutton(self.generate_root, text = "Special symbols", variable = self.CheckVar1)
		self.CheckVar2 = IntVar()
		self.CheckVar3= IntVar()
		self.CheckVar4= IntVar()
		self.uppercase = Checkbutton(self.generate_root, text = "Uppercases", variable = self.CheckVar2, \
		                 onvalue = 1, offvalue = 0, height=2, \
		                 width = 20)
		self.lowercase = Checkbutton(self.generate_root, text = "Lowercases", variable = self.CheckVar3, \
		                 onvalue = 1, offvalue = 0, height=2, \
		                 width = 20)
		self.digits = Checkbutton(self.generate_root, text = "Digits", variable = self.CheckVar4, \
		                 onvalue = 1, offvalue = 0, height=2, \
		                 width = 20)
		self.special.grid()
		self.uppercase.grid()
		self.lowercase.grid()
		self.digits.grid()
		'''
		self.special_symbols=False
		self.special=Checkbutton(self.generate_root, text="Special symbols", command=self.symbol_state)
		self.uppercase_symbols = False
		self.uppercase=Checkbutton(self.generate_root, text="Uppercases", command=self.uppercase_state)
		self.lowercase_symbols = False
		self.lowercase=Checkbutton(self.generate_root, text="Lowercases", command=self.lowercase_state)
		self.digit = False
		self.digits=Checkbutton(self.generate_root, text="Digits", command=self.digits_state)
		self.generate_button=Button(self.generate_frame, text="Generate", command=self.generate_password_button)		
		self.generate_button.grid()
		self.special.grid()
		self.uppercase.grid()
		self.lowercase.grid()
		self.digits.grid()

	def symbol_state(self):
		self.special_symbols = not self.special_symbols

	def uppercase_state(self):
		self.uppercase_symbols = not self.uppercase_symbols

	def lowercase_state(self):
		self.lowercase_symbols = not self.lowercase_symbols

	def digits_state(self):
		self.digit = not self.digit

	def generate_password_button(self):
		if self.special_symbols==True or self.lowercase_symbols==True or self.uppercase_symbols==True\
				or self.digits==True:
			p = Password.Password()
			p.special_symbols(self.special_symbols)
			p.set_uppercase(self.uppercase_symbols)
			p.set_lowercase(self.lowercase_symbols)
			p.set_digits(self.digit)

			random_password = p.generate()
			tkMessageBox.showinfo("Generate status","Password generated successfully!\n" + random_password)

			self.generate_root.destroy()
		else:
			tkMessageBox.showinfo("Error","You must select at least one option")
		

	def create_menu(self):
		self.list_data()		
		self.login_username_label.grid_forget()
		self.login_password_label.grid_forget()
		self.register_username.grid_forget()
		self.login_username_entry.destroy()
		self.login_password_entry.destroy()
		self.register_username_entry.destroy()
		self.login_button.destroy()
		self.register_button.destroy()
		menubar = Menu(root)
		filemenu = Menu(menubar, tearoff=0)
		filemenu.add_command(label="Generate password", command=self.generate_password)

		filemenu.add_separator()
		menubar.add_cascade(label="Generate", menu=filemenu)

		editmenu = Menu(menubar, tearoff=0)
		editmenu.add_command(label="Add new record", command=self.add_new_record)
		editmenu.add_command(label="Edit password", command=self.edit_password)
		editmenu.add_command(label="Remove record", command=self.remove_record)
		editmenu.add_command(label="Remove all records", command=self.remove_all)

		editmenu.add_separator()

		menubar.add_cascade(label="Edit", menu=editmenu)
		helpmenu = Menu(menubar, tearoff=0)
		helpmenu.add_command(label="About...", command=self.help)
		menubar.add_cascade(label="Help", menu=helpmenu)

		root.config(menu=menubar)



gui=GUI(root)
root.mainloop()
