import hash,dbconn,re
from flask import jsonify

def login(email, password):
    if email is None or password is None:
        res = jsonify(status=0, message='Missing fields!'), 400
        return res
    hashed_password = hash.hash_pwd(password)
    if not dbconn.email_already_exists_teacher(email):
        res = jsonify(status=0, message='Email not present!'), 400
    else:
        api_key = dbconn.login_teacher(email, hashed_password)
        if api_key is None:
            res = jsonify(status=0, message='Auth failure!'), 401
        else:
            res = jsonify(status=1, api_key=api_key)
    return res
