all:
	coverage run Password_test.py
	coverage report -m
	coverage html