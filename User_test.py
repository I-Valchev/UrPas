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
        self.u.create('TestUser', 'TestPassword')
        self.assertEqual(self.u.get_username(), 'TestUser')
        
if __name__ == '__main__':
    unittest.main()