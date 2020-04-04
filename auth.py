from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from .api_requests import get_token, refresh_tocken
from .models import User
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('email')
    password = request.form.get('password')
    # password = hashlib.md5(request.form.get('password').encode('utf-8')).hexdigest()
    remember = True if request.form.get('remember') else False

    request_user_ttlock = get_token(username, password)
    flash(request_user_ttlock.json()['expires_in'])
    if request_user_ttlock is None:
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))  # if user doesn't exist or password is wrong, reload the page
    expire_in = request_user_ttlock.json()['expires_in']
    check_username = User.query.filter_by(username=username).first()
    if check_username:  # if a user is found, we want to redirect back to signup page so user can try again
        if expire_in < 432000:
            refresh_tocken_ttlock = refresh_tocken(request_user_ttlock.json()['refresh_tocken'])
            check_username.access_token = refresh_tocken_ttlock.json()['access_token']
            check_username.expires_in = refresh_tocken_ttlock.json()['expires_in']
            check_username.refresh_token = refresh_tocken_ttlock.json()['refresh_token']
            db.session.commit()
    else:
        new_user = User(
            username=username,
            uid=request_user_ttlock.json()['uid'],
            password=password,
            access_token=request_user_ttlock.json()['access_token'],
            openid=request_user_ttlock.json()['openid'],
            scope=request_user_ttlock.json()['scope'],
            refresh_token=request_user_ttlock.json()['refresh_token'],
        )
        db.session.add(new_user)
        db.session.commit()

    user = User.query.filter_by(username=username).first()
    login_user(user, remember=remember)
    return redirect(url_for('main.index'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
