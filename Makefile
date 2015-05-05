all:
	coverage run -p Password_test.py
	coverage run -p User_test.py
	coverage combine
	coverage report -m
	coverage html
