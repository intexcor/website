import random

from flask import Flask, render_template, request, redirect, url_for, session, flash, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

import datetime
import os

from forms.loginforn import LoginForm
from forms.product import ProductFrom
from forms.user import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)
app.config['UPLOAD_FOLDER'] = 'static/img/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
login_manager = LoginManager()
login_manager.init_app(app)

db = SQLAlchemy(app)


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    img_prod = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True, nullable=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=True)
    phone_number = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    img_prof = db.Column(db.String, nullable=True)
    favorite_prods = db.Column(db.String, nullable=True)
    purch_prods = db.Column(db.String, nullable=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.errorhandler(404)
def not_found(_error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@app.route("/")
def index():
    products = Product.query.all()
    return render_template("index.html", products=products, title='Главная')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        if User.query.filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        if form.image_prof.data:
            image_file = form.image_prof.data
            print(image_file)
            if '.' in image_file and image_file.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']:
                filename = str(random.randint(10000000000000, 100000000000000)) + "profile.jpg"
                image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                pth = filename
            else:
                pth = "profile_image.png"
        else:
            pth = "profile_image.png"

        user = User(
            name=form.name.data,
            surname=form.surname.data,
            last_name=form.lastname.data,
            phone_number=form.phone_number.data,
            email=form.email.data,
            password=form.password.data,
            img_prof=pth,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/product', methods=['GET', 'POST'])
@login_required
def add_jobs():
    form = ProductFrom()
    if request.method == 'POST' and form.validate_on_submit():
        prod = Product()
        filename = "img.png"
        img = request.files['img_prod']
        if img and ('.' in img.filename and img.filename.rsplit('.', 1)[1].lower()
                    in app.config['ALLOWED_EXTENSIONS']):
            filename = str(random.randint(10000000000000, 100000000000000)) + "product.jpg"
        img.save(str(os.path.join(app.config['UPLOAD_FOLDER'], filename)))
        prod.img_prod = filename
        prod.name = form.name_ooo.data
        prod.description = form.description.data
        prod.price = form.price.data
        db.session.add(prod)
        db.session.commit()
        return redirect('/')
    return render_template('product.html', title='Добавление товара',
                           form=form)


@app.route('/profile')
def profile():
    return render_template("profile.html", title="Профиль")


if __name__ == '__main__':
    app.run(port=8090, host='127.0.0.1')
