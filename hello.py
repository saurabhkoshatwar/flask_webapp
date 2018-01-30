from flask import Flask, jsonify, request, render_template, url_for, flash
from flask_wtf import form, Form
from wtforms import PasswordField


from wtforms.validators import DataRequired

import dbconn, student_auth,hash,os,re,json_gen
from flask_mail import Mail,Message
from itsdangerous import URLSafeTimedSerializer

app = Flask(__name__)
app.config.from_pyfile('flask.cfg')
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
app.config["MAIL_PASSWORD"] = os.environ["MAIL_PASSWORD"]

m = Mail(app)


class PasswordForm(Form):
    password = PasswordField('Password', validators=[DataRequired()])


@app.route("/", methods=['GET'])
def hello():
    return "<h1>Hello World!</h1>"


@app.route('/api/v1/test/<int:id>', methods=['GET'])
def tester(id):
    return dbconn.dbtest(id)


@app.route('/api/v1/signup/student', methods=['POST'])
def signup_handler():
    data = request.get_json()
    # print(data)
    try:
        return student_auth.sign_up(data["name"], data["email"], data["password"])
    except:
        return jsonify(status=0, message='Missing fields!/Error Occured! :/')



@app.route('/api/v1/login/student', methods=["POST"])
def login_handler():
    data = request.get_json()
    # print(data)
    try:
        return student_auth.login(data['email'], data['password'])
    except:
        return jsonify(status=0, message='Missing fields!/Error Occured! :/')

def send_email(subject,recipients,html_body):
    msg = Message(subject, recipients=recipients)
    msg.html = html_body
    m.send(msg) 
      
    
@app.route('/api/v1/forgot/', methods=["POST"])
def send_password_reset_email():
    data = request.get_json()
    user_email=data['email']
    if not re.match(r"[^@]+@[^@]+\.[^@]+", user_email):
        return jsonify(status='Failed', message='Please enter valid email!')
    if user_email is None:
        return jsonify(status='Failed', message='Missing parameter')
    if not dbconn.email_already_exists(user_email):
        return jsonify(status='Failed', message='Email not exists!')
    else:
    
        password_reset_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
 
        password_reset_url = url_for(
        'reset_with_token',
        token = password_reset_serializer.dumps(user_email, salt='password-reset-salt'),
        _external=True)
 
        html = render_template('email_password_reset.html',password_reset_url=password_reset_url)
        send_email('Password Reset Requested', [user_email], html)
        return jsonify(status="Link Sent!") 

@app.route('/reset/<token>', methods=["GET", "POST"])
def reset_with_token(token):
    try:
        password_reset_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        email = password_reset_serializer.loads(token, salt='password-reset-salt', max_age=3600)
        print(email)
    except:
        flash('The password reset link is invalid or has expired.', 'error')
        #return redirect(url_for('users.login'))
        return 'inv'

    form = PasswordForm()
 
    if form.validate_on_submit():
        hashed_password = hash.hash_pwd(form.password.data)
        status = dbconn.forgot(email,hashed_password)
        # try:
        #     user = User.query.filter_by(email=email).first_or_404()
        # except:
        #     flash('Invalid email address!', 'error')
        #     return redirect(url_for('users.login'))
        #
        # user.password = form.password.data
        # db.session.add(user)
        # db.session.commit()
        # flash('Your password has been updated!', 'success')
        # return redirect(url_for('users.login'))
        return status

    return render_template('reset_password_with_token.html', form=form, token=token)

   

@app.route('/api/v1/get_timetable/', methods=['GET'])
def get_timetable():
    date = request.args.get('date')
    shift = request.args.get('shift')
    batch = request.args.get('batch')
    print(date)
    return json_gen.generate(date, shift, batch)


if __name__ == '__main__':
    app.run()
