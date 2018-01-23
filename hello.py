from flask import Flask, jsonify, request
import dbconn, signup

app = Flask(__name__)


@app.route("/", methods=['GET'])
def hello():
    return "<h1>Hello World!</h1>"


@app.route('/api/v1/test/<int:id>', methods=['GET'])
def tester(id):
    return (dbconn.dbtest(id))


@app.route('/api/v1/signup/student', methods=['POST'])
def signup_handler():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    print(name,email,password)
    return signup.sign_up(name, email, password)


if __name__ == '__main__':
    app.run()
