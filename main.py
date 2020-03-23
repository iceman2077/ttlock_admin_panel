from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .api_requests import lock_list, list_passwords, unlock_records, get_all_unlock_records
from .models import User
import json

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    user = User.query.filter_by(uid=current_user.uid).first()
    locks = lock_list(user.access_token, 1)
    return render_template('index.html',locks=[locks.json()["list"][x] for x in range(len(locks.json()["list"]))])

@main.route('/locks')
@login_required
def unlock_records_all():
    user = User.query.filter_by(uid=current_user.uid).first()
    unlock_records_resp = get_all_unlock_records(user.access_token)
    return render_template('unlock_records.html', unlock_records=[unlock_records_resp[x][0] for x in range(len(unlock_records_resp))])

@main.route("/unlock/<lockId>")
@login_required
def unlock_records(lockId):
    user = User.query.filter_by(uid=current_user.uid).first()
    unlock_records_resp = unlock_records(user.access_token, lockId, 1)
    return render_template('unlock_records.html', unlock_records=[unlock_records_resp.json()["list"][x] for x in range(len(unlock_records_resp.json()["list"]))])

@main.route("/password/<lockId>")
@login_required
def lock_passwords(lockId):
    lockId = lockId
    user = User.query.filter_by(uid=current_user.uid).first()
    passwords = list_passwords(user.access_token, lockId, 1)
    return render_template('passwords.html',passwords=[passwords.json()["list"][x] for x in range(len(passwords.json()["list"]))])


