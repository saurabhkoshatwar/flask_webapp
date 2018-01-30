import hashlib, os
def hash_pwd(password):
	salt = os.environ["SALT"].encode('utf-8')
	password = password.encode('utf-8')
	hashed_password = hashlib.sha512(password+salt).hexdigest()
	# print(type(hashed_password))
	return hashed_password