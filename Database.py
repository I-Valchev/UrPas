import MySQLdb
import Password
import os

class Database:
	def __init__(self):
		self.db = MySQLdb.connect(host="localhost", user="root", passwd="", db="UrPasDB", unix_socket="/opt/lampp/var/mysql/mysql.sock")
		self.cursor = self.db.cursor()

	def _add_data(self, user, destination, password):
		user_id = self.get_user_id(user.username)
		self._execute("INSERT IGNORE INTO Passwords(UserID, Destination, Password) VALUES('%s', '%s','%s')" 
			% (user_id, destination, password))
		self._commit()

	def _get_data(self, user, destination):
		user_id = self.get_user_id(user.username)
		self._execute("SELECT Password FROM Passwords WHERE UserID='%s' AND Destination = '%s'" % (user_id, destination))
		user_row = self.cursor.fetchone()
		if user_row is None:
			print "No password"
			return
		return user_row[0]

	def _extract_user(self, username, column):
		self._execute("SELECT %s FROM User WHERE Username='%s'" % (column, username))
		user_row = self.cursor.fetchone()
		if user_row is None:
			print("Such user does not exist")
			return
			
		return user_row

	def get_user_hash(self, username):
		return self._extract_user(username, "Hash")[0]

	def get_user_id(self, username):
		return self._extract_user(username, "UserID")[0]

	def clear_passwords(self):
		self._execute("TRUNCATE TABLE Passwords")
		self._commit()

	def clear_users(self):
		self._execute("TRUNCATE TABLE User")
		self._commit()

	def clear_passwords(self):
		self._execute("TRUNCATE TABLE Passwords")
		self._commit()

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

	def _add_user(self, user, password):
		print "Addint user"
		self._execute("INSERT IGNORE INTO User(Username, Hash) VALUES('%s', '%s')" % (user, password))
		self._commit()