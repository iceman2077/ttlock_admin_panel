from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from concurrent.futures import as_completed, ThreadPoolExecutor
from datetime import datetime
from .api_requests import lock_list, list_passwords, unlock_records, unlock_records_one_day, create_password
from .models import User
import json

main = Blueprint('main', __name__)


@main.route('/')
@login_required
def index():
    user = User.query.filter_by(uid=current_user.uid).first()
    locks = lock_list(user.access_token, 1)
    return render_template('index.html', locks=[locks.json()["list"][x] for x in range(len(locks.json()["list"]))])


@main.route('/locks')
@login_required
def unlock_records_all():
    user = User.query.filter_by(uid=current_user.uid).first()
    locks = lock_list(user.access_token, 1)
    all_locks_id = []
    for i in range(len(locks.json()["list"])):
        all_locks_id.append(locks.json()["list"][i]["lockId"])
    all_unlock_records = []
    with ThreadPoolExecutor(max_workers=5) as pool:
        future_to_unlock_records = {pool.submit(unlock_records_one_day, user.access_token, lock_id, 1): lock_id for lock_id in all_locks_id}
        for unlock_record in as_completed(future_to_unlock_records):
            if unlock_record.result().json()['total'] != 0:
                all_unlock_records.extend(unlock_record.result().json()["list"])
    all_unlock_records_sorted = sorted(all_unlock_records, key=lambda k: k.get('serverDate', 0), reverse=True)
    return render_template('unlock_records.html', unlock_records=[all_unlock_records_sorted[x] for x in range(len(all_unlock_records_sorted))])


@main.route("/unlock/<lockId>")
@login_required
def get_unlock_records(lockId):
    user = User.query.filter_by(uid=current_user.uid).first()
    unlock_records_responce = unlock_records(user.access_token, lockId, 1)
    return render_template('unlock_records.html', unlock_records=[unlock_records_responce.json()["list"][x] for x in range(len(unlock_records_responce.json()["list"]))])


@main.route("/password/<lockId>")
@login_required
def get_lock_passwords(lockId):
    lockId = lockId
    user = User.query.filter_by(uid=current_user.uid).first()
    passwords = list_passwords(user.access_token, lockId, 1)
    return render_template('passwords.html', passwords=[passwords.json()["list"][x] for x in range(len(passwords.json()["list"]))])


@main.route("/create_password/<lockId>")
@login_required
def create_lock_passwords(lockId):
    return render_template('create_password.html', lockId=lockId)


def convet_time_to_timestamp(time):
    print(time)
    date_processing = time.replace('T', '-').replace(':', '-').split('-')
    date_processing = [int(v) for v in date_processing]
    date_out = datetime(*date_processing)
    return int(date_out.timestamp() * 1e3)


@login_required
@main.route('/create_password/<lockId>', methods=['POST'])
@login_required
def create_lock_passwords_post(lockId):
    lockId = lockId
    user = User.query.filter_by(uid=current_user.uid).first()
    keyboardPwd = request.form.get('keyboardPwd')
    password = request.form.get('password')
    startDate = convet_time_to_timestamp(request.form.get('startDate'))
    endDate = convet_time_to_timestamp(request.form.get('endDate'))
    password = create_password(user.access_token, lockId, password, keyboardPwd,  startDate, endDate)
    print(password.content)
    return redirect(url_for('main.index'))
