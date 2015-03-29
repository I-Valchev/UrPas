import MySQLdb
import Password

class Database:
	def __init__(self):
		self.db = MySQLdb.connect(host="localhost", user="root", passwd="", db="UrPasDB", unix_socket="/opt/lampp/var/mysql/mysql.sock")
		self.cursor = self.db.cursor()

	def print_users(self):
		self._execute("SELECT * FROM User")
		self._print()

	def print_passwords(self):
		self._execute("SELECT * FROM Passwords")
		self._print()

	def _print(self):
		numrows = int(self.cursor.rowcount)
		for x in range(0,numrows):
		    row = self.cursor.fetchone()
		    print row[0], ":", row[1], ":", row[2]


	def _commit(self):
		self.db.commit()

	def _execute(self, string):
		self.cursor.execute(string)

	def add_user(self, username, password):
		pas = Password.Password()
		pas.set_times_to_encrypt(100000)
		password = pas.encrypt("Pass=" + password)
		self._execute("INSERT INTO User(Username, Password) VALUES('%s', '%s')" % (username, password))
		self._commit()