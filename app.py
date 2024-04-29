import datetime
import os
import random
from flask import Flask, render_template, redirect, abort, request, jsonify

from forms.user import RegisterForm
from data import db_session, product_api, users_api
from data.users import User
from data.products import Product
from data.reviews import Reviews
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from forms.product import ProductFrom
from forms.review import ReviewForm
from forms.buying import BuyingForm
from forms.buying_all import BuyingAllForm

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


@app.route('/product/<int:id_pr>',  methods=['GET', 'POST'])
def prosm_prods(id_pr):
    db_sess = db_session.create_session()
    product = db_sess.query(Product).filter(Product.id == id_pr).first()
    return render_template('product_item.html', prod=product, title='dgsgdssd')


@app.route('/product',  methods=['GET', 'POST'])
def add_prods():
    form = ProductFrom()
    if request.method == 'POST' and form.validate_on_submit():
        db_sess = db_session.create_session()
        prod = Product()
        img = request.files['img_prod']
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


@app.route('/korzina/<int:id_pr>',  methods=['GET', 'POST'])
@login_required
def korz_add(id_pr):
    db_sess = db_session.create_session()
    us = db_sess.query(User).filter(User.id == current_user.id).first()
    if not us.korzina:
        us.korzina = f'{id_pr}#1'
    else:
        spis = us.korzina.split(', ')
        spis_ = [i.split('#') for i in spis]
        spisi = []
        f = True
        for i in spis_:
            if str(id_pr) == i[0]:
                spisi.append(f'{i[0]}#{str(int(i[1]) + 1)}')
                f = False
            else:
                spisi.append(f'{i[0]}#{i[1]}')
        if f:
            spisi.append(f'{id_pr}#1')
        us.korzina = ', '.join(spisi)
    db_sess.commit()
    return redirect(f'/product/{id_pr}')


@app.route('/korzina_delete/<int:id_pr>',  methods=['GET', 'POST'])
@login_required
def korz_delete(id_pr):
    db_sess = db_session.create_session()
    us = db_sess.query(User).filter(User.id == current_user.id).first()
    if us.korzina is None:
        redirect('/korzina')
    else:
        spis = us.korzina.split(', ')
        spis_ = [i.split('#') for i in spis]
        spisi = []
        f = True
        for i in spis_:
            if str(id_pr) != i[0]:
                spisi.append(f'{i[0]}#{i[1]}')
        us.korzina = ', '.join(spisi)
    db_sess.commit()
    return redirect('/korzina')


@app.route('/korzina',  methods=['GET', 'POST'])
@login_required
def korz_all():
    db_sess = db_session.create_session()
    us = db_sess.query(User).filter(User.id == current_user.id).first()
    slov = {}
    print(us.korzina)
    if us.korzina:
        spis_ids = [i.split('#')[0] for i in us.korzina.split(', ')]
        korz_t = db_sess.query(Product).filter(Product.id.in_(spis_ids)).all()
        slov_k = dict([i.split('#') for i in us.korzina.split(', ')])
        for i in korz_t:
            slov[i] = slov_k[str(i.id)]
        print(slov)
    return render_template('korzina.html', korz=slov.items())


@app.route('/korzina_add/<int:id>/<string:plus>',  methods=['GET', 'POST'])
@login_required
def korz_add_minus(id, plus):
    print(plus, type(plus))
    db_sess = db_session.create_session()
    us = db_sess.query(User).filter(User.id == current_user.id).first()
    spis = us.korzina.split(', ')
    spis_ = [i.split('#') for i in spis]
    spisi = []
    f = True
    for i in spis_:
        if str(id) == i[0]:
            spisi.append(f'{i[0]}#{str(int(i[1]) + int(plus))}')
            f = False
        else:
            spisi.append(f'{i[0]}#{i[1]}')
    if f:
        spisi.append(f'{id}#1')
    us.korzina = ', '.join(spisi)
    db_sess.commit()
    return redirect('/korzina')


@app.route('/buying/<int:id_pr>',  methods=['GET', 'POST'])
@login_required
def buying(id_pr):
    form = BuyingForm()
    db_sess = db_session.create_session()
    product = db_sess.query(Product).filter(Product.id == id_pr).first()
    if request.method == 'POST' and form.validate_on_submit():
        db_sess = db_session.create_session()
        us = db_sess.query(User).filter(User.id == current_user.id).first()
        if us.purch_prods is None:
            us.purch_prods = f'{id_pr}'
        else:
            us.purch_prods += f', {id_pr}'
        db_sess.commit()
        return redirect('/')
    return render_template('buying.html', title='Покупка',
                           form=form, price=product.price)


@app.route('/buying_korz',  methods=['GET', 'POST'])
@login_required
def buyingAll():
    form = BuyingAllForm()
    db_sess = db_session.create_session()
    us = db_sess.query(User).filter(User.id == current_user.id).first()
    slov = {}
    if us.korzina:
        spis_ids = [i.split('#')[0] for i in us.korzina.split(', ')]
        korz_t = db_sess.query(Product).filter(Product.id.in_(spis_ids)).all()
        slov_k = dict([i.split('#') for i in us.korzina.split(', ')])
        for i in korz_t:
            slov[i] = slov_k[str(i.id)]
    sum = 0
    for i, j in slov.items():
        sum += i.price * int(j)
    if request.method == 'POST' and form.validate_on_submit():
        db_sess = db_session.create_session()
        us = db_sess.query(User).filter(User.id == current_user.id).first()
        spis_ids = [f', {i.id}' * int(j) for i, j in slov.items()]
        print(spis_ids)
        if us.purch_prods is None:
            us.purch_prods = f'{''.join(spis_ids)}'
        else:
            us.purch_prods += f'{''.join(spis_ids)}'
        us.korzina = None
        db_sess.commit()
        return redirect('/')
    return render_template('buying_all.html', title='Покупка',
                           form=form, price=sum)


@app.route('/add_review/<int:id_pr>',  methods=['GET', 'POST'])
@login_required
def add_review(id_pr):
    if current_user.purch_prods and str(id_pr) in current_user.purch_prods.split(', '):
        form = ReviewForm()
        if request.method == 'POST' and form.validate_on_submit():
            db_sess = db_session.create_session()
            rew = Reviews()
            img = request.files['img_rev']
            if img.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
                filename = str(random.randint(10000000000000, 100000000000000)) + "review.jpg"
                img.save(str(os.path.join('static/img/reviews', filename)))
                rew.img_rew = filename
            rew.text_rew = form.text.data
            rew.id_prod = id_pr
            rew.id_user = current_user.id
            db_sess.add(rew)
            db_sess.commit()
            return redirect(f'/reviews/{id_pr}')
        return render_template('add_rev.html', title='Добавление отзыва',
                               form=form, id_pr=id_pr)
    else:
        return render_template('error_review.html', title='Не куплен товар', id_pr=id_pr)


@app.route("/", methods=['GET', 'POST'])
def index():
    db_sess = db_session.create_session()
    producti = db_sess.query(Product).all()
    if request.method == 'POST':
        db_sess = db_session.create_session()
        producti = db_sess.query(Product).filter(Product.name.like(f'%{request.form['search']}%')).all()
        return render_template("index.html", products=producti, title='Главная')
    return render_template("index.html", products=producti, title='Главная')


@app.route("/reviews/<int:id_pr>", methods=['GET', 'POST'])
def reviews(id_pr):
    db_sess = db_session.create_session()
    product = db_sess.query(Product).get(id_pr)
    rews = db_sess.query(Reviews).filter(Reviews.id_prod == product.id).all()
    return render_template("reviews.html", reviews=rews, title=f'Отзывы на товар {product.name}', prod=product.id)


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


@app.route('/profile')
def profile():
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    return render_template('profile.html', user=user)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        img = request.files['image_prof']
        if img.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
            filename = str(random.randint(10000000000000, 100000000000000)) + "user.jpg"
            img.save(str(os.path.join('static/img/users', filename)))
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            last_name=form.lastname.data,
            phone_number=form.phone_number.data,
            email=form.email.data,
            password=form.password.data,
            img_prof=filename,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


def main():
    app.register_blueprint(product_api.blueprint)
    app.register_blueprint(users_api.blueprint)
    app.run(port=8080)


if __name__ == '__main__':
    db_session.global_init("db/ggbd.db")
    main()
