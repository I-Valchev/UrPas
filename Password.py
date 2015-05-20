import random
import string
import hashlib
import os
import base64
from Crypto.Cipher import AES

class Password:
	
	def __init__(self):
		self.special = ""
		self.uppercase = ""
		self.digits = ""
		self.set_lowercase(True) # default generation
		self.length = 10
		self.times_to_encrypt = 100000
		self.BLOCK_SIZE = 32

	def decrypt(self, encrypted_password, key):
		"""Decrypts an encrypted password given a key

		:param encrypted_password: password to be decrypted
		:param key: the key needed to decrypt the password
		:returns: String -- the decrypted password.
		"""
		PADDING = self._extract_key(key)[0]
		secret = self._extract_key(key)[1]

		cipher = AES.new(secret)

		decrypted_password = cipher.decrypt(base64.b64decode(encrypted_password)).rstrip(PADDING)

		return decrypted_password

	def _extract_key(self, key):
		PADDING = key[0]
		secret = key[1:]

		return [PADDING, secret]

	def generate_key(self):
		"""Generates a new key

		:returns: an array representing the key"""
		PADDING = random.choice(string.letters)
		secret = base64.b64encode(os.urandom(self.BLOCK_SIZE))
		return [PADDING, secret]

	def import_key(self, key):
		"""Imports a key

		:returns: the decoded key"""
		return base64.b64decode(key)

	def encrypt(self, password, key):
		"""Encrypts the given password using the given key

		:param password: the password to be encrypted
		:param key: the key used to encrypt the password
		:retuns: String -- the encrypted password"""
		PADDING = self._extract_key(key)[0]
		secret = self._extract_key(key)[1]
		
		cipher = AES.new(secret)

		pasword_to_encrypt = password + (self.BLOCK_SIZE - len(password) % self.BLOCK_SIZE) * PADDING
		encrypted_password = base64.b64encode(cipher.encrypt(pasword_to_encrypt))
		return encrypted_password

	def generate_hash(self, password):
		"""Generates a hash by a given user password

		:param password: the password to be hashed
		:returns: String -- the hashed password"""
		encrypted_password = hashlib.sha224(password).hexdigest()

		for i in range(0, self.times_to_encrypt-1):
			encrypted_password = hashlib.sha224(encrypted_password).hexdigest()

		return encrypted_password

	def set_length(self,length):
		"""Sets the length of an automatically generated password

		:param: length - the length of the password to be generated"""
		self.length = length

	def generate(self):
		"""Generates a password

		Dependencies: special, digits, uppercase and lowercase (either True or False)"""
		chars = self.special + self.digits + self.uppercase + self.lowercase
		print "CHARS: " + chars
		return ''.join(random.choice(chars) for _ in range(self.length))

	def special_symbols(self, to_generate=True):
		"""Allows/forbids the generation of special special_symbols

		:param to_generate: boolean"""
		if to_generate:
			self.special = "`~!@?#+$%^=&:*/(_)-[]{};<>.,|"
		else:
			self.speical = ""

	def set_uppercase(self,to_generate):
		"""Allows/forbids the generation of uppercases

		:param to_generate: boolean"""
		if to_generate:
			self.uppercase = string.ascii_uppercase
		else:
			self.uppercase = ""

	def set_lowercase(self,to_generate):
		"""Allows/forbids the generation of lowercases

		:param to_generate: boolean"""
		if to_generate:
			self.lowercase = string.ascii_lowercase
		else:
			self.lowercase = ""

	def set_digits(self,to_generate):
		"""Allows/forbids the generation of digits

		:param to_generate: boolean"""
		if to_generate:
			self.digits = string.digits
		else:
			self.digits = ""



