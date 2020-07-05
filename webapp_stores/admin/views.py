from flask import Blueprint, render_template, flash, url_for
from flask_login import login_user, current_user, logout_user
from werkzeug.utils import redirect
from webapp_stores.user.model import User, db, InterestingProduct
from webapp_stores.user.forms import Login_form, Registration_user,Mailsend_off,Mailsend_on

blueprint = Blueprint('admin', __name__, url_prefix='/admin')


@blueprint.route("/admin_panel")
def admin_panel():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    title = 'Autorization'
    form = Login_form()
    return render_template('user/login.html', title=title, form=form)