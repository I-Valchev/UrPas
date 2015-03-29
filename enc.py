import hashlib

pas = hashlib.sha224('password').hexdigest()
print(hashlib.sha224(pas)).hexdigest()