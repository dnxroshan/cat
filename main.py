
import os
import csv

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
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
from table_question_bank import TableQuestionBank

from form_login import FormLogin
from form_candidate_reg import FormCandidateReg
from form_examiner_reg import FormExaminerReg
from form_search_tests import FormSearchTests
from user import User
from crypto import Crypto
from misc import *
import config
from constants import Options, Difficulty
import constants

from test_engine import TestEngine

app = Flask(__name__)
app.secret_key = config.SECRET_KEY
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER

table_users = TableUsers()
table_candidates = TableCandidates()
table_examiners = TableExaminers()
table_tests = TableTests()
table_question_bank = TableQuestionBank()
crypto = Crypto()

test_engine = TestEngine(session)

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
                return redirect(url_for('candidate', title='', subject='All', date=''))
            elif user_data['type'] == constants.UserType.Examiner:
                return redirect(url_for('examiner'))
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
    form_reg = FormExaminerReg()
    return render_template('examiner_registration.html', form_reg=form_reg)

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
    form = FormExaminerReg(request.form)

    if form.validate():
        if table_users.get(form.username.data):
            form.username.errors.append('This username is not available.')
            return render_template('examiner_registration.html', form_reg=form)

        add_user(form.username.data, form.password.data, constants.UserType.Examiner)

        examiner_data = {
            'username'  : form.username.data,
            'first_name': form.first_name.data,
            'last_name' : form.last_name.data,
            'subject'   : ','.join(form.subject.data),
            'school'    : form.school.data,
        }
        table_examiners.add(examiner_data)
        return redirect(url_for('home'))

    return render_template('examiner_registration.html', form_reg=form)
    

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
    form_search_tests = FormSearchTests()
    data_tests = None
    candidate_data = table_candidates.get(current_user.get_id())

    if request.args:
        form_search_tests = FormSearchTests(request.args)
        data_tests = table_tests.search(
            form_search_tests.title.data,
            form_search_tests.subject.data,
            form_search_tests.date.data,
            candidate_data['standard']
        )

    return render_template(
        'candidate.html', 
        username=current_user.get_id(),
        form_search_tests=form_search_tests,
        data_tests=data_tests
    )

@app.route('/candidate/instructions')
@login_required
def instructions():
    authorized(constants.UserType.Candidate)
    test_id = request.args.get('test')
    test_info = table_tests.get_by_test_id(test_id)
    return render_template(
        'instructions.html', 
        username = current_user.get_id(),
        test_info=test_info,
        test_id=test_id
    )

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
    qb_path = os.path.join(app.config['UPLOAD_FOLDER'], qb_filename)
    uploaded_file.save(qb_path)
    res = validate_and_save_qb(new_test_id, qb_path)
    print(res)
    os.remove(qb_path)
    return redirect(url_for('examiner'))

@app.route('/examiner/get-tests', methods = ['GET'])
@login_required
def get_tests():
    username = current_user.get_id()
    data = table_tests.get_by_examiner(username)
    return jsonify(data)

@app.route('/candidate/start-test', methods=['POST'])
@login_required
def start_test():

    test_engine.start(request.form.get('test'))
    return redirect(url_for('run_test'), code=307)

@app.route('/candidate/run-test', methods=['POST'])
@login_required
def run_test():

    question = test_engine.question()
    status = {
        'question_no': session['question_no'],
        'score'      : session['score'],
        'difficulty' : session['difficulty']
    }
    return render_template(
        'test.html', 
        question=question, 
        status = status
    )

@app.route('/candidate/result', methods=['POST'])
@login_required
def test_result():

    test_engine.update(request.form.get('answer'))

    return redirect(url_for('run_test'), code=307)


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

def validate_and_save_qb(test_id, filename):

    content = []
    
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        n = 0
        for row in reader:
            if not n:
                n = 1
                continue

            if len(row) != 7:
                return 1
            if not row[5].lower() in [Options.a, Options.b, Options.c, Options.d]:
                return 2
            if not row[6].upper() in [Difficulty.Easy, Difficulty.Medium, Difficulty.Hard]:
                return 3

            row.insert(0, test_id)
            content.append(tuple(row))

    table_question_bank.add(content)
    return 0

if __name__ == '__main__':
    app.run(debug=True)
