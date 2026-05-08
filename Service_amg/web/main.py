from flask import Flask, render_template, redirect
from forms.register_form import RegisterForm
from data import db_session
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/register', methods=["GET", "POST"])
def register():
    form_register = RegisterForm()
    if form_register.validate_on_submit():
        if form_register.password.data != form_register.repeat_password.data:
            return render_template('registration.html', message='Пароли не совпадают', form=form_register,
                                   title='Регистрация')
        session_db = db_session.create_session()
        if session_db.query(User).filter(User.email == form_register.email.data).first():
            return render_template('registration.html', message='Такой пользователь уже существует', form=form_register,
                                   title='Регистрация')
        user = User(
            name=form_register.name.data,
            surname=form_register.surname.data,
            age=form_register.age.data,
            phone=form_register.position.data,
            email=form_register.email.data
        )
        user.set_password(form_register.password.data)
        session_db.add(user)
        session_db.commit()
        return redirect('/login')
    return render_template('registration.html', form=form_register, title='Регистрация')


if __name__ == '__main__':
    db_session.global_init("data.db")
    app.run(port=8080, host='127.0.0.1')
