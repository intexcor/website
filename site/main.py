import datetime
import os

import jwt
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)
app.config['UPLOAD_FOLDER'] = 'static/img/avatars'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

db = SQLAlchemy(app)  # Создаем экземпляр SQLAlchemy


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    token = db.Column(db.String(100), unique=True, nullable=False)
    avatar = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(100), nullable=False)


# Пример данных в базе данных для тестирования
# Замените их реальными данными из вашей базы данных
# Создание тестовых данных при создании приложения
with app.app_context():
    db.create_all()

    # Пример данных для тестирования
    # product1 = Product(name='Product 1', description='Description for product 1', price=10.99, image='product1.jpg')
    # product2 = Product(name='Product 2', description='Description for product 2', price=19.99, image='product2.jpg')
    # product3 = Product(name='Product 3', description='Description for product 3', price=15.49, image='product3.jpg')
    #
    # db.session.add_all([product1, product2, product3])
    # db.session.commit()


#     user = User(username='admin', password='admin_password')
#     db.session.add(user)
#     db.session.commit()


@app.route('/')
@app.route('/index')
def index():
    products = Product.query.all()  # Получаем все товары из базы данных
    # Проверяем, вошел ли пользователь в систему
    if 'token' in session and session['token']:
        # Если пользователь вошел в систему, отображаем его информацию
        user = User.query.filter_by(token=session['token']).first()
        user_name = user.username

        return render_template('index.html', user_name=user_name, token=session['token'], products=products)
    else:
        # Если пользователь не вошел в систему, отображаем кнопку входа
        return render_template('index.html', products=products)


@app.route('/purchases')
def purchases():
    return render_template('purchases.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Проверяем, существует ли пользователь с таким именем и паролем в базе данных
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['token'] = user.token
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error_message='Неверное имя пользователя или пароль')

    return render_template('login.html')


# Добавляем обработчик для страницы регистрации
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        avatar = request.files['avatar'] if 'avatar' in request.files else None

        # Проверяем, существует ли пользователь с таким именем уже в базе данных
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            error_message = 'Пользователь с таким именем уже существует'
            return render_template('register.html', error_message=error_message)

        token = jwt.encode({"username": username}, app.config['SECRET_KEY'],
                           algorithm='HS256')

        filename = "img.png"

        if avatar and ('.' in avatar.filename and avatar.filename.rsplit('.', 1)[1].lower()
                       in app.config['ALLOWED_EXTENSIONS']):
            filename = token[-20:-1] + token[-1] + ".jpg"
            avatar.save(str(os.path.join(app.config['UPLOAD_FOLDER'], filename)))

        # Создаем нового пользователя и сохраняем его в базе данных
        new_user = User(username=username, token=token, avatar=filename, password=password)
        db.session.add(new_user)
        db.session.commit()

        session['token'] = token
        # Перенаправляем пользователя на страницу входа
        return redirect(url_for('index'))

    return render_template('register.html')


@app.route('/logout')
def logout():
    # Удаляем данные о пользователе из сессии
    session.pop('token', None)
    # Перенаправляем пользователя на страницу входа или на главную страницу
    return redirect(url_for('login'))


@app.route('/upload_avatar', methods=['POST'])
def upload_avatar():
    if 'avatar' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['avatar']

    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and ('.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']):
        token = session['token']
        filename = token[-20:-1] + token[-1] + ".jpg"
        file.save(str(os.path.join(app.config['UPLOAD_FOLDER'], filename)))
        # Далее можно сохранить путь к файлу в базу данных для конкретного пользователя
        # Например, если есть модель User, то можно обновить поле user.avatar = filename
        # Затем перенаправить пользователя на страницу профиля или обновить текущую страницу
        return redirect(url_for('profile'))
    else:
        flash('Allowed file types are png, jpg, jpeg, gif')
        return redirect(request.url)


@app.route('/profile')
def profile():
    token = session['token']
    user = User.query.filter_by(token=token).first()
    user_name = user.username
    return render_template('profile.html', user_name=user_name, user_avatar=user.avatar,
                           token=token)


@app.route('/clear_cache')
def clear_cache():
    session.pop('token', None)
    return "Cache cleared"


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
