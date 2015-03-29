import random
import string
import hashlib

class Password:
	
	def __init__(self):
		self.special = ""
		self.uppercase = ""
		self.digits = ""
		self.set_lowercase(True) #default generation
		self.length = 10
		self.times_to_encrypt = 100000

	def set_times_to_encrypt(self,times):
		self.times_to_encrypt = times

	def encrypt(self, password):
		encrypted_password = hashlib.sha224(password).hexdigest()

		for i in range(0, self.times_to_encrypt-1):
			encrypted_password = hashlib.sha224(encrypted_password).hexdigest()

		return encrypted_password

	
	def set_length(self,length):
		self.length = length


	def generate(self):
		chars = self.special + self.digits + self.uppercase + self.lowercase
		return ''.join(random.choice(chars) for _ in range(self.length))

	def special_symbols(self, to_generate=True):
		if to_generate:
			self.special = "`~!@?#+$%^=&:*/(_)-[]{};<>.,|"
		else:
			self.speical = ""

	def set_uppercase(self,to_generate):
		if to_generate:
			self.uppercase = string.ascii_uppercase
		else:
			self.uppercase = ""

	def set_lowercase(self,to_generate):
		if to_generate:
			self.lowercase = string.lowercase
		else:
			self.lowercase = ""

	def set_digits(self,to_generate):
		if to_generate:
			self.digits = string.digits
		else:
			self.digits = ""



