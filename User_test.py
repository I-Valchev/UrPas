from User import *
import unittest
import os
class User_test(unittest.TestCase):
    def setUp(self):
        self.u = User()
        os.chdir("/opt/lampp")
        os.system("sudo ./xampp start")

    def setDown(self):
        os.system("sudo ./xampp stop")

    def test_create_and_username(self):
        self.u.create("TestUser", "TestPassword")
        self.assertEqual(self.u.get_username(), "TestUser")

    def test_add_data_unauthenticated(self):
        self.u.add_data("TestDestination", "TestPassword")

    def test_get_data_unauthenticated(self):
        self.u.get_data(destination="TestDestination")
        
if __name__ == '__main__':
    unittest.main()