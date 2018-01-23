import re, dbconn
from flask import jsonify


def sign_up(name, email, password):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify(status='Failed', message='Please enter valid email!')
    if name == None or email == None or password == None:
        return jsonify(status='Failed', message='Missing parameter')
    if dbconn.email_already_exists(email):
        return jsonify(status='Failed', message='Email already exists!')
    else:
        pass
