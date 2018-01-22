import re
from flask import jsonify
def sign_up(name, email, password):
	if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
		return jsonify(status = '0')