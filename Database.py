import MySQLdb
import Password
import os

class Database:
	def __init__(self):
		self.db = MySQLdb.connect(host="localhost", user="root", passwd="", db="UrPasDB", unix_socket="/opt/lampp/var/mysql/mysql.sock")
		self.cursor = self.db.cursor()

	def _add_data(self, user, destination, password):
		user_id = self.get_user_id(user.username)
		self._execute("SELECT Destination FROM Passwords WHERE Destination = '%s'" % destination)
		command_result = self.cursor.fetchone()

		if command_result is None:
			self._execute("INSERT IGNORE INTO Passwords(UserID, Destination, Password) VALUES('%s', '%s','%s')" 
				% (user_id, destination, password))
			self._commit()
			print "Data for " + destination + " added successfully"
		else:
			print "Warning: Destination (" + destination + ") already exists. Not added..."
			pass

	def _get_password(self, user, destination):
		user_id = self.get_user_id(user.username)
		self._execute("SELECT Password FROM Passwords WHERE UserID='%s' AND Destination = '%s'" % (user_id, destination))
		user_row = self.cursor.fetchone()
		if user_row is None:
			print "No password"
			return
		return user_row[0]

	def _get_destinations(self, user):
		user_id = self.get_user_id(user.username)
		self._execute("SELECT Destination FROM Passwords WHERE UserID='%s'" % user_id)
		destinations_tuple = self.cursor.fetchall()
		result = list()
		for element in destinations_tuple:
			result.append(element[0])

		return result

	def _extract_user(self, username, column):
		self._execute("SELECT %s FROM User WHERE Username='%s'" % (column, username))
		user_row = self.cursor.fetchone()
		if user_row is None:
			print("Such user does not exist")
			return
			
		return user_row

	def get_user_hash(self, username):
		'''Given a username returns its hashed password

		:param username: the username to extract the hash from
		:returns: String -- the hashed password
		'''
		return self._extract_user(username, "Hash")[0]

	def get_user_id(self, username):
		'''Given a username returns the Database ID of that user

		:param username: the username to get the ID from
		:returns: Int -- the ID of the user
		'''
		return self._extract_user(username, "UserID")[0]

	def clear_passwords(self):
		'''Resets the Password database
		'''
		self._execute("TRUNCATE TABLE Passwords")
		self._commit()

	def clear_users(self):
		'''Resets the User database
		'''
		self._execute("TRUNCATE TABLE User")
		self._commit()

	def print_users(self):
		'''Prints all users from User database
		'''
		self._execute("SELECT * FROM User")
		self._print()

	def print_passwords(self):
		'''Prints all (hashed) password from Passwords database
		'''
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
		self._execute("INSERT IGNORE INTO User(Username, Hash) VALUES('%s', '%s')" % (user, password))
		self._commit()