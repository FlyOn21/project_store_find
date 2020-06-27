from getpass import getpass # ВВод пароля из командной строки
import sys
from webapp_stores import create_app
from webapp_stores.stores.model import db
from webapp_stores.user.model import User

app = create_app()
with app.app_context():
    name = input('input name: ')
    surname = input('input surname: ')
    username = input('input login: ')
    email = input('Input e-mail: ')
    if User.query.filter(User.username == username, User.name==name,User.surname==surname).count():
        print('User is exist')
        sys.exit(0)
    password_1 = getpass('Input password: ')
    password_2 = getpass('Confirm password: ')

    if not password_1 == password_2:
        print('password is not confirm')
        sys.exit(0)
    new_user = User(username = username, role = 'admin',is_active=True,name = name, surname = surname)
    new_user.save_password(password_1)

    db.session.add(new_user)
    db.session.commit()
    print(f'Creature new user {username}')