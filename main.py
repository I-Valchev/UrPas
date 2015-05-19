import Password
import Database
import User
import base64
import unittest


password = Password.Password()
base = Database.Database()

#print(password.generate_hash('password'))

#base.clear_users()
#base.clear_passwords()
#user_key = password.generate_key()
#user = User.User()
#user.create("Ivo", user_key)
#print user.password

user = User.User()
user.auth("Ivo", "oedlhgAABdkLBe9CIUTU93wznTIrSurKcO55KsSK3fP0=")
#user.add_data("testDest22", "testPass22")
#destinations = user.get_destinations()
#passwords = user.get_passwords(destinations)
#print(base.get_user_id("Pesho"))
#print(base.get_user_id("Pesho"))
#base.print_users()
'''
User: Ivo
Pass: oedlhgAABdkLBe9CIUTU93wznTIrSurKcO55KsSK3fP0=
'''