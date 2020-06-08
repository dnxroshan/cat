
import os

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import jsonify

from flask_login import LoginManager
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from flask_login import current_user

from table_users import TableUsers
from table_candidates import TableCandidates
from table_examiners import TableExaminers
from table_tests import TableTests

from form_login import FormLogin
from form_candidate_reg import FormCandidateReg

from user import User
from crypto import Crypto
from misc import *
import config
import constants

app = Flask(__name__)
app.secret_key = config.SECRET_KEY
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER

table_users = TableUsers()
table_candidates = TableCandidates()
table_examiners = TableExaminers()
table_tests = TableTests()
crypto = Crypto()

login_manager = LoginManager(app)

@login_manager.user_loader
def user_loader(user_id):
    if table_users.get(user_id):
        return User(user_id)


'''
    View Function for Home

'''
@app.route('/')
def home():
    form_login = FormLogin()
    return render_template('home.html', form_login=form_login)

@app.route('/login', methods=['POST'])
def login():

    form = FormLogin(request.form)

    if form.validate():
        user_data = table_users.get(form.username.data)
        if not user_data:
            form.username.errors.append('User not registrad')
            return render_template('home.html', form_login=form)

        if crypto.validate_password(form.password.data, user_data['salt'], user_data['hashed']):
            user = User(form.username.data)
            login_user(user)

            if user_data['type'] == constants.UserType.Candidate:
                return redirect(url_for('candidate'))
            elif user_data['type'] == constants.UserType.Examiner:
                return redirect(url_for('examiner', tab='add-test'))
            else:
                return redirect(url_for('admin'))
        else:
            form.password.errors.append('Incorrect password')
            return render_template('home.html', form_login=form)

    return render_template('home.html', form_login=form)

@app.route('/candiadte-registration')
def candidate_registration():
    form_reg = FormCandidateReg()
    return render_template('candidate_registration.html', form_reg=form_reg)

@app.route('/examiner-registration')
def examiner_registration():
    return render_template('examiner_registration.html')

@app.route('/candiadte-registration/add-candidate', methods=['POST'])
def add_candidate():
    form = FormCandidateReg(request.form)

    if form.validate():
        if table_users.get(form.username.data):
            form.username.errors.append('This username is not available.')
            return render_template('candidate_registration.html', form_reg=form)

        add_user(form.username.data, form.password.data, constants.UserType.Candidate)

        candidate_data = {
            'username'  : form.username.data,
            'first_name': form.first_name.data,
            'last_name' : form.last_name.data,
            'dob'       : form.dob.data,
            'gender'    : form.gender.data,
            'standard'  : form.standard.data,
            'school'    : form.school.data,
            'email'     : form.email.data,
            'phone'     : form.phone.data
        }
        table_candidates.add(candidate_data)
        return redirect(url_for('home'))
    return render_template('candidate_registration.html', form_reg=form)

@app.route('/examiner-registration/add-examiner', methods=['POST'])
def add_examiner():
    form = dict(request.form)

    if table_users.get(form['username']):
        return redirect(url_for('examiner_registeration'))
    if form['password'] != form['passwordre']:
        return redirect(url_for('examiner_registeration'))

    add_user(form['username'], form['password'], constants.UserType.Examiner)

    examiner_data = {
        'username'  : form['username'],
        'first_name': form['first_name'],
        'last_name' : form['last_name'],
        'subject'   : form['subject'],
        'school'    : form['school'],
    }
    table_examiners.add(examiner_data)
    return redirect(url_for('home'))

@app.route('/admin')
@login_required
def admin():
    authorized(constants.UserType.Admin)
    return render_template('admin.html')

@app.route('/examiner')
@login_required
def examiner():
    authorized(constants.UserType.Examiner)
    return render_template('examiner.html', username=current_user.get_id())

@app.route('/candidate')
@login_required
def candidate():
    authorized(constants.UserType.Candidate)
    return render_template('candidate.html')

@app.route('/examiner/add-test', methods=['POST'])
@login_required
def add_test():
    authorized(constants.UserType.Examiner)

    form = dict(request.form)
    uploaded_file = request.files['question_bank']

    new_test = {
        'examiner'          : current_user.get_id(),
        'title'             : form['title'], 
        'description'       : form['description'],
        'date'              : form['date'],
        'subject'           : form['subject'],
        'standard'          : form['standard'], 
        'score_easy'        : form['score_easy'],
        'score_medium'      : form['score_medium'],
        'score_hard'        : form['score_hard'], 
        'score_threshold'   : form['score_threshold'], 
    }
    new_test_id = table_tests.get_new_id()
    table_tests.add(new_test)
    qb_filename = generate_qb_filename(new_test_id)
    uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], qb_filename))
    return redirect(url_for('add_test'))

@app.route('/examiner/get-tests', methods = ['GET'])
@login_required
def get_tests():
    username = current_user.get_id()
    data = table_tests.get_by_examiner(username)
    return jsonify(data)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

def authorized(type):
    user = table_users.get(current_user.get_id())
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

    table_users.add(new_user)

if __name__ == '__main__':
    app.run(debug=True)
