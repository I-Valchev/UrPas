import hashlib
import binascii

class Authenticate:
	def set_password(self, password):
		self.password = password

	def print_password(self):
		print(self.password)

	def execute(self):
		self.__encrypt()

	def __encrypt(self):
		if not getattr(self, 'password', None):
			return
		enc = hashlib.sha224(self.password)

		for i in range(0, 100000):
			enc = hashlib.sha224(enc.hexdigest())
			
		self.encrypted_password = enc.hexdigest()


	self.encryption_value = 100000 

	def encrypt(self, password):
		encrypted_password = hashlib.sha224(password)

		for i in range(0, self.encryption_value):
			encrypted_password = hashlib.sha224(enc.hexdigest())

		return encrypted_password
