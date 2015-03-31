import Password
import Database
import User

import unittest


password = Password.Password()
base = Database.Database()

base.clear_users()
#base.add_user("Pesho", "123456")
base.add_user("Pesho", "123456")
user = User.User("Pesho", "12356")

#print(base.get_user_id("Pesho"))
#print(base.get_user_id("Pesho"))
#base.print_users()