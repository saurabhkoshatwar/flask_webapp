from flask import Flask, jsonify, request
import dbconn, signup

app = Flask(__name__)


@app.route("/", methods=['GET'])
def hello():
    return "<h1>Hello World!</h1>"

@app.route('/api/v1/test/<int:id>', methods=['GET'])
def tester(id):
	return(dbconn.dbtest(id))

@app.route('/api/v1/signup/student', methods=['PUT'])
def signup():
	name = request.form.get('name')
	email = request.form.get('email')
	password = request.form.get('password')
	res = signup.sign_up(name, email, password)
	print(res)
	return res

if __name__ == '__main__':
    app.run()	