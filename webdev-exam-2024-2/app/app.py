from flask import Flask, render_template, flash, request, redirect, url_for, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from datetime import date
import hashlib
import os
import bleach
import markdown
from werkzeug.security import check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import YEAR
from sqlalchemy.sql import func
import traceback

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

class Books(db.Model):
    __tablename__ = 'books'
    
    id = db.Column(db.INT, primary_key=True) 
    name = db.Column(db.VARCHAR(100)) # VARCHAR
    description = db.Column(db.TEXT) # TEXT
    year = db.Column(YEAR) # YEAR 
    publishing_house = db.Column(db.VARCHAR(100)) # VARCHAR
    author = db.Column(db.VARCHAR(100)) # VARCHAR
    pages = db.Column(db.INT) # INT
    cover = db.Column(db.INT, db.ForeignKey('covers.id',ondelete='CASCADE')) # Внешний ключ
    
    reviews = db.relationship('Reviews', backref='books', uselist=True)
    genres = db.relationship('BooksAndGenres', backref='books', uselist=True)
    cover_image = db.relationship('Covers', backref='books', uselist=False)

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
    book = db.Column(db.INT, db.ForeignKey('books.id', ondelete='CASCADE')) # Внешний ключ
    genre =  db.Column(db.INT, db.ForeignKey('genres.id')) # Внешний ключ
    
    def __repr__(self):
        return f"<books_and_genres {self.id}>"

class Reviews(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.INT, primary_key=True) 
    book = db.Column(db.INT, db.ForeignKey('books.id', ondelete='CASCADE')) # Внешний ключ
    user = db.Column(db.INT, db.ForeignKey('users.id')) # Внешний ключ
    grade = db.Column(db.INT) # INT
    text = db.Column(db.TEXT) # TEXT
    date = db.Column(db.Date, default = date.today) # DATE
    status =  db.Column(db.INT, db.ForeignKey('statuses.id'), default = 1) # Внешний ключ
    
    book_info = db.relationship('Books', backref='reviewss', uselist=False)
    user_info = db.relationship('Users', backref='reviews', uselist=False)
    status_info = db.relationship('Statuses', backref='reviews', uselist=False)
    
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
    
class Statuses(db.Model):
    __tablename__ = 'statuses'
    
    id = db.Column(db.INT, primary_key=True) 
    name = db.Column(db.VARCHAR(100)) # VARCHAR
    
    def __repr__(self):
        return f"<statuses {self.id}>"

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
    genres = Genres.query.all()
    books = Books.query.order_by(Books.year.desc()).all()
    reviews_stats = db.session.query(func.avg(Reviews.grade).label('average'), func.count(Reviews.grade).label('count'), Reviews.book).group_by(Reviews.book).filter(Reviews.status==2).all()
    reviewed_books = [avg.book for avg in reviews_stats]
    return render_template('index.html', books=books, genres=genres, reviews_stats=reviews_stats, reviewed_books=reviewed_books)

@app.route('/view/<int:id>')
def view(id):
    book = Books.query.filter(Books.id==id).first()
    genres = Genres.query.all()
    reviews = Reviews.query.filter(Reviews.book==id).filter(Reviews.status==2).all()
    
    if current_user.is_authenticated and len(db.session.query(Reviews).filter(Reviews.user==current_user.id).filter(Reviews.book==id).all())==0:
        can_write_review = True
    else:
        can_write_review = False
    
    return render_template('view.html', book=book, genres=genres, reviews=reviews, can_write_review=can_write_review, md=markdown.markdown)

@app.route('/write_review/<int:id>', methods=['GET','POST'])
@login_required
def write_review(id):
    if request.method == "POST":
        try:
            #  форма
            grade = request.form.get('book-grade')
            review = request.form.get('book-review')
            review = bleach.clean(review)
            print(grade, review)
            
            # отзыв для бд
            review = Reviews(
                book = id,
                user = current_user.id,
                grade = int(grade),
                text = review
            )
                        
            db.session.add(review)
            db.session.flush()
            db.session.commit()
            print("Book id ", review.id)
                    
            return redirect(url_for('index'))
        except Exception as e: 
            traceback.print_exc()
            db.session.rollback()
            flash("При сохранении данных возникла ошибка. Проверьте корректность введённых данных.", "danger")
            return redirect(url_for('index'))
    else:
        return render_template('write_review.html')


@app.route('/my_reviews')
@login_required
def my_reviews():
    reviews = Reviews.query.filter(Reviews.user==current_user.id).all()
    return render_template('my_reviews.html', reviews=reviews, md=markdown.markdown) 
    
@app.route('/moderate_reviews', methods=['GET','POST'])
@login_required
def moderate_reviews():
    id = request.args.get('id')
    action = request.args.get('action')
    if id and action:        
        review = Reviews.query.filter(Reviews.id==id).first()
        review.status = 2 if action=="allow" else 3
        db.session.flush()
        db.session.commit()
        print(review.status, review)
        return redirect(url_for('moderate_reviews'))

    reviews = Reviews.query.filter(Reviews.status==1).all()
    return render_template('moderate_reviews.html', reviews=reviews, md=markdown.markdown) 

@app.route('/delete/<int:id>')
def delete(id):
    if not current_user.is_admin: # если не админ
        flash("Недостаточно прав для выполнения этого действия.", "danger")
    else:
        try:
            book = db.session.query(Books).get(id)
            db.session.delete(book)
            db.session.flush()
            db.session.commit()   
            flash("Книга успешно удалена.", "success")
        except: 
            traceback.print_exc()
            db.session.rollback()
            flash("При удалении возникла ошибка.", "danger")
    
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET','POST'])
def edit(id):
    genres = Genres.query.all()
    if request.method == "POST":
        try:
            #  форма
            name = request.form.get('book-name')
            description = request.form.get('book-description')
            description = bleach.clean(description)
            year =  request.form.get('book-year')
            publishing_house = request.form.get('book-publishing-house')
            author = request.form.get('book-author')
            pages =  request.form.get('book-pages')
            book_genres = request.form.getlist('book-genres')
            
            # объект книги
            book = db.session.query(Books).get(id)
            
            # новые поля книги
            book.name = name
            book.description = description
            book.year = year
            book.publishing_house = publishing_house
            book.author = author
            book.pages = pages
            db.session.commit()
            
            # новые жанры
            old_genres = db.session.query(BooksAndGenres).filter(BooksAndGenres.book==book.id).all()
            if old_genres:
                for old_g in old_genres:
                    db.session.delete(old_g)
                db.session.flush()
            for genre in genres: 
                if genre.name in book_genres:
                    db.session.add(BooksAndGenres(book=book.id, genre=genre.id))
            db.session.commit()   
        
            return redirect(url_for('index'))
        except Exception as e: 
            traceback.print_exc()
            db.session.rollback()
            book = Books(
                name = name,
                description = description,
                year = year,
                publishing_house = publishing_house,
                author = author,
                pages = pages,
                cover = 1 # наш ключ обложки
            )
            flash("При сохранении данных возникла ошибка. Проверьте корректность введённых данных.", "danger")
            return render_template('edit.html', book=book, genres=genres)
    else:
        book = Books.query.filter(Books.id==id).first()
        return render_template('edit.html', book=book, genres=genres)

@app.route('/add', methods=['GET','POST'])
@login_required
def add():
    genres = Genres.query.all()
    print(genres)
    if request.method == 'POST':
        try:    
            # поля формы
            name = request.form.get('book-name')
            description = request.form.get('book-description')
            description = bleach.clean(description)
            year =  request.form.get('book-year')
            publishing_house = request.form.get('book-publishing-house')
            author = request.form.get('book-author')
            pages =  request.form.get('book-pages')
            book_genres = request.form.getlist('book-genres')
            image = request.files.get('book-cover')
            
            print(name, description, year, publishing_house, author, pages, image, book_genres)
            
            # данные для добавления картинки
            image_name = image.filename
            image_content = image.read() 
            image_hash = hashlib.md5(image_content).hexdigest()
            image_mimetype = image.mimetype
            image_in_db = Covers.query.filter(Covers.md5_hash==image_hash).first()
            
            print(image_name, image_hash, image_mimetype, image_in_db)
            
            # Сохранение обложки или получение её из бд
            if (image_in_db == None):
                cover = Covers(
                    name = image_name,
                    mime_type = image_mimetype,
                    md5_hash = image_hash
                )
                db.session.add(cover)
                db.session.flush()
                db.session.commit()
                cover_id = cover.id
            else:
                cover_id = image_in_db.id
            
            print("Обложка", cover_id)
            # книга для бд
            book = Books(
                name = name,
                description = description,
                year = year,
                publishing_house = publishing_house,
                author = author,
                pages = pages,
                cover = cover_id # наш ключ обложки
            )
                        
            db.session.add(book)
            db.session.flush()
            print("Book id ", book.id)
            db.session.commit()
            
            # жанры
            if book_genres:
                for genre in genres: #"проза" 
                    if genre.name in book_genres:
                        db.session.add(BooksAndGenres(book=book.id, genre=genre.id))
            
            db.session.flush()
            db.session.commit()
            # сохраняем файл если предыдущие шаги успешны
            if (image_in_db == None):
                with open(os.path.join(app.config['UPLOAD_FOLDER'], image_name), "wb") as f:
                    f.write(image_content)
                    
            return redirect(url_for('index'))
        except Exception as e: 
            db.session.rollback()
            book = Books(
                name = name,
                description = description,
                year = year,
                publishing_house = publishing_house,
                author = author,
                pages = pages,
                cover = 1 # наш ключ обложки
            )
            flash("При сохранении данных возникла ошибка. Проверьте корректность введённых данных.", "danger")
            return render_template('add.html', book=book, genres=genres)
    else:
        return render_template('add.html', book='', genres=genres)


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

# TODO:
# Пагинация 
#  - книги
#  - рецензии
# python3 -m venv ve
# . ve/bin/activate -- Linux
# ve\Scripts\activate -- Windows
# pip install flask python-dotenv
