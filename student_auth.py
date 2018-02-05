import re, dbconn, hash
from flask import jsonify


def sign_up(name, email, password):
    hashed_password = hash.hash_pwd(password)
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify(status='Failed', message='Please enter valid email!')
    if name is None or email is None or password is None:
        return jsonify(status=0, message='Missing parameter'), 400
    if dbconn.email_already_exists(email):
        return jsonify(status=0, message='Email already exists!'), 400
    else:
        api_key = dbconn.sign_up(name, email, hashed_password)
        if api_key:
            res = jsonify(status=1, api_key=api_key)
        else:
            res = jsonify(status=0, message="Try Again!"), 400
        return res


def login(email, password):
    if email is None or password is None:
        res = jsonify(status=0, message='Missing fields!'), 400
        return res
    hashed_password = hash.hash_pwd(password)
    if not dbconn.email_already_exists(email):
        res = jsonify(status=0, message='Email not present!'), 400
    else:
        api_key = dbconn.login(email, hashed_password)
        if api_key is None:
            res = jsonify(status=0, message='Auth failure!'), 401
        else:
            res = jsonify(status=1, api_key=api_key)
    return res

def teacher_login(api_key):
    if api_key is None:
        res = jsonify(status=0, message='Missing fields!'), 400
        return res
    else:
        name = dbconn.t_login(api_key)
        if name is None:
            res = jsonify(status=0, message='Auth failure!'), 401
        else:
            res = jsonify(status=1, name=name)
    return res

