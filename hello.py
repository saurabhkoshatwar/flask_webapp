from flask import Flask, jsonify, request
import dbconn, student_auth

app = Flask(__name__)


@app.route("/", methods=['GET'])
def hello():
    return "<h1>Hello World!</h1>"


@app.route('/api/v1/test/<int:id>', methods=['GET'])
def tester(id):
    return dbconn.dbtest(id)


@app.route('/api/v1/signup/student', methods=['POST'])
def signup_handler():
    data = request.get_json()
    print(data)
    return student_auth.sign_up(data["name"], data["email"], data["password"])


if __name__ == '__main__':
    app.run(debug=True)
