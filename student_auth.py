import re, dbconn, hash
from flask import jsonify


def sign_up(name, email, password):
    hashed_password = hash.hash_pwd(password)
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify(status='Failed', message='Please enter valid email!')
    if name is None or email is None or password is None:
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


def login(email, password):
    if email is None or password is None:
        res = jsonify(status=0, message='Missing fields!')
        return res
    hashed_password = hash.hash_pwd(password)
    if not dbconn.email_already_exists(email):
        res = jsonify(status=0, message='Email not present!')
    else:
        api_key = dbconn.login(email, hashed_password)
        if api_key is None:
            res = jsonify(status=0, message='Auth failure!')
        else:
            res = jsonify(status=1, api_key=api_key)
    return res
