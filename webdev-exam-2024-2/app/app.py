from flask import Flask, render_template, flash, request, redirect, url_for, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
import datetime
from werkzeug.security import check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import YEAR

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

class Books(db.Model):
    __tablename__ = 'books'
    
    id = db.Column(db.INT, primary_key=True) 
    name = db.Column(db.VARCHAR(100)) # VARCHAR
    description = db.Column(db.TEXT) # TEXT
    year = db.Column(db.Date) # YEAR 
    publishing_house = db.Column(db.VARCHAR(100)) # VARCHAR
    author = db.Column(db.VARCHAR(100)) # VARCHAR
    pages = db.Column(db.INT) # INT
    cover = db.Column(db.INT, db.ForeignKey('covers.id')) # Внешний ключ

    def __repr__(self):
        return f"<books {self.id}>"

class Covers(db.Model):
    __tablename__ = 'covers'

    id = db.Column(db.INT, primary_key=True) 
    name = db.Column(db.VARCHAR(100)) # VARCHAR
    mime_type = db.Column(db.VARCHAR(100)) # VARCHAR
    md5_hash = db.Column(db.VARCHAR(100)) # VARCHAR
    
    def __repr__(self):
        return f"<covers {self.id}>"

class Genres(db.Model):
    __tablename__ = "genres"
    
    id = db.Column(db.INT, primary_key=True) 
    name = db.Column(db.VARCHAR(100)) # VARCHAR

    def __repr__(self):
        return f"<genres {self.id}>"

class BooksAndGenres(db.Model):
    __tablename__ = 'books_and_genres'
    
    id = db.Column(db.INT, primary_key=True) 
    book = db.Column(db.INT, db.ForeignKey('books.id')) # Внешний ключ
    genre =  db.Column(db.INT, db.ForeignKey('genres.id')) # Внешний ключ
    
    def __repr__(self):
        return f"<books_and_genres {self.id}>"

class Reviews(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.INT, primary_key=True) 
    book = db.Column(db.INT, db.ForeignKey('books.id')) # Внешний ключ
    user = db.Column(db.INT, db.ForeignKey('users.id')) # Внешний ключ
    grade = db.Column(db.INT) # INT
    text = db.Column(db.TEXT) # TEXT
    date = db.Column(db.Date, default = datetime.datetime.date) # DATE
    
    def __repr__(self):
        return f"<reviews {self.id}>"
    
class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.INT, primary_key=True) 
    login = db.Column(db.VARCHAR(100)) # VARCHAR
    password_hash = db.Column(db.VARCHAR(200)) # VARCHAR
    name = db.Column(db.VARCHAR(100)) # VARCHAR
    surname = db.Column(db.VARCHAR(100)) # VARCHAR
    patronymic  = db.Column(db.VARCHAR(100)) # VARCHAR
    role = db.Column(db.INT, db.ForeignKey('roles.id')) # Внешний ключ
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_role(self):
        return self.role
    
    @property
    def full_name(self):
        return ' '.join([self.surname, self.name, self.patronymic or ''])
    
    @property
    def is_admin(self):
        return self.role == 1
    
    @property    
    def is_moderator(self):
        return self.role == 2
    
    @property
    def is_user(self):
        return self.role == 3
    
    def __repr__(self):
        return f"<users {self.id}>"
    
class Roles(db.Model):
    __tablename__ = 'roles'
    
    id = db.Column(db.INT, primary_key=True) 
    name = db.Column(db.VARCHAR(100)) # VARCHAR
    text = db.Column(db.TEXT) # TEXT
    
    def __repr__(self):
        return f"<roles {self.id}>"

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message = 'У вас недостаточно прав для выполнения данного действия'
login_manager.login_message_category = 'danger'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    user = db.session.execute(db.select(Users).filter_by(id=user_id)).scalar()
    return user

@app.route('/')
def index():
    print()
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        remember = request.form.get('remember')
        user = db.session.execute(db.select(Users).filter_by(login=login)).scalar()
        if user and user.check_password(password):
            login_user(user, remember=remember)
            flash('Вы успешно аутентифицированы.', 'success')
            next = request.args.get('next')
            return redirect(next or url_for('index'))
        flash("Невозможно аутентифицироваться с указанными логином и паролем", "danger")
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы успешно вышли.', 'success')
    return redirect(url_for('index'))

# @app.route('/add')
# def index():
#     return render_template('add.html')

# python3 -m venv ve
# . ve/bin/activate -- Linux
# ve\Scripts\activate -- Windows
# pip install flask python-dotenv
