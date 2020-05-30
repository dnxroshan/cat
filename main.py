
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

from flask_login import LoginManager
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from flask_login import current_user

from table_users import TableUsers
from table_candidates import TableCandidates
from user import User
from crypto import Crypto
import config
import constants

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

table_users = TableUsers()
table_candidates = TableCandidates()
crypto = Crypto()

login_manager = LoginManager(app)

@login_manager.user_loader
def user_loader(user_id):
    if table_users.get_user(user_id):
        return User(user_id)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['POST'])
def login():
    error = False
    username = request.form.get('username')
    password = request.form.get('password')

    user_data = table_users.get_user(username)

    if not user_data:
        return redirect(url_for('home'))

    if crypto.validate_password(password, user_data['salt'], user_data['hashed']):
        user = User(username)
        login_user(user)

        if user_data['type'] == constants.UserType.Candidate:
            return redirect(url_for('candidate'))
        elif user_data['type'] == constants.UserType.Examiner:
            return redirect(url_for('candidate'))
        else:
            return redirect(url_for('admin'))
            
    return redirect(url_for('home'))

@app.route('/candiadte_signup')
def candidate_signup():
    return render_template('candidate_signup.html')

@app.route('/candidate_signup/add_candidate', methods=['POST'])
def add_candidate():
    form = dict(request.form)

    if table_users.get_user(form['username']):
        return redirect(url_for('candidate_signup'))
    if form['password'] != form['passwordre']:
        return redirect(url_for('candidate_signup'))

    add_user(form['username'], form['password'], constants.UserType.Candidate)

    candidate_data = {
        'username'  : form['username'],
        'first_name': form['first_name'],
        'last_name' : form['last_name'],
        'dob'       : form['dob'],
        'gender'    : form['gender'],
        'standard'  : form['standard'],
        'school'    : form['school'],
        'email'     : form['email'],
        'phone'     : form['phone']
    }
    table_candidates.add_candidate(candidate_data)
    return redirect(url_for('home'))

@app.route('/admin')
@login_required
def admin():
    authorized(constants.UserType.Admin)
    return render_template('admin_home.html')

@app.route('/examiner')
@login_required
def examiner():
    authorized(constants.UserType.Examiner)
    return render_template('examiner_home.html')

@app.route('/candidate')
@login_required
def candidate():
    authorized(constants.UserType.Candidate)
    return render_template('candidate_home.html')

def authorized(type):
    user = table_users.get_user(current_user.get_id())
    print(type)
    if user['type'] != type:
        return login_manager.unauthorized()

def add_user(username, password, user_type):
    salt = crypto.get_salt()
    hashed = crypto.get_hash(salt + password)

    new_user = {
        'username': username,
        'salt'    : salt,
        'hashed'  : hashed,
        'type'    : user_type
    }

    table_users.add_user(new_user)

if __name__ == '__main__':
    app.run(debug=True)
