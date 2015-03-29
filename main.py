import Password
import Database
import unittest

password = Password.Password()
base = Database.Database()

base.add_user("BasiParolata", "dsjfodasjffkaf")
# get the number of rows in the resultset
base.print_users()
