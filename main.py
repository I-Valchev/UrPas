import Password
import Database
import User
import base64
import unittest


password = Password.Password()
base = Database.Database()

#base.clear_users()
#base.clear_passwords()
#user_key = password.generate_key()
#user = User.User()
#user.create("Ivo", user_key)
#print user.password

user = User.User()
user.auth("Ivo", "vVuhFMWp4epQGj45KFHLm49zhTnWEEL14dELs4itHEg8=")
#user.add_data("www.google.bg", "some_random_pass")
user.get_data("www.google.bg")
print user.password

#print(base.get_user_id("Pesho"))
#print(base.get_user_id("Pesho"))
#base.print_users()