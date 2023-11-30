from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import desc
from flask import redirect,flash
from flask import url_for
from flask_login import login_required
from flask_login import current_user
from flask_admin import expose
from functools import wraps


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    @login_required
    def admin_main(self):
        from models import User
        users = User.query.order_by(desc(User.date)).all()
        return self.render('admin/index.html', users=users)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        flash('you not admin')
        return redirect(url_for('login'))



class MyModelView(ModelView):
    column_labels = {
        'username': 'Логин',
        'password': 'Пароль',
        'name': 'ФИО',
        'email': 'Почта',
        'phone': 'Телефон',
        'date': 'Дата',
        'doctor': 'Врач',
        'message': 'Сообщение', }

    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Вы не авторизованы')
            return redirect(url_for('login'))
        if not current_user.has_role('admin'):
            flash('Вы не администратор!')
            return redirect(url_for('account'))
        return f(*args, **kwargs)
    return decorated_function
