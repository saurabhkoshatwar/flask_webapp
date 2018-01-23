import re, dbconn, hash
from flask import jsonify


def sign_up(name, email, password):
    hashed_password = hash.hash_pwd(password)
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify(status='Failed', message='Please enter valid email!')
    if name == None or email == None or password == None:
        return jsonify(status='Failed', message='Missing parameter')
    if dbconn.email_already_exists(email):
        return jsonify(status='Failed', message='Email already exists!')
    else:
        api_key = dbconn.sign_up(name, email, hashed_password)
        if api_key:
            res = jsonify(status="Successful!", api_key=api_key)
        else:
            res = jsonify(status="Failed", message="Try Again!")
        return res

def login():
    pass