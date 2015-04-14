import Database
import Password

class User():

	def __init__(self):
		pass

	def add_data(self, destination, password):
		if not self.authenticated:
			print "User not authenticated"
			return

		db = Database.Database()
		encrypted_password = Password.Password().encrypt(password, self.key)
		db._add_data(self, destination, encrypted_password)

	def get_data(self, destination):
		if not self.authenticated:
			print "User not authenticated"
			return

		db = Database.Database()
		password = db._get_data(self, destination)
		decrypted_password = Password.Password().decrypt(password, self.key)
		return decrypted_password

	def auth(self, username, password):
		self.username = username
		self.password = password
		self.authenticated = False
		self.key = Password.Password().import_key(password)
		self._authenticate()

	def username(self):
		return self.username

	def _authenticate(self):
		hashed_password = Password.Password().generate_hash(self.password)
		if hashed_password != Database.Database().get_user_hash(self.username):
			print "Wrong username or password"
		else:
			self.authenticated = True
			print "Authenticated successfully!"

	#def set_password(self, password):
	#	self.password = pasword

	def create(self, user, password):
		print("Creating user...")
		encoded_password = ''.join(Password.Password().generate_key())
		self.password = encoded_password
		hashed_password = Password.Password().generate_hash(encoded_password)
		if not self.__user_is_in_database__():
			db = Database.Database()
			db._add_user(user, hashed_password)

	def __user_is_in_database__(self):
		if not getattr(self, 'username', None) or not getattr(self, 'password', None):
			return True
		return False