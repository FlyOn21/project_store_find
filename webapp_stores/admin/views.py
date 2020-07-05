from flask import Blueprint, render_template, flash, url_for,current_app,request
from flask_login import login_user, current_user, logout_user
from werkzeug.utils import redirect
from webapp_stores.user.model import User, db, InterestingProduct


blueprint = Blueprint('admin', __name__, url_prefix='/admin')


@blueprint.route("/admin_panel")
def admin_panel():
    """Формирование словаря для панели администратора"""
    title = 'Панель админимтратора'
    with current_app.app_context():
        count = User.query.count()
        all_user = []
        for i in range(1,(count+1)):
            current_user_dict = {}
            user = User.query.filter_by(id=i).first()
            print(user)
            current_user_dict['id'] = user.id
            current_user_dict['user'] = user.username
            current_user_dict['mail'] = user.email
            current_user_dict['name'] = user.name
            current_user_dict['surname'] = user.surname
            current_user_dict['role'] = user.role
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
        user_s = 'user'
    return render_template('admin/admin_panel.html', title=title, users = all_user)

# @blueprint.route("/changes", methods=['POST'])
# def changes():
#     id =
#     role = request.form['role']




if __name__ =="__main__":
    admin_panel()