import datetime
import os
import random
from flask import Flask, render_template, redirect, abort, request, jsonify

from forms.user import RegisterForm
from data import db_session, jobs_api, users_api
from data.users import User
from data.products import Product
from data.reviews import Reviews
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from forms.product import ProductFrom

from forms.loginforn import LoginForm
from flask import make_response

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)
app.config['UPLOAD_FOLDER'] = 'static/img/products'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
login_manager = LoginManager()
login_manager.init_app(app)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/product/<int:id_pr>', methods=['GET', 'POST'])
def prosm_prods(id_pr):
    db_sess = db_session.create_session()
    product = db_sess.query(Product).filter(Product.id == id_pr).first()
    print(product)
    return render_template('product_item.html', prod=product, title='dgsgdssd')


@app.route('/product', methods=['GET', 'POST'])
def add_prods():
    form = ProductFrom()
    if request.method == 'POST' and form.validate_on_submit():
        db_sess = db_session.create_session()
        prod = Product()
        img = request.files['img_prod']
        print(request.files)
        if img.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
            filename = str(random.randint(10000000000000, 100000000000000)) + "product.jpg"
            img.save(str(os.path.join(app.config['UPLOAD_FOLDER'], filename)))
            prod.img_prod = filename
        prod.name = form.name_ooo.data
        prod.description = form.description.data
        prod.price = form.price.data
        db_sess.add(prod)
        db_sess.commit()
        return redirect('/')
    return render_template('product.html', title='Добавление товара',
                           form=form)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    producti = db_sess.query(Product).all()
    return render_template("index.html", products=producti, title='Главная')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
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


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    return render_template('profile.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    # if request.method == 'POST':
    #     img = request.files['img_prod']
    #     db_sess = db_session.create_session()
    #     print(img)
    #     form = request.form
    #
    #     user = User(
    #         name=form.name.data,
    #         surname=form.surname.data,
    #         last_name=form.lastname.data,
    #         phone_number=form.phone_number.data,
    #         email=form.email.data,
    #         password=form.password.data,
    #         img_prof=form.image_prof.data,
    #     )
    #     user.set_password(form.password.data)
    #     db_sess.add(user)
    #     db_sess.commit()
    #     return redirect('/login')
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        db_sess = db_session.create_session()
        user = User()
        img = request.files['image_prof']

        user.name = form.name.data
        user.email = form.email.data
        user.surname = form.surname.data
        user.last_name = form.lastname.data
        user.email = form.email.data
        user.password = form.password.data

        if img.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
            filename = str(random.randint(10000000000000, 100000000000000)) + "product.jpg"
            img.save(str(os.path.join(app.config['UPLOAD_FOLDER'], filename)))
            user.img_prof = filename

        # print(img)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


def main():
    app.run(port=8000)


if __name__ == '__main__':
    db_session.global_init("db/ggbd.db")
    main()
