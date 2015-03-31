import Database
import Password

class User():
	def __init__(self, username, user_hash):
		self.given_username = username
		self.given_hash = Password.Password().generate_hash(user_hash)

	def _authenticate(self):
		if self.given_hash != Database.Database().get_user_hash(username):
			self.__del__()

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