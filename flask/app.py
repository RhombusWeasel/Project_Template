from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, request, session, redirect, url_for, jsonify
from itsdangerous import URLSafeTimedSerializer
from utils.db import Database
from flask_cors import CORS
from functools import wraps
from time import time
import configparser
import logging
import json
import re

log = logging.getLogger('werkzeug')

conf = configparser.ConfigParser()
conf.read('config.ini')
admin_list = conf['admin']['admin_list'].split(',') if 'admin_list' in conf['admin'] else []
trusted_list = conf['admin']['trusted_list'].split(',') if 'trusted_list' in conf['admin'] else []
white_list = conf['admin']['white_list'].split(',') if 'white_list' in conf['admin'] else []

app = Flask(__name__)
app.secret_key = 'your_secret_key'
CORS(app, resources={r"*": {"origins": "*"}})

user_db = Database('users.db')
user_db.create_table('users')
user_db.add_column_to_table('users', 'password', 'TEXT')
user_db.add_column_to_table('users', 'permissions', 'TEXT')
user_db.add_column_to_table('users', 'last_login', 'DATETIME')

s = URLSafeTimedSerializer(app.secret_key)

def check_permissions(username, perm):
    perms = json.loads(user_db.load_data('users', username)['permissions'])
    return perms[perm]

# Decorator to check if the user is logged in, put under your routes that require to be logged in.
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return 'You must be logged in to view this page.', 401
        return f(*args, **kwargs)
    return decorated_function


# Decorator to check if the user has trusted status, put under your routes that require trusted status.
def trusted_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session or session['username'] not in trusted_list:
            if not check_permissions(session['username'], 'trusted'):
                return 'You must be trusted to view this page.', 401
        elif 'username' in session and session['username'] in admin_list:
            return f(*args, **kwargs)
        return f(*args, **kwargs)
    return decorated_function


# Decorator to check if the user is an admin, put under your routes that require admin privileges.
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session or session['username'] not in admin_list:
            if not check_permissions(session['username'], 'admin'):
                return 'You must be an admin to view this page.', 401
        return f(*args, **kwargs)
    return decorated_function


# Store failed login attempts and the time of the last attempt
login_attempts = {}


@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    return jsonify({'message': 'Alive'}), 200


@app.route('/user_login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']

    # Account lockout mechanism
    if (username in login_attempts and
            login_attempts[username]['count'] >= 3 and
            time() - login_attempts[username]['last_attempt'] < 60 * 5):  # Lockout time: 5 minutes
        return 'Account locked. Please try again later.', 403

    user_data = user_db.load_data('users', username)
    if user_data and check_password_hash(user_data['password'], password):
        session['username'] = username
        return jsonify(user_data['permissions']), 200
    else:
        if username not in login_attempts:
            login_attempts[username] = {'count': 1, 'last_attempt': time()}
        else:
            login_attempts[username]['count'] += 1
            login_attempts[username]['last_attempt'] = time()
        return 'Invalid username or password', 401


@app.route('/user_register', methods=['POST'])
def register():
    username = request.json['username']
    password = generate_password_hash(
        request.json['password'], method='scrypt')

    if not re.match(r"[^@]+@[^@]+\.[^@]+", username):  # Basic email validation
        return 'Invalid email address', 401

    if user_db.load_data('users', username) is None:
        print('username: %s added to database.', username)
        user_db.save_data('users', username, 'password', password)
        perms = {
            "admin": True if username in admin_list else False,
            "trusted": True if username in trusted_list else False,
            "user": True
        }
        user_db.save_data('users', username, 'permissions', json.dumps(perms))
        return redirect('/'), 200

    return 'An error occurred while registering the user', 500


@app.route('/user_logout', methods=['GET'])
@login_required
def logout():
    session.pop('username', None)
    return "True", 200


@app.route('/user_permissions', methods=['GET'])
@login_required
def get_permissions():
    username = session['username']
    user_data = user_db.load_data('users', username)
    return jsonify(json.loads(user_data['permissions'])), 200


@app.route('/reset_password', methods=['POST'])
def reset_password():
    username = request.json['username']
    user_data = user_db.load_data('users', username)

    if user_data is not None:
        token = s.dumps(username, salt='password-reset-salt')
        # In a real-world application, send this token to the user's email address,
        # then they would use it to confirm their identity and reset their password.
        return f'Password reset token: {token}'
    return 'Invalid username'


@app.route('/confirm_reset/<token>', methods=['POST'])
def confirm_reset(token):
    if request.method == 'POST':
        try:
            username = s.loads(token, salt='password-reset-salt', max_age=3600)
        except:
            return 'The password reset link is invalid or has expired.'

        user_data = user_db.load_data('users', username)
        if user_data is not None:
            new_password = generate_password_hash(request.json['password'])
            user_db.save_data('users', username, 'password', new_password)
            return redirect(url_for('login'))
        return 'Invalid username'


def modify_permissions(username, perm, value):
    perms = json.loads(user_db.load_data('users', username)['permissions'])
    perms[perm] = value
    user_db.save_data('users', username, 'permissions', json.dumps(perms))


def check_user(username):
    udata = user_db.get_table('users')
    for user in udata:
        if user['_id'] == username:
            return True
    return False


@app.route('/grant_perms', methods=['POST'])
@admin_required
def grant_perms():
    username = request.json['username']
    perm = request.json['perm']
    print(user_db.get_table('users'))
    if not check_user(username):
        return f'{username} is not a user.', 200
    else:
        modify_permissions(username, perm, True)
    return f'{username} now has {perm} permissions.', 200


@app.route('/revoke_perms', methods=['POST'])
@admin_required
def revoke_perms():
    username = request.json['username']
    perm = request.json['perm']
    if session['username'] == username and perm == 'admin':
        return 'You cannot revoke your own permissions.', 200
    if not check_user(username):
        return f'{username} is not a user.', 200
    else:
        modify_permissions(username, perm, False)
    return f'{username} no longer has {perm} permissions.', 200


@app.route('/get_users')
@admin_required
def get_users():
    return jsonify(user_db.get_table('users')), 200

# Additional endpoints can be added here.


if __name__ == '__main__':
    app.run(debug=True)
