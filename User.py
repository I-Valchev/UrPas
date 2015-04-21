import Database
import Password

class User():

	def __init__(self):
		pass

	def add_data(self, destination, password):
		'''Adds destination and password to user represented by the object its called from

		:param destination: the desination the passwords belongs to
		:param password: the password for the destination
		'''
		if not self.authenticated:
			print "User not authenticated"
			return

		db = Database.Database()
		encrypted_password = Password.Password().encrypt(password, self.key)
		db._add_data(self, destination, encrypted_password)

	def get_data(self, destination):
		'''Returns the password of a desination (authentication required)

		:param desination: the destination to extract the password from
		:returns: String -- the decrypted password
		'''
		if not self.authenticated:
			print "User not authenticated"
			return

		db = Database.Database()
		password = db._get_data(self, destination)
		decrypted_password = Password.Password().decrypt(password, self.key)
		return decrypted_password

	def auth(self, username, password):
		'''Authenticates the user
		Warning: If the authentication fails, data could not be added or extracted \
		from the Database

		:param username: the username of the user
		:param password: the password of the user
		'''
		self.username = username
		self.password = password
		self.authenticated = False
		self.key = Password.Password().import_key(password)
		self._authenticate()

	def username(self):
		'''Returns the username associated with this object
		'''
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
		'''Creates a new user

		:param user: the username of the user
		:param password: the password of the new user
		'''
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