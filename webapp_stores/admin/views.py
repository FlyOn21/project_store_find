from flask import Blueprint, render_template, flash, url_for, current_app, request
from flask_login import login_user, current_user, logout_user
from werkzeug.utils import redirect
from webapp_stores.user.model import User, db, InterestingProduct
from webapp_stores.admin.form import Valid_mail

blueprint = Blueprint('admin', __name__, url_prefix='/admin')


@blueprint.route("/admin_panel")
def admin_panel():
    """Формирование словаря для панели администратора"""
    title = 'Панель админимтратора'


    with current_app.app_context():
        users_all = User.query.all()
        users_id = []
        for user in users_all:
            step_one = (str(user).split(','))[0]
            step_two = (step_one.split(':'))[1]
            users_id.append(step_two)
        # print("----",users_id,"----")
        all_user = []
        for i in users_id:
            current_user_dict = {}
            user = User.query.filter_by(id=i).first()
            # print(user)

            current_user_dict['id'] = user.id
            current_user_dict['user'] = user.username
            current_user_dict['mail'] = user.email
            current_user_dict['name'] = user.name
            current_user_dict['surname'] = user.surname
            current_user_dict['role'] = user.role
            form_m = Valid_mail()
            if user.role == 'user':
                current_user_dict['role_alternative'] = 'admin'
            else:
                current_user_dict['role_alternative'] = 'user'
            current_user_dict['active'] = user.is_active
            if user.is_active == True:
                current_user_dict['active_alternative'] = False
            else:
                current_user_dict['active_alternative'] = True
            current_user_dict['send_mail'] = user.send_mail
            if user.send_mail == True:
                current_user_dict['send_mail_alternative'] = False
            else:
                current_user_dict['send_mail_alternative'] = True
            all_user.append(current_user_dict)
        print(all_user)

    return render_template('admin/admin_panel.html', title=title, users=all_user)


@blueprint.route("/changes", methods=['POST'])
def changes():
    # user_cange = {}
    # user_cange['id'] = request.form['id']
    # user_cange['user'] = request.form['username']
    # user_cange['mail'] = request.form['mail']
    # user_cange['name'] = request.form['name']
    # user_cange['surname'] = request.form['surname']
    # user_cange['role'] = request.form['role']
    # user_cange['active'] = request.form['active']
    # user_cange['send_mail'] = request.form['send_mail']
    # print("------------------",user_cange,"------------------")
    user_change = User.query.filter_by(id = request.form['id']).first()
    user_change.username = request.form['username']
    user_change.email = request.form['mail']
    user_change.name = request.form['name']
    user_change.surname = request.form['surname']
    user_change.role = request.form['role']
    if request.form['active'] == 'True':
        user_change.is_active = 1
    else:
        user_change.is_active = 0
    if request.form['send_mail'] == 'True':
        user_change.send_mail = 1
    else:
        user_change.send_mail = 0
    db.session.add(user_change)
    db.session.commit()
    return redirect(url_for('admin.admin_panel'))

@blueprint.route("/delete_user", methods=['POST'])
def delete_user():
    user_del = User.query.filter(User.id == int(request.form['user_to_delete'])).first()
    products = user_del.interesting_products
    for product in products:
        db.session.delete(product)
        db.session.commit()
        # print("-------",product)
    db.session.delete(user_del)
    db.session.commit()
    return redirect(url_for('admin.admin_panel'))




