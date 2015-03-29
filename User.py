import Database

class User():
	def __init__(self, username):
		self.username = username
		self.password = Password.Password

	def set_password(self, password):
		self.password = pasword

	def create(self):
		print("Creating user...")
		self.__user_database__()

	def __user_database__(self):

		if not getattr(self, 'username', None) or not getattr(self, 'password', None):
			return #exception?
		print("Still...")
		db = Database.Database(self.username, self.password)
		db.build_database()