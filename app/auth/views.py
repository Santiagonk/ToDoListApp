from app.models import UserData
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user

from app.forms import LoginForm

from . import auth
from app.firestore_service import get_user
from app.models import UserData, UserModel

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    login_form = LoginForm()
    context = {
        'login_form': login_form
    }

    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data

        user_doc = get_user(username)

        if user_doc.to_dict() is not None:
            password_from_db = user_doc.to_dict()['password']

            if password_from_db == password:
                user_data = UserData(username, password)
                user = UserModel(user_data)

                login_user(user)

                flash('Bienvenido de Nuevo')

                redirect(url_for('hello'))

                flash('Informacion no coincide')

        else:
            flash('El usuario no existe')


        return redirect(url_for('index'))

    return render_template('login.html',  **context)

@auth.route('logout')
@login_required
def logout():
    logout_user()
    flash('Regresa pronto')

    return redirect(url_for('auth.login'))