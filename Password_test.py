from Password import *
import unittest

class Password_test(unittest.TestCase):
	def setUp(self):
		self.p = Password()
		pass

	def test_special_symbols(self):
		self.p.special_symbols(True)

		self.assertEqual(self.p.special, '`~!@?#+$%^=&:*/(_)-[]{};<>.,|')

	def test_times_to_encrypt(self):
		self.p.test_times_to_encrypt = 1
		self.assertEqual(self.p.test_times_to_encrypt, 1)

	def test_length(self):
		self.p.set_length(1)
		self.assertEqual(self.p.length, 1)

	def test_set_uppercase(self):
		self.p.set_uppercase(True)
		self.assertEqual(self.p.uppercase, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ')

	def test_set_lowercase(self):
		self.p.set_lowercase(True)
		self.assertEqual(self.p.lowercase, 'abcdefghijklmnopqrstuvwxyz')

	def test_set_digits(self):
		self.p.set_digits(True)
		self.assertEqual(self.p.digits, '0123456789')

if __name__ == '__main__':
	unittest.main()