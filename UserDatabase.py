import MySQLdb
'''
	def __init__(self, username, password):
		self.username = username
		self.password = password
		self.base = MySQLdb.connect("localhost", "prog_user", "prog", "urpas").cursor()
		self.sql = ""

	def build_database(self):
		self.sql = "CREATE DATABASE DB_%s" % self.username
		self.__execute()

		#self.sql = "USE DB_%s" % self.username
		#self.__execute()

		#self.sql = "CREATE TABLE userProperties( \
		#		ID int PRIMARY KEY AUTO_INCREMENT, \
		#		USERNAME VARCHAR(50) NOT NULL, \
		#		USER_PASSWORD VARCHAR(100) NOT NULL, \
		#	)"
		#self.__execute()
		print("Database created successfully.")


	def __execute(self):
		self.base.execute(self.sql)

'''

#!/usr/bin/python
import MySQLdb

class UserDatabase:
	def __init__(self):
		self.db = MySQLdb.connect(host="localhost", user="root", passwd="", db="UrPasDB", unix_socket="/opt/lampp/var/mysql/mysql.sock")
		self.cursor = self.db.cursor()

	def print_me(self):
		self._execute("SELECT * FROM User")

		numrows = int(self.cursor.rowcount)
		for x in range(0,numrows):
		    row = self.cursor.fetchone()
		    print row[0], ":", row[1], ":", row[2]


	def _commit(self):
		self.db.commit()

	def _execute(self, string):
		self.cursor.execute(string)

	def add(self, username, password):
		self._execute("INSERT INTO User(Username, Password) VALUES('%s', '%s')" % (username, password))
		self._commit()

			