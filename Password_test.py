from Password import *
import unittest

class Password_test(unittest.TestCase):
	def setUp(self):
		self.p = Password()
		pass

	def test_times_to_encrypt(self):
		self.p.test_times_to_encrypt = 1
		self.assertEqual(self.p.test_times_to_encrypt, 1)

	def test_length(self):
		self.p.set_length(1)
		self.assertEqual(self.p.length, 1)

	def test_with_special_symbols(self):
		self.p.special_symbols(True)
		self.assertEqual(self.p.special, '`~!@?#+$%^=&:*/(_)-[]{};<>.,|')

	def test_without_special_symbols_false(self):
		self.p.special_symbols(False)
		self.assertEqual(self.p.special, '')

	def test_with_set_uppercase(self):
		self.p.set_uppercase(True)
		self.assertEqual(self.p.uppercase, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ')

	def test_without_set_uppercase(self):
		self.p.set_uppercase(False)
		self.assertEqual(self.p.uppercase, '')

	def test_set_lowercase(self):
		self.p.set_lowercase(True)
		self.assertEqual(self.p.lowercase, 'abcdefghijklmnopqrstuvwxyz')

	def test_set_digits(self):
		self.p.set_digits(True)
		self.assertEqual(self.p.digits, '0123456789')

	def test_generate_hash(self):
		self.assertEqual(self.p.generate_hash('password'), \
			'6f5e0d544a2a40fb33a1ef36600a585ce5cebe0dc588e14d50bb4fad')

if __name__ == '__main__':
	unittest.main()