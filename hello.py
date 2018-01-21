from flask import Flask
import dbconn

app = Flask(__name__)


@app.route("/", methods=['GET'])
def hello():
    return "<h1>Hello</h1>"

@app.route('/api/v1/test/<int:id>', methods=['GET'])
def tester(id):
	return(dbconn.dbtest(id))

if __name__ == '__main__':
    app.run()
